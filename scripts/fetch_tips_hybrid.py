#!/usr/bin/env python3
"""
Hybrid TIP scraper combining GitHub Issues UI and markdown file approaches
This provides maximum coverage by using both methods
"""
import json
import time
import requests
from bs4 import BeautifulSoup
import re
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def parse_tip_content(content, tip_number):
    """Parse TIP content to extract metadata (from markdown files)"""
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
        if line.startswith('# ') and (tip_data['title'] == 'Unknown' or 'title' not in tip_data):
            potential_title = line[2:].strip()
            if not potential_title.lower().startswith('tip-'):
                tip_data['title'] = potential_title
    
    return tip_data

def fetch_single_tip_markdown(tip_number, session):
    """Fetch a single TIP's metadata from markdown file"""
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
        return None

def fetch_tips_from_issues(session):
    """Scrape TIPs from GitHub Issues UI to find newer/active TIPs"""
    print("Fetching newer TIPs from GitHub Issues UI...")
    
    all_tips = []
    page = 1
    
    # Base URL for TIP issues (sorted by creation date, descending)
    base_url = "https://github.com/tronprotocol/tips/issues"
    
    while page <= 5:  # Limit to first 5 pages for efficiency
        try:
            url = f"{base_url}?q=is%3Aissue&sort=created-desc&page={page}"
            
            response = session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find issue links
            issue_links = soup.find_all('a', href=True)
            tip_links = []
            for link in issue_links:
                href = link.get('href', '')
                text = link.get_text().lower()
                if '/issues/' in href and ('tip' in text or re.search(r'tip[-\s]?\d+', text, re.I)):
                    tip_links.append(link)
            
            if not tip_links:
                break
            
            page_tips = []
            
            for link in tip_links:
                try:
                    tip_data = extract_tip_from_issue_link(link)
                    if tip_data:
                        page_tips.append(tip_data)
                
                except Exception:
                    continue
            
            if not page_tips:
                break
            
            all_tips.extend(page_tips)
            page += 1
            time.sleep(1)  # Be respectful
                
        except Exception:
            break
    
    return all_tips

def extract_tip_from_issue_link(link_element):
    """Extract TIP data from a GitHub issue link"""
    
    try:
        href = link_element.get('href', '')
        title_text = link_element.get_text(strip=True)
        
        if not href or '/issues/' not in href:
            return None
        
        # Extract TIP number from title
        tip_match = re.search(r'tip[-\s]?(\d+)', title_text, re.I)
        if not tip_match:
            return None
        
        tip_number = int(tip_match.group(1))
        
        # Create TIP object with minimal data from issues
        tip_data = {
            'id': f'TIP-{tip_number}',
            'number': tip_number,
            'title': title_text,
            'status': 'draft',  # Default for issues
            'author': 'Unknown',
            'created': '',
            'type': 'Standards Track',
            'category': 'Core',
            'url': f'https://github.com{href}',
            'file_url': f'https://github.com{href}',
            'protocol': 'tron',
            'summary': f"{title_text} - TIP {tip_number}",
            'source': 'https://github.com/tronprotocol/tips/issues'
        }
        
        return tip_data
        
    except Exception:
        return None

