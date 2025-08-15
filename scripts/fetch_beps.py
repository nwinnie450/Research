#!/usr/bin/env python3
"""
Fetch BEPs from GitHub repository HTML (no GitHub API)
"""
import json
import time
import requests
from bs4 import BeautifulSoup
import re
import os

def fetch_beps():
    """Scrape BEPs from GitHub repository HTML"""
    print("Fetching BEPs from GitHub repository HTML...")
    
    BASE_URL = "https://github.com/bnb-chain/BEPs"
    
    try:
        # Get the repository file listing page
        r = requests.get(BASE_URL, timeout=30)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        
        rows = []
        
        # Find all BEP files in the repository
        print("Looking for BEP files in repository...")
        
        # Look for file links that match BEP-*.md pattern
        bep_links = []
        for link in soup.find_all("a", href=True):
            href = link.get("href", "")
            if "/blob/master/BEPs/BEP-" in href and href.endswith(".md"):
                # Extract BEP number for sorting
                match = re.search(r'BEP-(\d+)\.md', href)
                if match:
                    bep_number = int(match.group(1))
                    bep_links.append((bep_number, href))
            elif "/blob/master/BEP" in href and href.endswith(".md"):
                # Alternative pattern: /BEP123.md
                match = re.search(r'BEP(\d+)\.md', href)
                if match:
                    bep_number = int(match.group(1))
                    bep_links.append((bep_number, href))
        
        # Sort by BEP number (descending) to get latest first
        bep_links.sort(reverse=True)
        
        print(f"Found {len(bep_links)} BEP files")
        
        for i, (bep_number, bep_link) in enumerate(bep_links):
            try:
                bep_id = f"BEP-{bep_number}"
                
                # Construct raw content URL based on the actual link structure
                raw_url = f"https://raw.githubusercontent.com{bep_link.replace('/blob/', '/')}"
                
                # Fetch the file content
                file_response = requests.get(raw_url, timeout=10)
                
                if file_response.status_code == 200:
                    content = file_response.text
                    
                    # Parse BEP metadata from content
                    bep_data = parse_bep_content(content, bep_number)
                    bep_data.update({
                        "id": bep_id,
                        "number": bep_number,
                        "url": f"https://github.com{bep_link}",
                        "file_url": f"https://github.com{bep_link}",
                        "protocol": "binance_smart_chain",
                        "source": BASE_URL,
                    })
                    
                    rows.append(bep_data)
                    
                else:
                    # If we can't get the content, create basic entry
                    rows.append({
                        "id": bep_id,
                        "number": bep_number,
                        "title": f"BEP-{bep_number}",
                        "status": "Unknown",
                        "author": "Unknown",
                        "created": "Unknown",
                        "type": "Unknown",
                        "url": f"https://github.com{bep_link}",
                        "file_url": f"https://github.com{bep_link}",
                        "protocol": "binance_smart_chain",
                        "summary": f"BEP-{bep_number} proposal",
                        "source": BASE_URL,
                    })
                
                # Progress indicator
                if (i + 1) % 10 == 0:
                    print(f"  Processed {i + 1}/{len(bep_links)} BEPs...")
                    
            except Exception as e:
                print(f"  Warning: Error processing BEP-{bep_number}: {e}")
                continue
        
        print(f"Successfully scraped {len(rows)} BEPs")
        
        # Sort by number (latest first)
        rows.sort(key=lambda x: x["number"], reverse=True)
        
        return rows
        
    except Exception as e:
        print(f"Error fetching BEPs: {e}")
        return []

def parse_bep_content(content, bep_number):
    """Parse BEP content to extract metadata from <pre> format"""
    
    bep_data = {
        "title": f"BEP-{bep_number}",
        "status": "Unknown",
        "author": "Unknown",
        "created": "Unknown",
        "type": "Unknown",
        "summary": content[:200] + '...' if len(content) > 200 else content
    }
    
    try:
        # BEPs use <pre> tags with metadata
        if '<pre>' in content:
            # Extract content between <pre> and </pre>
            pre_match = re.search(r'<pre>(.*?)</pre>', content, re.DOTALL)
            if pre_match:
                pre_content = pre_match.group(1).strip()
                
                # Parse metadata from pre block
                for line in pre_content.split('\n'):
                    line = line.strip()
                    
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip().lower()
                        value = value.strip()
                        
                        if key == 'bep':
                            try:
                                bep_data['number'] = int(value)
                            except:
                                pass
                        elif key == 'title':
                            bep_data['title'] = value
                        elif key == 'status':
                            bep_data['status'] = value
                        elif key in ['author', 'authors']:
                            bep_data['author'] = value
                        elif key in ['created', 'date']:
                            bep_data['created'] = value
                        elif key == 'type':
                            bep_data['type'] = value
                
                # Extract summary from content after </pre>
                post_pre = content.split('</pre>', 1)
                if len(post_pre) > 1:
                    body = post_pre[1]
                    
                    # Find first substantial paragraph
                    body_lines = body.split('\n')
                    summary_lines = []
                    
                    for line in body_lines:
                        line = line.strip()
                        
                        # Skip headers, links, empty lines
                        if (line and not line.startswith('#') and 
                            not line.startswith('-') and 
                            not line.startswith('[') and
                            len(line) > 30):
                            
                            summary_lines.append(line)
                            if len(summary_lines) >= 2:
                                break
                    
                    if summary_lines:
                        bep_data['summary'] = ' '.join(summary_lines)[:400] + '...'
        
        # Fallback: look for inline metadata patterns
        else:
            lines = content.split('\n')
            
            for line in lines[:15]:
                line = line.strip()
                
                # Look for various metadata patterns
                if line.startswith('BEP:'):
                    try:
                        bep_data['number'] = int(line.split(':', 1)[1].strip())
                    except:
                        pass
                elif line.startswith('Title:'):
                    bep_data['title'] = line.split(':', 1)[1].strip()
                elif line.startswith('Status:'):
                    bep_data['status'] = line.split(':', 1)[1].strip()
                elif line.startswith('Author:'):
                    bep_data['author'] = line.split(':', 1)[1].strip()
                elif line.startswith('Created:'):
                    bep_data['created'] = line.split(':', 1)[1].strip()
                elif line.startswith('Type:'):
                    bep_data['type'] = line.split(':', 1)[1].strip()
    
    except Exception:
        pass  # Use defaults if parsing fails
    
    return bep_data

def save_beps_data(beps_data, output_file="data/beps.json"):
    """Save BEPs data to JSON file"""
    
    out = {
        "generated_at": int(time.time()),
        "generated_at_iso": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "count": len(beps_data),
        "protocol": "binance_smart_chain",
        "source": "https://github.com/bnb-chain/BEPs",
        "items": beps_data,
    }
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(beps_data)} BEPs to {output_file}")
    return output_file

if __name__ == "__main__":
    beps = fetch_beps()
    if beps:
        save_beps_data(beps)
        print(f"SUCCESS: BEPs fetch completed successfully!")
        
        # Show sample of latest BEPs
        print("\nLatest 5 BEPs:")
        for bep in beps[:5]:
            print(f"  {bep['id']}: {bep['title']} ({bep['status']})")
        
        # Show status breakdown
        status_counts = {}
        for bep in beps:
            status = bep['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print(f"\nStatus breakdown:")
        for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {status}: {count} BEPs")
    else:
        print("FAILED: Failed to fetch BEPs")