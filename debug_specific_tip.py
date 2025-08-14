#!/usr/bin/env python3
"""
Debug script to check if TIP-4907 exists
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def check_tip_4907():
    token = os.getenv('GITHUB_TOKEN')
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'BlockchainResearchHub/1.0'
    }
    
    # Check if TIP-4907 exists
    url = "https://api.github.com/repos/tronprotocol/TIPs/contents/tip-4907.md"
    
    try:
        response = requests.get(url, headers=headers)
        print(f"TIP-4907 check: {response.status_code}")
        
        if response.status_code == 200:
            print("TIP-4907 EXISTS!")
        else:
            print("TIP-4907 does NOT exist")
            
        # Also check for any files that might be interpreted as TIP-4907
        base_url = "https://api.github.com/repos/tronprotocol/TIPs/contents"
        response = requests.get(base_url, headers=headers)
        
        if response.status_code == 200:
            files = response.json()
            
            print("\nFiles that might be confused for TIP-4907:")
            for file in files:
                if '4907' in file['name'] or file['name'].startswith('tip-49'):
                    print(f"- {file['name']}")
                    
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    check_tip_4907()