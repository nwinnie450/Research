#!/usr/bin/env python3
"""
Fetch EIPs from https://eips.ethereum.org/all (no GitHub API)
"""
import json
import time
import requests
from bs4 import BeautifulSoup
import os

def fetch_eips():
    """Scrape EIPs from the official EIPs website"""
    print("Fetching EIPs from https://eips.ethereum.org/all...")
    
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
            
            total_processed = 0
            
            for table_idx, table in enumerate(tables):
                table_rows = table.find_all("tr")[1:]  # Skip header row
                default_status = table_status_map.get(table_idx, "Unknown")
                
                print(f"  Processing table {table_idx + 1} with {len(table_rows)} rows (default status: {default_status})")
                
                for i, tr in enumerate(table_rows):
                    try:
                        td = [c.get_text(strip=True) for c in tr.find_all("td")]
                        
                        # Basic columns: [Number, Title, Author] or [Number, Review ends, Title, Author]
                        if len(td) >= 3:
                            num_text = td[0].strip()
                            
                            # Skip empty rows
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
                            
                            # Get link from the number cell or title cell
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
                                continue  # Skip if not a valid number
                            
                            rows.append({
                                "number": eip_number,
                                "id": f"EIP-{eip_number}",
                                "title": title,
                                "author": author,
                                "type": "Standards Track",  # Default type
                                "category": "",  # Will be determined later if needed
                                "status": default_status,
                                "created": "",  # Would need individual page scraping
                                "url": link,
                                "file_url": link,
                                "protocol": "ethereum",
                                "summary": f"{title} - {default_status} EIP by {author}",
                                "source": URL,
                                "review_ends": review_ends,
                            })
                            
                            total_processed += 1
                            
                    except Exception as e:
                        print(f"  Warning: Error processing EIP row {table_idx}-{i}: {e}")
                        continue
            
            print(f"Successfully scraped {len(rows)} EIPs from {len(tables)} tables")
            
        else:
            print("Error: Could not find any EIPs tables on the page")
            return []
        
        # Sort by number (latest first)
        rows.sort(key=lambda x: x["number"], reverse=True)
        
        return rows
        
    except Exception as e:
        print(f"Error fetching EIPs: {e}")
        return []

def save_eips_data(eips_data, output_file="data/eips.json"):
    """Save EIPs data to JSON file"""
    
    out = {
        "generated_at": int(time.time()),
        "generated_at_iso": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "count": len(eips_data),
        "protocol": "ethereum",
        "source": "https://eips.ethereum.org/all",
        "items": eips_data,
    }
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(eips_data)} EIPs to {output_file}")
    return output_file

if __name__ == "__main__":
    eips = fetch_eips()
    if eips:
        save_eips_data(eips)
        print(f"SUCCESS: EIPs fetch completed successfully!")
        
        # Show sample of latest EIPs
        print("\nLatest 5 EIPs:")
        for eip in eips[:5]:
            print(f"  {eip['id']}: {eip['title']} ({eip['status']})")
        
        # Show status breakdown
        status_counts = {}
        for eip in eips:
            status = eip['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print(f"\nStatus breakdown:")
        for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {status}: {count} EIPs")
    else:
        print("FAILED: Failed to fetch EIPs")