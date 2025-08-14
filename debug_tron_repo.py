#!/usr/bin/env python3
"""
Debug script to check TRON repository structure
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def check_tron_repo():
    token = os.getenv('GITHUB_TOKEN')
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'BlockchainResearchHub/1.0'
    }
    
    base_url = "https://api.github.com/repos/tronprotocol/TIPs"
    
    # Check different possible paths
    paths_to_test = [
        "",  # Root directory
        "tip",  # Current config
        "tips", 
        "TIPs",
        "TIPS",
        "content",
        "contents"
    ]
    
    print("Testing TRON repository structure:")
    print("=" * 50)
    
    for path in paths_to_test:
        url = f"{base_url}/contents/{path}" if path else f"{base_url}/contents"
        
        try:
            response = requests.get(url, headers=headers)
            print(f"Path '{path}': {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"  - Found {len(data)} items")
                
                # Look for TIP files
                tip_files = [f for f in data if f['name'].lower().startswith('tip-') and f['name'].endswith('.md')]
                print(f"  - TIP files found: {len(tip_files)}")
                
                if tip_files:
                    print(f"  - Example files: {[f['name'] for f in tip_files[:3]]}")
            
        except Exception as e:
            print(f"Path '{path}': ERROR - {str(e)}")
        
        print()

if __name__ == "__main__":
    check_tron_repo()