#!/usr/bin/env python3
"""
Debug script to check number extraction logic
"""
import requests
import os
import re
import base64
from dotenv import load_dotenv

load_dotenv()

def debug_number_extraction():
    """Test the _extract_proposal_number logic"""
    
    def _extract_proposal_number(filename: str) -> int:
        """Extract proposal number from filename - same logic as service"""
        try:
            # Extract number from filename like "eip-1559.md" or "bip-0001.mediawiki"
            numbers = re.findall(r'\d+', filename)
            return int(numbers[0]) if numbers else 0
        except:
            return 0
    
    # Test with some TIP filenames
    test_files = [
        "tip-4906.md",
        "tip-3326.md", 
        "tip-1193.md",
        "tip-721.md"
    ]
    
    print("Testing number extraction:")
    for filename in test_files:
        number = _extract_proposal_number(filename)
        print(f"  {filename} -> {number}")
    
    # Now check what GitHub actually returns for the highest TIPs
    token = os.getenv('GITHUB_TOKEN')
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'BlockchainResearchHub/1.0'
    }
    
    print("\nChecking actual GitHub files:")
    
    # Get repository contents
    url = "https://api.github.com/repos/tronprotocol/TIPs/contents"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            files = response.json()
            
            # Extract and sort TIP numbers
            tip_files = []
            for file in files:
                if file['name'].startswith('tip-') and file['name'].endswith('.md'):
                    number = _extract_proposal_number(file['name'])
                    tip_files.append({
                        'filename': file['name'],
                        'number': number,
                        'path': file['path']
                    })
            
            # Sort by number descending
            tip_files.sort(key=lambda x: x['number'], reverse=True)
            
            print(f"Top 10 TIP files by number:")
            for tip in tip_files[:10]:
                print(f"  {tip['filename']} -> Number: {tip['number']}")
            
            # Check if TIP-4907 actually exists in any form
            for file in files:
                if '4907' in file['name']:
                    print(f"\nFound file with '4907': {file['name']}")
                    
                    # Get the content to see what's inside
                    content_url = f"https://api.github.com/repos/tronprotocol/TIPs/contents/{file['path']}"
                    content_response = requests.get(content_url, headers=headers)
                    
                    if content_response.status_code == 200:
                        file_data = content_response.json()
                        content = base64.b64decode(file_data['content']).decode('utf-8')
                        
                        # Look for 'tip:' field in content
                        for line in content.split('\n')[:20]:
                            if line.strip().startswith('tip:'):
                                print(f"  Content tip field: {line.strip()}")
                                break
                        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    debug_number_extraction()