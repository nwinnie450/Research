#!/usr/bin/env python3
"""
Enhanced TIP scraper to get all TRON TIPs from GitHub repository + recent issues/PRs
"""
import json
import time
import requests
from bs4 import BeautifulSoup
import re
import os
from datetime import datetime, timezone

def parse_tip_content(content, tip_number):
    """Parse TIP content to extract metadata"""
    lines = content.split('\n')
    
    tip_data = {
        'title': f'TIP-{tip_number}',
        'status': 'Unknown', 
        'author': 'Unknown',
        'created': '',
        'type': 'Unknown',
        'category': 'Unknown'
    }
    
    # Look for YAML frontmatter or structured metadata
    in_frontmatter = False
    
    for i, line in enumerate(lines[:50]):  # Check first 50 lines
        line = line.strip()
        
        # Check for YAML frontmatter markers
        if line == '---' and i == 0:
            in_frontmatter = True
            continue
        elif line == '---' and in_frontmatter:
            break
        elif line.startswith('```') and i == 0:
            in_frontmatter = True
            continue
        elif line.startswith('```') and in_frontmatter:
            break
        
        # Parse metadata (both YAML and other formats)
        if ':' in line and ('tip' in line.lower() or 'title' in line.lower() or 'status' in line.lower() or 'author' in line.lower() or 'created' in line.lower()):
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
                elif 'created' in key or 'date' in key:
                    tip_data['created'] = value
                elif 'type' in key:
                    tip_data['type'] = value
                elif 'category' in key:
                    tip_data['category'] = value
        
        # Also look for markdown-style headers
        if line.startswith('# ') and 'TIP-' in line:
            tip_data['title'] = line[2:].strip()
    
    return tip_data

def fetch_single_tip(tip_number, session):
    """Fetch a single TIP's metadata from the repository"""
    try:
        # Try multiple URL patterns for TIP files
        urls_to_try = [
            f"https://raw.githubusercontent.com/tronprotocol/tips/master/tip-{tip_number}.md",
            f"https://raw.githubusercontent.com/tronprotocol/TIPs/master/tip-{tip_number}.md",
            f"https://raw.githubusercontent.com/tronprotocol/tips/master/tip-{tip_number:03d}.md",
            f"https://raw.githubusercontent.com/tronprotocol/TIPs/master/tip-{tip_number:03d}.md"
        ]
        
        content = None
        successful_url = None
        
        for url in urls_to_try:
            try:
                r = session.get(url, timeout=10)
                if r.status_code == 200:
                    content = r.text
                    successful_url = url
                    break
            except:
                continue
        
        if not content:
            return None
        
        # Parse the content
        tip_data = parse_tip_content(content, tip_number)
        
        # Create the full TIP object
        tip_object = {
            'title': tip_data['title'],
            'status': tip_data['status'],
            'author': tip_data['author'],
            'created': tip_data['created'] if tip_data['created'] else 'Unknown',
            'type': tip_data['type'],
            'category': tip_data['category'],
            'id': f'TIP-{tip_number}',
            'number': tip_number,
            'url': successful_url.replace('raw.githubusercontent.com', 'github.com').replace('/master/', '/blob/master/'),
            'file_url': successful_url.replace('raw.githubusercontent.com', 'github.com').replace('/master/', '/blob/master/'),
            'protocol': 'tron',
            'summary': f"{tip_data['title']} - {tip_data['status']} TIP by {tip_data['author']}",
            'source': 'https://github.com/tronprotocol/tips'
        }
        
        return tip_object
        
    except Exception as e:
        return None

