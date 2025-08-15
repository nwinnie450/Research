#!/usr/bin/env python3
"""
Fetch creation dates for the latest/most recent EIPs that users see first
"""
import json
import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_eip_creation_date(eip_url, eip_number):
    """Fetch creation date from individual EIP page"""
    try:
        r = requests.get(eip_url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Look for creation date in the metadata table
        table = soup.find('table')
        if table:
            for row in table.find_all('tr'):
                cells = row.find_all(['th', 'td'])
                if len(cells) >= 2:
                    header = cells[0].get_text(strip=True).lower()
                    value = cells[1].get_text(strip=True)
                    if 'created' in header:
                        return value
        
        # Fallback: look in YAML frontmatter
        content = soup.get_text()
        lines = content.split('\n')[:20]
        for line in lines:
            if line.strip().lower().startswith('created:'):
                return line.split(':', 1)[1].strip()
        
        return ""
        
    except Exception as e:
        print(f"  Warning: Could not fetch creation date for EIP-{eip_number}: {e}")
        return ""

def update_latest_eip_dates():
    """Update creation dates for the most recent EIPs"""
    print("Updating creation dates for latest EIPs that users see first...")
    
    # Load current EIPs data
    with open('data/eips.json', encoding='utf-8') as f:
        data = json.load(f)
    
    # Find EIPs without creation dates, focusing on recent ones
    eips_without_dates = [eip for eip in data['items'] if not eip.get('created') or not eip['created'].strip()]
    
    print(f"Found {len(eips_without_dates)} EIPs without creation dates")
    
    # Take the first 30 EIPs (which are the most recent due to sorting)
    eips_to_update = eips_without_dates[:30]
    print(f"Fetching creation dates for the {len(eips_to_update)} most recent EIPs...")
    
    # Fetch creation dates
    def fetch_date_wrapper(eip):
        created_date = fetch_eip_creation_date(eip['url'], eip['number'])
        if created_date:
            eip['created'] = created_date
            print(f"  SUCCESS: EIP-{eip['number']}: {created_date}")
            return True
        else:
            print(f"  FAILED: EIP-{eip['number']}: No creation date found")
            return False
    
    # Use threading for better performance
    successful_updates = 0
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_eip = {executor.submit(fetch_date_wrapper, eip): eip for eip in eips_to_update}
        
        for future in as_completed(future_to_eip):
            if future.result():
                successful_updates += 1
    
    print(f"\nSuccessfully updated {successful_updates} EIPs with creation dates")
    
    # Save updated data
    data['generated_at'] = int(time.time())
    data['generated_at_iso'] = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())
    
    with open('data/eips.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Show summary
    all_with_dates = sum(1 for eip in data['items'] if eip.get('created') and eip['created'].strip())
    print(f"\nSUMMARY:")
    print(f"Total EIPs with creation dates: {all_with_dates}/{data['count']} ({(all_with_dates/data['count']*100):.1f}%)")
    
    print(f"\nRecent EIPs now with creation dates:")
    recent_with_dates = [eip for eip in data['items'][:10] if eip.get('created') and eip['created'].strip()]
    for eip in recent_with_dates:
        print(f"  EIP-{eip['number']}: {eip['created']} - {eip['title'][:50]}...")

if __name__ == "__main__":
    update_latest_eip_dates()