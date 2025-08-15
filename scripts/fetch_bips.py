#!/usr/bin/env python3
"""
Fetch BIPs from GitHub repository HTML (no GitHub API)
"""
import json
import time
import requests
from bs4 import BeautifulSoup
import re
import os

def fetch_bips():
    """Scrape BIPs from GitHub repository HTML"""
    print("Fetching BIPs from GitHub repository HTML...")
    
    BASE_URL = "https://github.com/bitcoin/bips"
    
    try:
        # Get the repository file listing page
        r = requests.get(BASE_URL, timeout=30)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        
        rows = []
        
        # Find all BIP files in the repository
        print("Looking for BIP files in repository...")
        
        # Look for file links that match bip-*.mediawiki pattern
        bip_links = []
        for link in soup.find_all("a", href=True):
            href = link.get("href", "")
            if "/blob/master/bip-" in href and href.endswith(".mediawiki"):
                # Extract BIP number for sorting
                match = re.search(r'bip-(\d+)\.mediawiki', href)
                if match:
                    bip_number = int(match.group(1))
                    bip_links.append((bip_number, href))
        
        # Sort by BIP number (descending) to get latest first
        bip_links.sort(reverse=True)
        
        print(f"Found {len(bip_links)} BIP files")
        
        for i, (bip_number, bip_link) in enumerate(bip_links):
            try:
                bip_id = f"BIP-{bip_number}"
                
                # Get the raw content URL
                raw_url = f"https://raw.githubusercontent.com/bitcoin/bips/master/bip-{bip_number:04d}.mediawiki"
                
                # Fetch the file content
                file_response = requests.get(raw_url, timeout=10)
                
                if file_response.status_code == 200:
                    content = file_response.text
                    
                    # Parse BIP metadata from content
                    bip_data = parse_bip_content(content, bip_number)
                    bip_data.update({
                        "id": bip_id,
                        "number": bip_number,
                        "url": f"https://github.com{bip_link}",
                        "file_url": f"https://github.com{bip_link}",
                        "protocol": "bitcoin",
                        "source": BASE_URL,
                    })
                    
                    rows.append(bip_data)
                    
                else:
                    # If we can't get the content, create basic entry
                    rows.append({
                        "id": bip_id,
                        "number": bip_number,
                        "title": f"BIP-{bip_number}",
                        "status": "Unknown",
                        "author": "Unknown",
                        "created": "Unknown",
                        "type": "Unknown",
                        "layer": "Unknown",
                        "url": f"https://github.com{bip_link}",
                        "file_url": f"https://github.com{bip_link}",
                        "protocol": "bitcoin",
                        "summary": f"BIP-{bip_number} proposal",
                        "source": BASE_URL,
                    })
                
                # Progress indicator
                if (i + 1) % 20 == 0:
                    print(f"  Processed {i + 1}/{len(bip_links)} BIPs...")
                    
            except Exception as e:
                print(f"  Warning: Error processing BIP-{bip_number}: {e}")
                continue
        
        print(f"Successfully scraped {len(rows)} BIPs")
        
        # Sort by number (latest first)
        rows.sort(key=lambda x: x["number"], reverse=True)
        
        return rows
        
    except Exception as e:
        print(f"Error fetching BIPs: {e}")
        return []

def parse_bip_content(content, bip_number):
    """Parse BIP content to extract metadata from MediaWiki format"""
    
    bip_data = {
        "title": f"BIP-{bip_number}",
        "status": "Unknown",
        "author": "Unknown",
        "created": "Unknown",
        "type": "Unknown",
        "layer": "Unknown",
        "summary": content[:200] + '...' if len(content) > 200 else content
    }
    
    try:
        # MediaWiki format - metadata is at the top in key: value format
        lines = content.split('\n')
        
        # Look through first 30 lines for metadata
        for line in lines[:30]:
            line = line.strip()
            
            if ':' in line and not line.startswith('==') and not line.startswith('<!--'):
                # Split on first colon only
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip().lower()
                    value = parts[1].strip()
                    
                    # Clean up value (remove wiki markup)
                    value = re.sub(r'\[\[([^\]|]+)(\|[^\]]*)?\]\]', r'\1', value)  # [[link|text]] -> link
                    value = re.sub(r'\[([^\s]+)\s+([^\]]+)\]', r'\2', value)  # [url text] -> text
                    value = re.sub(r'<[^>]+>', '', value)  # Remove HTML tags
                    
                    if key == 'bip':
                        # BIP number field
                        bip_num = re.search(r'\d+', value)
                        if bip_num:
                            bip_data['number'] = int(bip_num.group())
                    elif key == 'title':
                        bip_data['title'] = value
                    elif key == 'status':
                        bip_data['status'] = value
                    elif key in ['author', 'authors']:
                        # Extract just names, remove email addresses
                        author_clean = re.sub(r'<[^>]+>', '', value)  # Remove email addresses
                        bip_data['author'] = author_clean
                    elif key in ['created', 'date']:
                        bip_data['created'] = value
                    elif key == 'type':
                        bip_data['type'] = value
                    elif key == 'layer':
                        bip_data['layer'] = value
        
        # Extract summary from content after metadata
        # Look for the first substantial paragraph
        content_lines = content.split('\n')
        in_content = False
        summary_lines = []
        
        for line in content_lines:
            line = line.strip()
            
            # Skip metadata section
            if ':' in line and not in_content and not line.startswith('=='):
                continue
            elif line.startswith('=='):
                in_content = True
                continue
            elif in_content and line and not line.startswith('=='):
                # Clean up wiki markup for summary
                clean_line = re.sub(r'\[\[([^\]|]+)(\|[^\]]*)?\]\]', r'\1', line)
                clean_line = re.sub(r'\[([^\s]+)\s+([^\]]+)\]', r'\2', clean_line)
                clean_line = re.sub(r'<[^>]+>', '', clean_line)
                clean_line = re.sub(r"'{2,}", '', clean_line)  # Remove bold/italic markup
                
                if clean_line and len(clean_line) > 10:
                    summary_lines.append(clean_line)
                    if len(summary_lines) >= 2:  # Get first 2 substantial lines
                        break
        
        if summary_lines:
            bip_data['summary'] = ' '.join(summary_lines)[:400] + '...'
    
    except Exception:
        pass  # Use defaults if parsing fails
    
    return bip_data

def save_bips_data(bips_data, output_file="data/bips.json"):
    """Save BIPs data to JSON file"""
    
    out = {
        "generated_at": int(time.time()),
        "generated_at_iso": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "count": len(bips_data),
        "protocol": "bitcoin",
        "source": "https://github.com/bitcoin/bips",
        "items": bips_data,
    }
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(bips_data)} BIPs to {output_file}")
    return output_file

if __name__ == "__main__":
    bips = fetch_bips()
    if bips:
        save_bips_data(bips)
        print(f"SUCCESS: BIPs fetch completed successfully!")
        
        # Show sample of latest BIPs
        print("\nLatest 5 BIPs:")
        for bip in bips[:5]:
            print(f"  {bip['id']}: {bip['title']} ({bip['status']})")
        
        # Show status breakdown
        status_counts = {}
        for bip in bips:
            status = bip['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print(f"\nStatus breakdown:")
        for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {status}: {count} BIPs")
    else:
        print("FAILED: Failed to fetch BIPs")