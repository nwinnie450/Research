#!/usr/bin/env python3
"""
Fetch TIPs from GitHub Issues UI (GPT-5 suggested approach)
This scraper uses GitHub's Issues interface to get comprehensive TIP data
"""
import json
import time
import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urljoin, urlparse, parse_qs

def fetch_tips_from_issues():
    """Scrape TIPs from GitHub Issues UI"""
    print("Fetching TIPs from GitHub Issues UI...")
    print("This approach provides comprehensive data including all TIP statuses")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    all_tips = []
    page = 1
    
    # Base URL for TIP issues (sorted by creation date, descending)
    base_url = "https://github.com/tronprotocol/tips/issues"
    
    while True:
        try:
            # Build URL for current page
            params = {
                'q': 'is:issue',
                'sort': 'created-desc',
                'page': page
            }
            
            # Construct URL manually to ensure proper formatting
            url = f"{base_url}?q=is%3Aissue&sort=created-desc&page={page}"
            
            print(f"Fetching page {page}: {url}")
            
            response = session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find issue rows using multiple selectors to be robust
            issue_rows = []
            
            # Try different selectors that GitHub might use
            selectors_to_try = [
                'div[aria-label="Issues"] div[role="row"]',
                'div.Box-row',
                'div.js-issue-row',
                '.Box-row',
                '[data-hovercard-type="issue"]'
            ]
            
            for selector in selectors_to_try:
                issue_rows = soup.select(selector)
                if issue_rows:
                    print(f"  Found {len(issue_rows)} issue rows using selector: {selector}")
                    break
            
            # Fallback: look for any links that contain TIP numbers
            if not issue_rows:
                print("  Using fallback: searching for TIP links")
                issue_links = soup.find_all('a', href=True)
                tip_links = []
                for link in issue_links:
                    href = link.get('href', '')
                    if '/issues/' in href and ('tip' in link.get_text().lower() or re.search(r'tip[-\s]?\d+', link.get_text(), re.I)):
                        tip_links.append(link)
                
                if tip_links:
                    issue_rows = tip_links
                    print(f"  Found {len(issue_rows)} TIP issue links")
            
            if not issue_rows:
                print(f"  No issues found on page {page}, stopping")
                break
            
            page_tips = []
            
            for i, row in enumerate(issue_rows):
                try:
                    tip_data = extract_tip_from_issue_row(row, session)
                    if tip_data:
                        page_tips.append(tip_data)
                        print(f"  Extracted: {tip_data['id']} - {tip_data['title'][:50]}...")
                
                except Exception as e:
                    print(f"  Error processing issue row {i+1}: {e}")
                    continue
            
            if not page_tips:
                print(f"  No valid TIPs found on page {page}, stopping")
                break
            
            all_tips.extend(page_tips)
            print(f"  Page {page} completed: {len(page_tips)} TIPs extracted")
            
            # Check if there's a next page
            next_page_link = soup.find('a', {'aria-label': 'Next Page'}) or soup.find('a', string='Next')
            if not next_page_link:
                print("  No next page found, stopping")
                break
            
            page += 1
            
            # Be respectful to GitHub's servers
            time.sleep(2)
            
            # Safety limit to prevent infinite loops
            if page > 50:
                print("  Reached page limit (50), stopping")
                break
                
        except Exception as e:
            print(f"  Error fetching page {page}: {e}")
            break
    
    print(f"\nSuccessfully extracted {len(all_tips)} TIPs from GitHub Issues")
    
    # Remove duplicates based on TIP number
    unique_tips = {}
    for tip in all_tips:
        tip_num = tip.get('number')
        if tip_num and (tip_num not in unique_tips or len(tip['title']) > len(unique_tips[tip_num]['title'])):
            unique_tips[tip_num] = tip
    
    final_tips = list(unique_tips.values())
    final_tips.sort(key=lambda x: x.get('number', 0), reverse=True)
    
    print(f"After deduplication: {len(final_tips)} unique TIPs")
    
    return final_tips

