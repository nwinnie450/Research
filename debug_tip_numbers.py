#!/usr/bin/env python3
"""
Debug script to check actual TIP numbers in repository
"""
import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

def check_latest_tips():
    token = os.getenv('GITHUB_TOKEN')
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'BlockchainResearchHub/1.0'
    }
    
    url = "https://api.github.com/repos/tronprotocol/TIPs/contents"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            files = response.json()
            
            # Extract TIP numbers
            tip_numbers = []
            for file in files:
                if file['name'].startswith('tip-') and file['name'].endswith('.md'):
                    # Extract number from filename
                    match = re.search(r'tip-(\d+)\.md', file['name'])
                    if match:
                        tip_numbers.append(int(match.group(1)))
            
            # Sort to see the range
            tip_numbers.sort()
            
            print(f"Total TIP files: {len(tip_numbers)}")
            print(f"Lowest TIP number: {min(tip_numbers) if tip_numbers else 'None'}")
            print(f"Highest TIP number: {max(tip_numbers) if tip_numbers else 'None'}")
            print(f"Latest 10 TIPs: {sorted(tip_numbers, reverse=True)[:10]}")
            print(f"First 10 TIPs: {sorted(tip_numbers)[:10]}")
            
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    check_latest_tips()