def fetch_tips_hybrid():
    """Hybrid approach: Combine markdown file scraping with Issues UI"""
    print("Starting hybrid TIP fetching...")
    print("Method 1: Scanning repository for markdown files (comprehensive historical data)")
    print("Method 2: Scanning Issues UI for newer/active TIPs")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    all_tips = {}  # Use dict to automatically handle duplicates by TIP number
    
    # Method 1: Get TIPs from repository markdown files (comprehensive)
    print("\n=== METHOD 1: Repository markdown files ===")
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
        
        print(f"Found {len(tip_numbers)} TIP markdown files in repository")
        
        # Fetch TIPs with threading
        tip_numbers = sorted(tip_numbers)
        successful_tips = []
        
        def fetch_batch(tip_nums):
            batch_results = []
            for tip_num in tip_nums:
                result = fetch_single_tip_markdown(tip_num, session)
                if result:
                    batch_results.append(result)
            return batch_results
        
        # Process in batches
        batch_size = 20
        for i in range(0, len(tip_numbers), batch_size):
            batch = tip_numbers[i:i+batch_size]
            print(f"Processing markdown batch {i//batch_size + 1}: TIPs {batch[0]}-{batch[-1]}")
            
            with ThreadPoolExecutor(max_workers=5) as executor:
                batch_tips = fetch_batch(batch)
                successful_tips.extend(batch_tips)
            
            time.sleep(1)
        
        # Add to all_tips dict
        for tip in successful_tips:
            all_tips[tip['number']] = tip
        
        print(f"Method 1 completed: {len(successful_tips)} TIPs from markdown files")
        
    except Exception as e:
        print(f"Method 1 failed: {e}")
    
    # Method 2: Get TIPs from Issues UI (newer/active)
    print("\n=== METHOD 2: GitHub Issues UI ===")
    try:
        issues_tips = fetch_tips_from_issues(session)
        
        # Merge with existing data (Issues data can override if more recent)
        new_from_issues = 0
        updated_from_issues = 0
        
        for tip in issues_tips:
            tip_num = tip['number']
            if tip_num not in all_tips:
                all_tips[tip_num] = tip
                new_from_issues += 1
            else:
                # Keep the markdown data but update status if issue provides newer info
                existing_tip = all_tips[tip_num]
                if not existing_tip.get('created') and tip.get('created'):
                    existing_tip['created'] = tip['created']
                    updated_from_issues += 1
        
        print(f"Method 2 completed: {new_from_issues} new TIPs, {updated_from_issues} updated from Issues UI")
        
    except Exception as e:
        print(f"Method 2 failed: {e}")
    
    # Convert back to list and sort
    final_tips = list(all_tips.values())
    final_tips.sort(key=lambda x: x.get('number', 0), reverse=True)
    
    print(f"\nHYBRID RESULT: {len(final_tips)} total unique TIPs")
    
    return final_tips

def save_tips_data(tips_data, output_file="data/tips.json"):
    """Save TIPs data to JSON file"""
    
    output_data = {
        "generated_at": int(time.time()),
        "generated_at_iso": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "count": len(tips_data),
        "protocol": "tron",
        "source": "https://github.com/tronprotocol/tips",
        "method": "Hybrid: Markdown files + Issues UI",
        "items": tips_data,
    }
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(tips_data)} TIPs to {output_file}")
    return output_file

if __name__ == "__main__":
    try:
        tips = fetch_tips_hybrid()
        
        if tips:
            # Save the data
            output_file = save_tips_data(tips)
            
            print(f"\nSUCCESS: Hybrid TIP scraping completed!")
            print(f"Total TIPs: {len(tips)}")
            
            # Show latest TIPs
            print(f"\nLatest 10 TIPs:")
            for tip in tips[:10]:
                created_display = tip['created'] if tip['created'] else 'No date'
                print(f"   TIP-{tip['number']}: {tip['title'][:60]}... (Created: {created_display}, Status: {tip['status']})")
            
            # Show TIP number range
            if tips:
                tip_numbers = [tip['number'] for tip in tips]
                print(f"\nTIP number range: TIP-{min(tip_numbers)} to TIP-{max(tip_numbers)}")
            
            # Show status distribution
            status_counts = {}
            for tip in tips:
                status = tip['status']
                status_counts[status] = status_counts.get(status, 0) + 1
            
            print(f"\nStatus distribution:")
            for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"   {status}: {count} TIPs")
            
            # Show creation date range
            dated_tips = [tip for tip in tips if tip.get('created') and tip['created'].strip()]
            if dated_tips:
                dates = [tip['created'] for tip in dated_tips]
                dates = [d for d in dates if re.match(r'\d{4}-\d{2}-\d{2}', d)]
                if dates:
                    dates.sort()
                    print(f"\nCreation date range: {dates[0]} to {dates[-1]}")
                    print(f"TIPs with creation dates: {len(dates)} out of {len(tips)}")
        else:
            print("FAILED: No TIPs extracted")
            
    except Exception as e:
        print(f"FAILED: Error during hybrid TIP scraping: {e}")
        import traceback
        traceback.print_exc()