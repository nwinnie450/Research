#!/usr/bin/env python3
"""
Quick verification script to check the specific TIPs mentioned by the user
"""
import json
import sys
import os

def verify_specific_tips():
    """Verify the specific TIPs that were showing 'Not available'"""
    
    print("=== VERIFYING SPECIFIC TIP CREATION DATES ===")
    
    # Load current TIP data
    data_file = 'data/tips.json'
    if not os.path.exists(data_file):
        print(f"ERROR: {data_file} not found.")
        return False
    
    with open(data_file, 'r', encoding='utf-8') as f:
        tip_data = json.load(f)
    
    tips = tip_data.get('items', [])
    
    # TIPs that were showing "Not available" according to user
    target_tips = [7951, 7702, 6963, 772]
    
    print("Checking TIPs that previously had 'Not available' creation dates:")
    print("-" * 80)
    
    all_fixed = True
    
    for tip_number in target_tips:
        # Find the TIP
        found_tip = None
        for tip in tips:
            if tip.get('number') == tip_number:
                found_tip = tip
                break
        
        if found_tip:
            created_date = found_tip.get('created', '')
            title = found_tip.get('title', 'Unknown Title')[:60]
            status = found_tip.get('status', 'Unknown')
            author = found_tip.get('author', 'Unknown')
            
            if created_date and created_date.strip() and created_date != 'Not available':
                print(f"TIP-{tip_number:>4}    {title:<60}    {status:<10}    {author:<25}    {created_date}")
            else:
                print(f"TIP-{tip_number:>4}    {title:<60}    {status:<10}    {author:<25}    STILL MISSING")
                all_fixed = False
        else:
            print(f"TIP-{tip_number:>4}    NOT FOUND IN DATA")
            all_fixed = False
    
    print("-" * 80)
    
    # Also show some TIPs that should have dates for comparison
    print("\nFor comparison, TIPs that already had creation dates:")
    comparison_tips = [4906, 3326, 1193, 1155, 745]
    
    for tip_number in comparison_tips:
        found_tip = None
        for tip in tips:
            if tip.get('number') == tip_number:
                found_tip = tip
                break
        
        if found_tip:
            created_date = found_tip.get('created', '')
            title = found_tip.get('title', 'Unknown Title')[:60]
            status = found_tip.get('status', 'Unknown')
            author = found_tip.get('author', 'Unknown')
            print(f"TIP-{tip_number:>4}    {title:<60}    {status:<10}    {author:<25}    {created_date}")
    
    print(f"\n=== SUMMARY ===")
    if all_fixed:
        print("[SUCCESS] All target TIPs now have creation dates!")
        print("The Streamlit app should now display creation dates instead of 'Not available'")
    else:
        print("[PARTIAL] Some TIPs still don't have creation dates")
    
    # Show overall stats
    tips_with_dates = len([tip for tip in tips if tip.get('created') and tip['created'].strip() and tip['created'] != 'Not available'])
    print(f"Total TIPs with creation dates: {tips_with_dates} out of {len(tips)}")
    
    return all_fixed

if __name__ == "__main__":
    success = verify_specific_tips()
    sys.exit(0 if success else 1)