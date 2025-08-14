#!/usr/bin/env python3
"""
Debug script to check TIP-4906 content specifically
"""
import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()

def check_tip_4906_content():
    token = os.getenv('GITHUB_TOKEN')
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'BlockchainResearchHub/1.0'
    }
    
    # Check TIP-4906 content
    url = "https://api.github.com/repos/tronprotocol/TIPs/contents/tip-4906.md"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            file_data = response.json()
            content = base64.b64decode(file_data['content']).decode('utf-8')
            
            print("TIP-4906 Content Analysis:")
            print("=" * 50)
            print("First 30 lines:")
            
            lines = content.split('\n')
            for i, line in enumerate(lines[:30]):
                print(f"{i+1:2}: {line}")
                
                # Look for tip field specifically
                if 'tip:' in line.lower():
                    print(f"    ^^^ FOUND TIP FIELD: {line.strip()}")
            
            print("=" * 50)
            
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    check_tip_4906_content()