#!/usr/bin/env python3
"""
Fetch TIPs from GitHub repository HTML (no GitHub API)
"""
import json
import time
import requests
from bs4 import BeautifulSoup
import re
import os

def fetch_tips():
    """Scrape TIPs from GitHub repository HTML"""
    print("Fetching TIPs from GitHub repository HTML...")
    
    BASE_URL = "https://github.com/tronprotocol/TIPs"
    
    try:
        # Get the repository file listing page
        r = requests.get(BASE_URL, timeout=30)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        
        rows = []
        
        # Find all TIP files in the repository
        print("Looking for TIP files in repository...")
        
        # Look for file links that match tip-*.md pattern
        tip_links = []
        for link in soup.find_all("a", href=True):
            href = link.get("href", "")
            if "/blob/master/tip-" in href and href.endswith(".md"):
                tip_links.append(href)
        
        print(f"Found {len(tip_links)} TIP files")
        
        for i, tip_link in enumerate(tip_links):
            try:
                # Extract TIP number from URL
                match = re.search(r'tip-(\d+)\.md', tip_link)
                if not match:
                    continue
                
                tip_number = int(match.group(1))
                tip_id = f"TIP-{tip_number}"
                
                # Get the raw content URL to read the file
                raw_url = f"https://raw.githubusercontent.com/tronprotocol/TIPs/master/tip-{tip_number}.md"
                
                # Fetch the file content
                file_response = requests.get(raw_url, timeout=10)
                
                if file_response.status_code == 200:
                    content = file_response.text
                    
                    # Parse TIP metadata from content
                    tip_data = parse_tip_content(content, tip_number)
                    tip_data.update({
                        "id": tip_id,
                        "number": tip_number,
                        "url": f"https://github.com{tip_link}",
                        "file_url": f"https://github.com{tip_link}",
                        "protocol": "tron",
                        "source": BASE_URL,
                    })
                    
                    rows.append(tip_data)
                    
                    # Progress indicator
                    if (i + 1) % 10 == 0:
                        print(f"  Processed {i + 1}/{len(tip_links)} TIPs...")
                        
                else:
                    # If we can't get the content, create basic entry
                    rows.append({
                        "id": tip_id,
                        "number": tip_number,
                        "title": f"TIP-{tip_number}",
                        "status": "Unknown",
                        "author": "Unknown",
                        "created": "Unknown",
                        "type": "Unknown",
                        "category": "Unknown",
                        "url": f"https://github.com{tip_link}",
                        "file_url": f"https://github.com{tip_link}",
                        "protocol": "tron",
                        "summary": f"TIP-{tip_number} proposal",
                        "source": BASE_URL,
                    })
                    
            except Exception as e:
                print(f"  Warning: Error processing TIP {tip_link}: {e}")
                continue
        
        print(f"Successfully scraped {len(rows)} TIPs")
        
        # Sort by number (latest first)
        rows.sort(key=lambda x: x["number"], reverse=True)
        
        return rows
        
    except Exception as e:
        print(f"Error fetching TIPs: {e}")
        return []

def parse_tip_content(content, tip_number):
    """Parse TIP content to extract metadata"""
    
    tip_data = {
        "title": f"TIP-{tip_number}",
        "status": "Unknown",
        "author": "Unknown",
        "created": "Unknown",
        "type": "Unknown",
        "category": "Unknown",
        "summary": content[:200] + '...' if len(content) > 200 else content
    }
    
    try:
        # Check for TIP format (starts with ``` code block)
        if content.startswith('```'):
            lines = content.split('\n')
            in_frontmatter = False
            body_start = 0
            
            for i, line in enumerate(lines):
                line = line.strip()
                
                if line == '```' and not in_frontmatter:
                    in_frontmatter = True
                    continue
                elif line == '```' and in_frontmatter:
                    in_frontmatter = False
                    body_start = i + 1
                    break
                elif in_frontmatter and ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower()
                    value = value.strip().strip('"\'')
                    
                    if key == 'title':
                        tip_data['title'] = value
                    elif key == 'status':
                        tip_data['status'] = value
                    elif key in ['author', 'authors']:
                        # Handle author format like "name email@domain.com"
                        if '@' in value and ' ' in value:
                            tip_data['author'] = value.split()[0]
                        else:
                            tip_data['author'] = value
                    elif key in ['created', 'date']:
                        tip_data['created'] = value
                    elif key == 'type':
                        tip_data['type'] = value
                    elif key == 'category':
                        tip_data['category'] = value
            
            # Get summary from body after frontmatter
            if body_start < len(lines):
                body_lines = [line.strip() for line in lines[body_start:] if line.strip() and not line.startswith('#')]
                if body_lines:
                    tip_data['summary'] = ' '.join(body_lines[:3])[:300] + '...'
        
        # Handle YAML frontmatter format (alternative)
        elif content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                body = parts[2]
                
                # Parse YAML-like frontmatter
                for line in frontmatter.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip().lower()
                        value = value.strip().strip('"\'')
                        
                        if key == 'title':
                            tip_data['title'] = value
                        elif key == 'status':
                            tip_data['status'] = value
                        elif key in ['author', 'authors']:
                            tip_data['author'] = value
                        elif key in ['created', 'date']:
                            tip_data['created'] = value
                        elif key == 'type':
                            tip_data['type'] = value
                        elif key == 'category':
                            tip_data['category'] = value
                
                # Get summary from body
                body_lines = [line.strip() for line in body.split('\n') if line.strip()]
                if body_lines:
                    tip_data['summary'] = ' '.join(body_lines[:3])[:300] + '...'
    
    except Exception:
        pass  # Use defaults if parsing fails
    
    return tip_data

def save_tips_data(tips_data, output_file="data/tips.json"):
    """Save TIPs data to JSON file"""
    
    out = {
        "generated_at": int(time.time()),
        "generated_at_iso": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "count": len(tips_data),
        "protocol": "tron",
        "source": "https://github.com/tronprotocol/TIPs",
        "items": tips_data,
    }
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(tips_data)} TIPs to {output_file}")
    return output_file

if __name__ == "__main__":
    tips = fetch_tips()
    if tips:
        save_tips_data(tips)
        print(f"SUCCESS: TIPs fetch completed successfully!")
        
        # Show sample of latest TIPs
        print("\nLatest 5 TIPs:")
        for tip in tips[:5]:
            print(f"  {tip['id']}: {tip['title']} ({tip['status']})")
            
        # Show draft TIPs count
        draft_tips = [t for t in tips if t['status'].lower() in ['draft', 'idea', 'open']]
        print(f"\nFound {len(draft_tips)} draft TIPs:")
        for tip in draft_tips:
            print(f"  {tip['id']}: {tip['title']} (Status: {tip['status']})")
        
        # Show status breakdown
        status_counts = {}
        for tip in tips:
            status = tip['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print(f"\nStatus breakdown:")
        for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {status}: {count} TIPs")
    else:
        print("FAILED: Failed to fetch TIPs")