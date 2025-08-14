#!/usr/bin/env python3
"""
Debug script to check TIP file format
"""
import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()

def check_tip_format():
    token = os.getenv('GITHUB_TOKEN')
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'BlockchainResearchHub/1.0'
    }
    
    # Check a specific TIP file
    url = "https://api.github.com/repos/tronprotocol/TIPs/contents/tip-721.md"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            file_data = response.json()
            content = base64.b64decode(file_data['content']).decode('utf-8')
            
            print("TIP-721 Content Structure:")
            print("=" * 50)
            print(content[:1000] + "..." if len(content) > 1000 else content)
            print("=" * 50)
            
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    check_tip_format()