def extract_tip_from_issue_row(row_element, session):
    """Extract TIP data from a GitHub issue row element"""
    
    try:
        # Find the issue link
        issue_link = None
        
        # Try different ways to find the issue link
        if row_element.name == 'a':
            issue_link = row_element
        else:
            issue_link = row_element.find('a', href=True)
        
        if not issue_link:
            return None
        
        href = issue_link.get('href', '')
        if not href or '/issues/' not in href:
            return None
        
        # Get issue title and number
        title_text = issue_link.get_text(strip=True)
        
        # Extract TIP number from title
        tip_number = None
        tip_match = re.search(r'tip[-\s]?(\d+)', title_text, re.I)
        if tip_match:
            tip_number = int(tip_match.group(1))
        else:
            # Try to extract from URL
            issue_match = re.search(r'/issues/(\d+)', href)
            if issue_match:
                # Use issue number as fallback
                issue_num = int(issue_match.group(1))
                # Try to map issue number to TIP number from title
                digit_match = re.search(r'(\d+)', title_text)
                if digit_match:
                    tip_number = int(digit_match.group(1))
                else:
                    tip_number = issue_num
        
        if not tip_number:
            return None
        
        # Get issue status (open/closed)
        status = 'draft'  # Default
        
        # Look for status indicators in the row
        status_indicators = row_element.find_all(['span', 'div'], class_=True)
        for indicator in status_indicators:
            classes = ' '.join(indicator.get('class', []))
            text = indicator.get_text(strip=True).lower()
            
            if 'open' in classes or 'open' in text:
                status = 'draft'
            elif 'closed' in classes or 'closed' in text:
                status = 'closed'
        
        # Try to get more details from the issue page
        issue_url = urljoin('https://github.com', href)
        
        # Get creation date and author from the row if possible
        created_date = ''
        author = 'Unknown'
        
        # Look for time elements or date indicators
        time_elements = row_element.find_all(['time', 'relative-time'])
        for time_elem in time_elements:
            datetime_attr = time_elem.get('datetime') or time_elem.get('title')
            if datetime_attr:
                created_date = datetime_attr.split('T')[0]  # Get just the date part
                break
        
        # Look for author information
        author_links = row_element.find_all('a', href=lambda x: x and '/user/' in str(x) or x and x.startswith('/'))
        for author_link in author_links:
            author_text = author_link.get_text(strip=True)
            if author_text and author_text != title_text:
                author = author_text
                break
        
        # Create TIP object
        tip_data = {
            'id': f'TIP-{tip_number}',
            'number': tip_number,
            'title': title_text,
            'status': status,
            'author': author,
            'created': created_date,
            'type': 'Standards Track',  # Default
            'category': 'Core',  # Default
            'url': issue_url,
            'file_url': issue_url,
            'protocol': 'tron',
            'summary': f"{title_text} - TIP {tip_number}",
            'source': 'https://github.com/tronprotocol/tips/issues'
        }
        
        return tip_data
        
    except Exception as e:
        print(f"    Error extracting TIP data: {e}")
        return None

def save_tips_data(tips_data, output_file="data/tips.json"):
    """Save TIPs data to JSON file"""
    
    output_data = {
        "generated_at": int(time.time()),
        "generated_at_iso": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "count": len(tips_data),
        "protocol": "tron",
        "source": "https://github.com/tronprotocol/tips/issues",
        "method": "GitHub Issues UI scraping",
        "items": tips_data,
    }
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\nSaved {len(tips_data)} TIPs to {output_file}")
    return output_file

if __name__ == "__main__":
    try:
        tips = fetch_tips_from_issues()
        
        if tips:
            # Save the data
            output_file = save_tips_data(tips)
            
            print(f"\nSUCCESS: TIP Issues scraping completed!")
            print(f"Total TIPs extracted: {len(tips)}")
            
            # Show latest TIPs
            print(f"\nLatest 10 TIPs:")
            for tip in tips[:10]:
                created_display = tip['created'] if tip['created'] else 'Unknown date'
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
        else:
            print("FAILED: No TIPs extracted from GitHub Issues")
            
    except Exception as e:
        print(f"FAILED: Error during TIP Issues scraping: {e}")
        import traceback
        traceback.print_exc()