#!/usr/bin/env python3
"""
Updated TIP scraper to get all TRON TIPs from GitHub repository
"""
import json
import time
import requests
from bs4 import BeautifulSoup
import re
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def parse_tip_content(content, tip_number):
    """Parse TIP content to extract metadata"""
    lines = content.split('\n')
    
    tip_data = {
        'title': 'Unknown',
        'status': 'Unknown', 
        'author': 'Unknown',
        'created': '',
        'type': 'Unknown',
        'category': 'Unknown'
    }
    
    # Look for YAML frontmatter or structured metadata
    in_frontmatter = False
    frontmatter_end = False
    
    for i, line in enumerate(lines[:50]):  # Check first 50 lines
        line = line.strip()
        
        # Check for YAML frontmatter markers
        if line == '---' and i == 0:
            in_frontmatter = True
            continue
        elif line == '---' and in_frontmatter:
            frontmatter_end = True
            break
        
        # Parse metadata (both YAML and other formats)
        if ':' in line:
            key_value = line.split(':', 1)
            if len(key_value) == 2:
                key = key_value[0].strip().lower()
                value = key_value[1].strip().strip('"\'')
                
                if 'title' in key:
                    tip_data['title'] = value
                elif 'status' in key:
                    tip_data['status'] = value
                elif 'author' in key:
                    tip_data['author'] = value
                elif 'created' in key:
                    tip_data['created'] = value
                elif 'type' in key:
                    tip_data['type'] = value
                elif 'category' in key:
                    tip_data['category'] = value
        
        # Also look for markdown-style headers
        if line.startswith('# ') and 'title' not in tip_data or tip_data['title'] == 'Unknown':
            potential_title = line[2:].strip()
            if not potential_title.lower().startswith('tip-'):
                tip_data['title'] = potential_title
    
    return tip_data

def fetch_single_tip(tip_number, session):
    """Fetch a single TIP's metadata"""
    try:
        # Use the correct repository URL structure
        raw_url = f"https://raw.githubusercontent.com/tronprotocol/tips/master/tip-{tip_number:02d}.md"
        
        r = session.get(raw_url, timeout=15)
        if r.status_code == 404:
            # Try without zero padding
            raw_url = f"https://raw.githubusercontent.com/tronprotocol/tips/master/tip-{tip_number}.md"
            r = session.get(raw_url, timeout=15)
        
        if r.status_code == 404:
            return None  # TIP doesn't exist
            
        r.raise_for_status()
        content = r.text
        
        # Parse the content
        tip_data = parse_tip_content(content, tip_number)
        
        # Create the full TIP object
        tip_object = {
            'title': tip_data['title'],
            'status': tip_data['status'],
            'author': tip_data['author'],
            'created': tip_data['created'],
            'type': tip_data['type'],
            'category': tip_data['category'],
            'id': f'TIP-{tip_number}',
            'number': tip_number,
            'url': f'https://github.com/tronprotocol/tips/blob/master/tip-{tip_number:02d}.md',
            'file_url': f'https://github.com/tronprotocol/tips/blob/master/tip-{tip_number:02d}.md',
            'protocol': 'tron',
            'summary': f"{tip_data['title']} - {tip_data['status']} TIP by {tip_data['author']}",
            'source': 'https://github.com/tronprotocol/tips'
        }
        
        return tip_object
        
    except Exception as e:
        print(f"  Error fetching TIP-{tip_number}: {e}")
        return None

def fetch_tips_updated():
    """Fetch all TRON TIPs with updated scraper"""
    print("Fetching TRON TIPs with updated scraper...")
    print("This may take a few minutes to get all TIPs...")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    # Try to get TIP numbers from repository listing first
    print("Getting TIP list from repository...")
    
    try:
        r = session.get('https://github.com/tronprotocol/tips', timeout=30)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Extract TIP numbers from file links
        tip_numbers = set()
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            match = re.search(r'tip-(\d+)\.md', href)
            if match:
                tip_numbers.add(int(match.group(1)))
        
        print(f"Found {len(tip_numbers)} TIP numbers in repository")
        
        if not tip_numbers:
            print("No TIP numbers found, trying sequential approach...")
            # Fallback: try sequential numbers (most TIPs follow this pattern)
            tip_numbers = set(range(1, 500))  # Try TIP-1 to TIP-499
        
    except Exception as e:
        print(f"Error getting repository listing: {e}")
        print("Using sequential approach...")
        tip_numbers = set(range(1, 500))
    
    tip_numbers = sorted(tip_numbers)
    print(f"Attempting to fetch {len(tip_numbers)} TIPs...")
    
    # Fetch TIPs with threading for better performance
    successful_tips = []
    
    def fetch_batch(tip_nums):
        batch_results = []
        for tip_num in tip_nums:
            result = fetch_single_tip(tip_num, session)
            if result:
                batch_results.append(result)
                if len(batch_results) % 10 == 0:
                    print(f"  Progress: {len(successful_tips) + len(batch_results)} TIPs fetched...")
        return batch_results
    
    # Process in batches to avoid overwhelming the server
    batch_size = 20
    for i in range(0, len(tip_numbers), batch_size):
        batch = tip_numbers[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1}: TIPs {batch[0]}-{batch[-1]}")
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            batch_tips = fetch_batch(batch)
            successful_tips.extend(batch_tips)
        
        # Be nice to the server
        time.sleep(1)
    
    print(f"Successfully fetched {len(successful_tips)} TIPs")
    
    # Sort by TIP number (descending for latest first)
    successful_tips.sort(key=lambda x: x.get('number', 0), reverse=True)
    
    # Create output data
    output_data = {
        'generated_at': int(time.time()),
        'generated_at_iso': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()),
        'count': len(successful_tips),
        'protocol': 'tron',
        'source': 'https://github.com/tronprotocol/tips',
        'items': successful_tips
    }
    
    # Save to file
    os.makedirs('data', exist_ok=True)
    output_file = 'data/tips.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nSUCCESS: Updated TIPs data saved to {output_file}")
    print(f"Total TIPs: {len(successful_tips):,}")
    
    # Show latest TIPs
    if successful_tips:
        print(f"\nLatest TIPs:")
        for tip in successful_tips[:5]:
            print(f"   TIP-{tip['number']}: {tip['title'][:50]}... (Created: {tip['created']}, Status: {tip['status']})")
        
        # Show TIP number range
        tip_numbers_found = [tip['number'] for tip in successful_tips]
        print(f"\nTIP number range: TIP-{min(tip_numbers_found)} to TIP-{max(tip_numbers_found)}")
        
        # Show status distribution
        status_counts = {}
        for tip in successful_tips:
            status = tip['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print(f"\nStatus distribution:")
        for status, count in sorted(status_counts.items()):
            print(f"   {status}: {count} TIPs")

if __name__ == "__main__":
    fetch_tips_updated()