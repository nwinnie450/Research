#!/usr/bin/env python3
"""
Comprehensive EIP creation date fetcher
Fetches creation dates for EIPs across ALL statuses, prioritizing by EIP number (newer = higher priority)
"""
import json
import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_eip_creation_date(eip_url, eip_number):
    """Fetch creation date from individual EIP page"""
    try:
        r = requests.get(eip_url, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Method 1: Look for creation date in the metadata table
        table = soup.find('table')
        if table:
            for row in table.find_all('tr'):
                cells = row.find_all(['th', 'td'])
                if len(cells) >= 2:
                    header = cells[0].get_text(strip=True).lower()
                    value = cells[1].get_text(strip=True)
                    if 'created' in header:
                        return value
        
        # Method 2: Look in YAML frontmatter
        content = soup.get_text()
        lines = content.split('\n')[:25]  # Check first 25 lines
        for line in lines:
            line_lower = line.strip().lower()
            if line_lower.startswith('created:'):
                return line.split(':', 1)[1].strip()
            elif 'created:' in line_lower:
                # Handle cases like "created: 2024-01-01"
                parts = line.split(':')
                for i, part in enumerate(parts):
                    if 'created' in part.lower() and i + 1 < len(parts):
                        return parts[i + 1].strip()
        
        # Method 3: Look for date patterns in first few paragraphs
        paragraphs = soup.find_all('p')[:5]
        for p in paragraphs:
            text = p.get_text()
            if 'created' in text.lower():
                import re
                # Look for date patterns like 2024-01-01 or January 1, 2024
                date_pattern = r'\d{4}-\d{2}-\d{2}'
                match = re.search(date_pattern, text)
                if match:
                    return match.group(0)
        
        return ""
        
    except Exception as e:
        print(f"  Warning: Could not fetch creation date for EIP-{eip_number}: {e}")
        return ""

def update_comprehensive_eip_dates():
    """Update creation dates for EIPs across all statuses, prioritizing by EIP number"""
    print("Comprehensive EIP creation date update - covering ALL statuses...")
    
    # Load current EIPs data
    with open('data/eips.json', encoding='utf-8') as f:
        data = json.load(f)
    
    # Find EIPs without creation dates
    eips_without_dates = [eip for eip in data['items'] if not eip.get('created') or not eip['created'].strip()]
    
    print(f"Found {len(eips_without_dates)} EIPs without creation dates")
    
    # Sort by EIP number (descending) - higher numbers = newer = higher priority
    eips_without_dates.sort(key=lambda x: x.get('number', 0), reverse=True)
    
    # Group by status to understand what we're updating
    by_status = {}
    for eip in eips_without_dates:
        status = eip.get('status', 'Unknown')
        if status not in by_status:
            by_status[status] = []
        by_status[status].append(eip)
    
    print(f"\nEIPs without dates by status:")
    for status, eips_list in by_status.items():
        print(f"  {status}: {len(eips_list)} EIPs")
    
    # Select EIPs to update - prioritize by number and ensure good coverage across statuses
    eips_to_update = []
    
    # Strategy: Take top EIPs by number from each status
    max_per_status = 25  # Reasonable limit per status
    for status, eips_list in by_status.items():
        # Take the highest numbered EIPs from each status
        selected = eips_list[:max_per_status]
        eips_to_update.extend(selected)
        print(f"  Selected {len(selected)} {status} EIPs for update (highest numbers: EIP-{selected[0]['number']} to EIP-{selected[-1]['number']})")
    
    # Remove duplicates and sort by number
    seen_numbers = set()
    unique_eips = []
    for eip in eips_to_update:
        if eip['number'] not in seen_numbers:
            unique_eips.append(eip)
            seen_numbers.add(eip['number'])
    
    eips_to_update = unique_eips
    eips_to_update.sort(key=lambda x: x.get('number', 0), reverse=True)
    
    print(f"\nFetching creation dates for {len(eips_to_update)} EIPs across all statuses...")
    print(f"Range: EIP-{eips_to_update[0]['number']} (newest) to EIP-{eips_to_update[-1]['number']} (oldest in selection)")
    
    # Fetch creation dates with progress tracking
    def fetch_date_wrapper(eip):
        created_date = fetch_eip_creation_date(eip['url'], eip['number'])
        if created_date:
            eip['created'] = created_date
            print(f"  ✓ EIP-{eip['number']} ({eip['status']}): {created_date}")
            return True
        else:
            print(f"  ✗ EIP-{eip['number']} ({eip['status']}): No date found")
            return False
    
    # Use threading for better performance
    successful_updates = 0
    failed_updates = 0
    
    with ThreadPoolExecutor(max_workers=6) as executor:
        future_to_eip = {executor.submit(fetch_date_wrapper, eip): eip for eip in eips_to_update}
        
        completed = 0
        for future in as_completed(future_to_eip):
            completed += 1
            if future.result():
                successful_updates += 1
            else:
                failed_updates += 1
            
            if completed % 20 == 0:
                print(f"  Progress: {completed}/{len(eips_to_update)} completed")
    
    print(f"\nUpdate completed:")
    print(f"  ✓ Successfully updated: {successful_updates}")
    print(f"  ✗ Failed to update: {failed_updates}")
    
    # Save updated data
    data['generated_at'] = int(time.time())
    data['generated_at_iso'] = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())
    
    with open('data/eips.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Show comprehensive summary
    all_with_dates = sum(1 for eip in data['items'] if eip.get('created') and eip['created'].strip())
    print(f"\nFINAL SUMMARY:")
    print(f"Total EIPs with creation dates: {all_with_dates}/{data['count']} ({(all_with_dates/data['count']*100):.1f}%)")
    
    # Show by status
    print(f"\nCreation date coverage by status:")
    all_by_status = {}
    with_dates_by_status = {}
    
    for eip in data['items']:
        status = eip.get('status', 'Unknown')
        if status not in all_by_status:
            all_by_status[status] = 0
            with_dates_by_status[status] = 0
        all_by_status[status] += 1
        if eip.get('created') and eip['created'].strip():
            with_dates_by_status[status] += 1
    
    for status in sorted(all_by_status.keys()):
        total = all_by_status[status]
        with_dates = with_dates_by_status[status]
        percentage = (with_dates / total * 100) if total > 0 else 0
        print(f"  {status}: {with_dates}/{total} ({percentage:.1f}%)")
    
    # Show examples from each status
    print(f"\nRecent EIPs with creation dates by status:")
    for status in ['Draft', 'Final', 'Last Call', 'Meta', 'Withdrawn']:
        status_eips = [eip for eip in data['items'] if eip.get('status') == status and eip.get('created') and eip['created'].strip()]
        if status_eips:
            # Show highest numbered (most recent) from this status
            status_eips.sort(key=lambda x: x.get('number', 0), reverse=True)
            eip = status_eips[0]
            print(f"  {status}: EIP-{eip['number']} ({eip['created']}) - {eip['title'][:50]}...")

if __name__ == "__main__":
    update_comprehensive_eip_dates()