def get_issue_creation_date(issue_url, session):
    """Get the actual creation date from a GitHub issue"""
    try:
        r = session.get(issue_url, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Look for issue metadata or creation date in various formats
        # GitHub shows creation date in relative time elements
        time_elements = soup.find_all('relative-time')
        if time_elements:
            # Get the datetime attribute from the first relative-time element
            datetime_attr = time_elements[0].get('datetime')
            if datetime_attr:
                # Convert ISO datetime to YYYY-MM-DD format
                from datetime import datetime
                dt = datetime.fromisoformat(datetime_attr.replace('Z', '+00:00'))
                return dt.strftime('%Y-%m-%d')
        
        # Alternative: look for timestamp in the page
        for element in soup.find_all(['time', 'span'], class_=True):
            if 'datetime' in element.attrs:
                datetime_attr = element['datetime']
                dt = datetime.fromisoformat(datetime_attr.replace('Z', '+00:00'))
                return dt.strftime('%Y-%m-%d')
        
        # Look for date patterns in text content
        date_pattern = r'(\d{4}-\d{2}-\d{2})'
        page_text = soup.get_text()
        date_matches = re.findall(date_pattern, page_text)
        if date_matches:
            # Return the most recent looking date
            dates = sorted(date_matches, reverse=True)
            return dates[0]
            
    except Exception as e:
        print(f"  Warning: Could not get creation date from {issue_url}: {e}")
    
    return None

def fetch_recent_tip_issues():
    """Fetch recent TIP proposals from GitHub issues and PRs with accurate dates"""
    print("Fetching recent TIP proposals from GitHub issues/PRs...")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    recent_tips = []
    
    # Known recent TIP issues with their issue numbers for more accurate fetching
    known_recent_tips = [
        {'number': 7951, 'issue': 785, 'title': 'TIP-7951: Precompile for secp256r1 Curve Support'},
        {'number': 7702, 'issue': None, 'title': 'TIP-7702: Add a new tx type that permanently sets the code for an EOA'},
        {'number': 6963, 'issue': None, 'title': 'TIP-6963: Multi Injected Provider Discovery'},
        {'number': 6780, 'issue': None, 'title': 'TIP-6780: SELFDESTRUCT only in same transaction'},
        {'number': 772, 'issue': 772, 'title': 'TIP-772: SRs produce blocks strictly in descending order of votes'},
        {'number': 767, 'issue': None, 'title': 'TIP-767: Transitioning proposal expire time configuration to Chain Governance'}
    ]
    
    try:
        # First, try to get accurate dates for known recent TIPs
        print("Getting accurate dates for known recent TIPs...")
        for tip_info in known_recent_tips:
            tip_number = tip_info['number']
            issue_number = tip_info.get('issue')
            title = tip_info['title']
            
            # Try to get the issue creation date
            created_date = '2025-01-01'  # Default fallback
            
            if issue_number:
                issue_url = f"https://github.com/tronprotocol/TIPs/issues/{issue_number}"
                actual_date = get_issue_creation_date(issue_url, session)
                if actual_date:
                    created_date = actual_date
                    print(f"  TIP-{tip_number}: Found creation date {created_date}")
            
            tip_object = {
                'title': title,
                'status': 'Draft',
                'author': 'Unknown',
                'created': created_date,
                'type': 'Proposal',
                'category': 'Enhancement',
                'id': f'TIP-{tip_number}',
                'number': tip_number,
                'url': f"https://github.com/tronprotocol/TIPs/issues/{issue_number}" if issue_number else f"https://github.com/tronprotocol/TIPs/issues",
                'file_url': f"https://github.com/tronprotocol/TIPs/issues/{issue_number}" if issue_number else f"https://github.com/tronprotocol/TIPs/issues",
                'protocol': 'tron',
                'summary': f"{title} - Draft TIP proposal",
                'source': 'https://github.com/tronprotocol/TIPs/issues'
            }
            
            recent_tips.append(tip_object)
        
        # Also scrape the issues page for any additional TIPs we might have missed
        print("Scanning issues page for additional TIPs...")
        issues_url = "https://github.com/tronprotocol/TIPs/issues"
        r = session.get(issues_url, timeout=30)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Find issue links that we haven't already processed
        existing_numbers = {tip['number'] for tip in recent_tips}
        
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            # Look for TIP proposals in recent issues
            if '/issues/' in href and ('TIP-' in text or 'Proposal:' in text):
                tip_match = re.search(r'TIP-(\d+)', text)
                if tip_match:
                    tip_number = int(tip_match.group(1))
                    
                    # Skip if we already have this TIP
                    if tip_number in existing_numbers:
                        continue
                    
                    # Extract issue number from URL
                    issue_match = re.search(r'/issues/(\d+)', href)
                    issue_number = int(issue_match.group(1)) if issue_match else None
                    
                    # Get issue creation date
                    created_date = '2024-01-01'  # Default
                    issue_url = f"https://github.com{href}" if href.startswith('/') else href
                    
                    actual_date = get_issue_creation_date(issue_url, session)
                    if actual_date:
                        created_date = actual_date
                        print(f"  TIP-{tip_number}: Found creation date {created_date}")
                    
                    tip_object = {
                        'title': text,
                        'status': 'Draft',
                        'author': 'Unknown',
                        'created': created_date,
                        'type': 'Proposal',
                        'category': 'Enhancement',
                        'id': f'TIP-{tip_number}',
                        'number': tip_number,
                        'url': issue_url,
                        'file_url': issue_url,
                        'protocol': 'tron',
                        'summary': f"{text} - Draft TIP proposal",
                        'source': 'https://github.com/tronprotocol/TIPs/issues'
                    }
                    
                    recent_tips.append(tip_object)
        
        print(f"Found {len(recent_tips)} recent TIP proposals from issues")
        
    except Exception as e:
        print(f"Error fetching recent issues: {e}")
    
    return recent_tips

def fetch_tips_enhanced():
    """Fetch all TRON TIPs with enhanced scraper including recent issues"""
    print("=" * 60)
    print("ENHANCED TRON TIPS SCRAPER")
    print("=" * 60)
    print("Fetching from:")
    print("1. Main repository (merged TIPs)")
    print("2. Recent GitHub issues/PRs (draft TIPs)")
    print()
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    all_tips = []
    
    # 1. Get TIPs from main repository
    print("Phase 1: Fetching TIPs from main repository...")
    
    # Try to get TIP numbers from repository listing
    try:
        repo_urls = [
            'https://github.com/tronprotocol/tips',
            'https://github.com/tronprotocol/TIPs'
        ]
        
        tip_numbers = set()
        for repo_url in repo_urls:
            try:
                r = session.get(repo_url, timeout=30)
                r.raise_for_status()
                soup = BeautifulSoup(r.text, 'html.parser')
                
                # Extract TIP numbers from file links
                for link in soup.find_all('a', href=True):
                    href = link.get('href', '')
                    match = re.search(r'tip-(\d+)\.md', href)
                    if match:
                        tip_numbers.add(int(match.group(1)))
                
                if tip_numbers:
                    print(f"Found {len(tip_numbers)} TIP files in {repo_url}")
                    break
                    
            except Exception as e:
                print(f"Error accessing {repo_url}: {e}")
                continue
        
        if not tip_numbers:
            print("Repository listing failed, trying sequential approach...")
            tip_numbers = set(range(1, 800))  # Extended range to catch recent TIPs
        
    except Exception as e:
        print(f"Error getting repository listing: {e}")
        tip_numbers = set(range(1, 800))
    
    tip_numbers = sorted(tip_numbers, reverse=True)  # Start with latest numbers
    print(f"Attempting to fetch {len(tip_numbers)} TIPs from repository...")
    
    # Fetch repository TIPs
    for i, tip_num in enumerate(tip_numbers):
        result = fetch_single_tip(tip_num, session)
        if result:
            all_tips.append(result)
            
        # Progress indicator
        if (i + 1) % 50 == 0:
            print(f"  Repository progress: {len(all_tips)} TIPs fetched from {i + 1} attempts...")
            
        # Be nice to the server
        if i % 20 == 0:
            time.sleep(0.5)
    
    print(f"Phase 1 complete: {len(all_tips)} TIPs from repository")
    
    # 2. Get recent TIP proposals from issues/PRs
    print("\nPhase 2: Fetching recent TIP proposals from issues...")
    recent_tips = fetch_recent_tip_issues()
    
    # Merge recent tips, avoiding duplicates
    for recent_tip in recent_tips:
        # Check if we already have this TIP number
        existing_numbers = {tip['number'] for tip in all_tips}
        if recent_tip['number'] not in existing_numbers:
            all_tips.append(recent_tip)
            print(f"  Added new TIP from issues: {recent_tip['id']}")
    
    print(f"Phase 2 complete: Added {len([t for t in recent_tips if t['number'] not in {tip['number'] for tip in all_tips[:-len(recent_tips)]}])} new TIPs from issues")
    
    # Sort by TIP number (descending for latest first)
    all_tips.sort(key=lambda x: x.get('number', 0), reverse=True)
    
    print(f"\nTotal TIPs collected: {len(all_tips)}")
    
    # Create output data
    output_data = {
        'generated_at': int(time.time()),
        'generated_at_iso': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()),
        'count': len(all_tips),
        'protocol': 'tron',
        'source': 'https://github.com/tronprotocol/tips + https://github.com/tronprotocol/TIPs/issues',
        'items': all_tips
    }
    
    # Save to file
    os.makedirs('data', exist_ok=True)
    output_file = 'data/tips.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n" + "=" * 60)
    print("SUCCESS: Enhanced TIPs data saved!")
    print("=" * 60)
    print(f"Output file: {output_file}")
    print(f"Total TIPs: {len(all_tips):,}")
    
    # Show latest TIPs
    if all_tips:
        print(f"\nLatest TIPs found:")
        for tip in all_tips[:10]:
            created_display = tip['created'] if tip['created'] != 'Unknown' else '(date unknown)'
            print(f"   {tip['id']}: {tip['title'][:60]}...")
            print(f"      Status: {tip['status']}, Created: {created_display}")
        
        # Show TIP number range
        tip_numbers_found = [tip['number'] for tip in all_tips]
        print(f"\nTIP number range: TIP-{min(tip_numbers_found)} to TIP-{max(tip_numbers_found)}")
        
        # Show status distribution
        status_counts = {}
        draft_count = 0
        for tip in all_tips:
            status = tip['status']
            status_counts[status] = status_counts.get(status, 0) + 1
            if status.lower() in ['draft', 'idea', 'open']:
                draft_count += 1
        
        print(f"\nStatus distribution:")
        for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {status}: {count} TIPs")
        
        print(f"\nTotal draft TIPs: {draft_count}")
        
        # Show recent drafts specifically
        recent_drafts = [tip for tip in all_tips if tip['status'].lower() in ['draft', 'idea', 'open'] and tip['number'] > 700]
        if recent_drafts:
            print(f"\nRecent draft TIPs (TIP-700+):")
            for tip in recent_drafts:
                print(f"   {tip['id']}: {tip['title'][:50]}... (Created: {tip['created']})")

if __name__ == "__main__":
    fetch_tips_enhanced()