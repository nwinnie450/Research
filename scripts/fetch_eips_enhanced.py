#!/usr/bin/env python3
"""
Enhanced EIP scraper that fetches creation dates from individual pages
"""
import json
import time
import requests
from bs4 import BeautifulSoup
import os
import random
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
        
        # Fallback: look in YAML frontmatter if table method fails
        # EIP pages sometimes have YAML metadata at the top
        content = soup.get_text()
        lines = content.split('\n')[:20]  # Check first 20 lines
        for line in lines:
            if line.strip().lower().startswith('created:'):
                return line.split(':', 1)[1].strip()
        
        return ""
        
    except Exception as e:
        print(f"  Warning: Could not fetch creation date for EIP-{eip_number}: {e}")
        return ""

def fetch_eips_enhanced():
    """Scrape EIPs with enhanced creation date fetching"""
    print("Fetching EIPs with enhanced creation date support...")
    
    URL = "https://eips.ethereum.org/all"
    
    try:
        r = requests.get(URL, timeout=30)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        
        rows = []
        tables = soup.find_all("table")
        
        if tables:
            print(f"Found {len(tables)} tables with EIPs data")
            
            # Status mapping for different tables
            table_status_map = {
                0: "Meta",        # Table 1: Meta EIPs
                1: "Final",       # Table 2: Final EIPs  
                2: "Last Call",   # Table 3: Last Call EIPs
                3: "Draft",       # Table 4: Draft EIPs
                4: "Draft",       # Table 5: More Draft EIPs
                5: "Final",       # Table 6: More Final EIPs
                6: "Withdrawn",   # Table 7: Withdrawn/Stagnant EIPs
            }
            
            # First pass: collect all EIP data
            all_eips = []
            
            for table_idx, table in enumerate(tables):
                table_rows = table.find_all("tr")[1:]  # Skip header row
                default_status = table_status_map.get(table_idx, "Unknown")
                
                print(f"  Processing table {table_idx + 1} with {len(table_rows)} rows (default status: {default_status})")
                
                for i, tr in enumerate(table_rows):
                    try:
                        td = [c.get_text(strip=True) for c in tr.find_all("td")]
                        
                        if len(td) >= 3:
                            num_text = td[0].strip()
                            
                            if not num_text or num_text == "":
                                continue
                            
                            # Handle different column layouts
                            if len(td) == 4:  # Has "Review ends" column
                                title = td[2].strip()
                                author = td[3].strip()
                                review_ends = td[1].strip()
                            else:  # Standard 3-column layout
                                title = td[1].strip()
                                author = td[2].strip()
                                review_ends = ""
                            
                            # Get link
                            link_elem = tr.find("a")
                            if link_elem and link_elem.get("href"):
                                link = link_elem["href"]
                                if not link.startswith("http"):
                                    link = f"https://eips.ethereum.org{link}"
                            else:
                                link = f"https://eips.ethereum.org/EIPS/eip-{num_text}"
                            
                            # Try to parse number
                            try:
                                eip_number = int(num_text)
                            except (ValueError, TypeError):
                                continue
                            
                            all_eips.append({
                                "number": eip_number,
                                "id": f"EIP-{eip_number}",
                                "title": title,
                                "author": author,
                                "type": "Standards Track",
                                "category": "",
                                "status": default_status,
                                "url": link,
                                "file_url": link,
                                "protocol": "ethereum",
                                "summary": f"{title} - {default_status} EIP by {author}",
                                "source": URL,
                                "review_ends": review_ends,
                                "created": ""  # Will be filled in next step
                            })
                            
                    except Exception as e:
                        print(f"  Warning: Error processing EIP row {table_idx}-{i}: {e}")
                        continue
            
            print(f"Collected {len(all_eips)} EIPs, now fetching creation dates...")
            
            # Second pass: fetch creation dates for a subset
            # Strategy: Get creation dates for first 25 from each status + random sampling
            eips_to_fetch_dates = []
            
            # Group by status
            by_status = {}
            for eip in all_eips:
                status = eip['status']
                if status not in by_status:
                    by_status[status] = []
                by_status[status].append(eip)
            
            # Select EIPs for date fetching
            for status, eips_list in by_status.items():
                # Take first 20 + 5 random from each status
                selected = eips_list[:20]
                if len(eips_list) > 20:
                    remaining = eips_list[20:]
                    selected.extend(random.sample(remaining, min(5, len(remaining))))
                eips_to_fetch_dates.extend(selected)
            
            print(f"Fetching creation dates for {len(eips_to_fetch_dates)} selected EIPs...")
            
            # Fetch creation dates with threading for better performance
            def fetch_date_wrapper(eip):
                created_date = fetch_eip_creation_date(eip['url'], eip['number'])
                eip['created'] = created_date
                if created_date:
                    print(f"  ✓ EIP-{eip['number']}: {created_date}")
                return eip
            
            # Use threading to speed up the process
            with ThreadPoolExecutor(max_workers=5) as executor:
                future_to_eip = {executor.submit(fetch_date_wrapper, eip): eip for eip in eips_to_fetch_dates}
                completed = 0
                
                for future in as_completed(future_to_eip):
                    completed += 1
                    if completed % 10 == 0:
                        print(f"  Progress: {completed}/{len(eips_to_fetch_dates)} creation dates fetched")
            
            # Update rows with the enhanced data
            eip_dict = {eip['number']: eip for eip in eips_to_fetch_dates}
            rows = []
            
            for eip in all_eips:
                if eip['number'] in eip_dict:
                    # Use enhanced version with creation date
                    rows.append(eip_dict[eip['number']])
                else:
                    # Use original version
                    rows.append(eip)
            
            print(f"Successfully enhanced {len(eips_to_fetch_dates)} EIPs with creation dates")
            
        else:
            print("No tables found")
            return
        
        # Sort by EIP number (descending)
        rows.sort(key=lambda x: x.get('number', 0), reverse=True)
        
        # Create output data
        output_data = {
            "generated_at": int(time.time()),
            "generated_at_iso": time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()),
            "count": len(rows),
            "protocol": "ethereum",
            "source": URL,
            "items": rows
        }
        
        # Save to file
        os.makedirs("data", exist_ok=True)
        output_file = "data/eips_enhanced.json"
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ SUCCESS: Enhanced EIPs data saved to {output_file}")
        print(f"📊 Total EIPs: {len(rows):,}")
        
        # Count how many have creation dates
        with_dates = sum(1 for eip in rows if eip.get('created'))
        print(f"📅 EIPs with creation dates: {with_dates:,} ({(with_dates/len(rows)*100):.1f}%)")
        
        # Show some examples
        print(f"\n📋 Sample with creation dates:")
        examples = [eip for eip in rows if eip.get('created')][:5]
        for eip in examples:
            print(f"   EIP-{eip['number']}: {eip['title'][:50]}... (Created: {eip['created']})")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        raise

if __name__ == "__main__":
    fetch_eips_enhanced()