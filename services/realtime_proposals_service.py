"""
Real-Time Blockchain Proposals Service
Fetches live improvement proposals using GitHub API
"""
import requests
import pandas as pd
import streamlit as st
import os
import re
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import base64

class RealtimeProposalsService:
    """Service for fetching real-time blockchain improvement proposals"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = 10
        
        # GitHub API authentication with multiple fallback methods
        self.github_token = None
        
        # Try multiple ways to get the token
        try:
            # Method 1: Direct secrets access
            if hasattr(st, 'secrets') and hasattr(st.secrets, 'GITHUB_TOKEN'):
                self.github_token = st.secrets.GITHUB_TOKEN
                st.info(f"🔍 Debug: Token from st.secrets.GITHUB_TOKEN: {self.github_token[:20]}...")
            # Method 2: Dictionary-style access
            elif hasattr(st, 'secrets') and 'GITHUB_TOKEN' in st.secrets:
                self.github_token = st.secrets['GITHUB_TOKEN']
                st.info(f"🔍 Debug: Token from st.secrets['GITHUB_TOKEN']: {self.github_token[:20]}...")
            # Method 3: Environment variable
            elif os.getenv('GITHUB_TOKEN'):
                self.github_token = os.getenv('GITHUB_TOKEN')
                st.info(f"🔍 Debug: Token from environment: {self.github_token[:20]}...")
            else:
                st.error("🔍 Debug: No token found in any location!")
                st.error(f"🔍 Secrets available: {list(st.secrets.keys()) if hasattr(st, 'secrets') else 'No secrets'}")
        except Exception as e:
            st.error(f"🔍 Debug: Error loading token: {str(e)}")
            self.github_token = None
        
        # Clean the token (remove quotes and whitespace)
        if self.github_token:
            self.github_token = str(self.github_token).strip().strip('"').strip("'")
            st.success(f"🔍 Debug: Cleaned token: {self.github_token[:20]}...")
        
        if self.github_token:
            self.session.headers.update({
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'BlockchainResearchHub/1.0'
            })
            self.rate_limit = 5000  # With token
        else:
            self.session.headers.update({
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'BlockchainResearchHub/1.0'
            })
            self.rate_limit = 60   # Without token
        
        # Repository configurations
        self.repositories = {
            'ethereum': {
                'name': 'Ethereum Improvement Proposals (EIPs)',
                'repo': 'ethereum/EIPs',
                'path': 'EIPS',
                'website': 'https://eips.ethereum.org/',
                'prefix': 'eip-',
                'file_extension': '.md'
            },
            'bitcoin': {
                'name': 'Bitcoin Improvement Proposals (BIPs)',
                'repo': 'bitcoin/bips',
                'path': '',
                'website': 'https://github.com/bitcoin/bips',
                'prefix': 'bip-',
                'file_extension': '.mediawiki'
            },
            'tron': {
                'name': 'TRON Improvement Proposals (TIPs)',
                'repo': 'tronprotocol/TIPs',
                'path': '',
                'website': 'https://tip.tronprotocol.org/',
                'prefix': 'tip-',
                'file_extension': '.md'
            },
            'binance_smart_chain': {
                'name': 'BNB Chain Evolution Proposals (BEPs)',
                'repo': 'bnb-chain/BEPs',
                'path': '',
                'website': 'https://github.com/bnb-chain/BEPs',
                'prefix': 'bep-',
                'file_extension': '.md'
            }
        }
        
        # Cache for proposals
        self.cache = {}
        self.cache_duration = 300  # 5 minutes
    
    def get_latest_proposals(self, protocol: str, limit: int = 10, status_filter: str = None, sort_by: str = 'number') -> List[Dict]:
        """Get latest proposals for a protocol"""
        cache_key = f"{protocol}_{limit}_{status_filter}"
        
        # Check cache
        if self._is_cached(cache_key):
            return self.cache[cache_key]['data']
        
        try:
            proposals = self._fetch_proposals_from_github(protocol, limit, sort_by, status_filter)
            st.info(f"🔍 Debug: Fetched {len(proposals)} proposals before status filtering")
            
            # Debug: Show first few proposal statuses
            if proposals:
                for i, p in enumerate(proposals[:3]):
                    st.info(f"🔍 Debug: Proposal {i+1} - Status: '{p.get('status', 'Unknown')}'")
            
            # Apply status filter
            if status_filter and status_filter != 'all':
                st.info(f"🔍 Debug: Applying status filter: '{status_filter}'")
                proposals = self._filter_by_status(proposals, status_filter)
                st.info(f"🔍 Debug: {len(proposals)} proposals after status filtering")
            
            # Cache results
            self._cache_data(cache_key, proposals)
            return proposals
            
        except Exception as e:
            st.warning(f"⚠️ GitHub API error for {protocol}: {str(e)}. Using fallback data.")
            return self._get_fallback_proposals(protocol, limit)
    
    def _fetch_proposals_from_github(self, protocol: str, limit: int, sort_by: str = 'number', status_filter: str = None) -> List[Dict]:
        """Fetch proposals from GitHub API"""
        if protocol not in self.repositories:
            st.error(f"🔍 Debug: Protocol {protocol} not found in repositories")
            return []
        
        repo_config = self.repositories[protocol]
        repo = repo_config['repo']
        path = repo_config['path']
        
        # Get repository contents
        url = f"https://api.github.com/repos/{repo}/contents/{path}" if path else f"https://api.github.com/repos/{repo}/contents"
        
        response = self.session.get(url)
        response.raise_for_status()
        
        files = response.json()
        
        # Filter proposal files
        proposal_files = []
        prefix = repo_config['prefix']
        extension = repo_config['file_extension']
        
        for file in files:
            if (file['type'] == 'file' and 
                file['name'].startswith(prefix) and 
                file['name'].endswith(extension)):
                proposal_files.append(file)
        
        # Sort by name (which includes number) and get latest first
        proposal_files.sort(key=lambda x: self._extract_proposal_number(x['name']), reverse=True)
        
        # For date sorting or status filtering, we need to fetch more files initially to find matches
        if status_filter in ['draft', 'review', 'withdrawn']:
            initial_limit = limit * 10  # Search through more proposals for less common statuses
        elif sort_by == 'date':
            initial_limit = limit * 3   # Need more for date sorting
        else:
            initial_limit = limit       # Default
        proposal_files = proposal_files[:initial_limit]
        
        # Fetch details for each proposal
        proposals = []
        
        for file in proposal_files:
            try:
                proposal_data = self._fetch_proposal_details(repo, file, repo_config)
                if proposal_data:
                    proposals.append(proposal_data)
            except Exception as e:
                continue  # Skip failed proposals
        
        # Apply sorting based on sort_by parameter
        if sort_by == 'date':
            # Sort by creation date (newest first)
            proposals.sort(key=lambda x: self._parse_date_for_sorting(x.get('created', '')), reverse=True)
        # else: already sorted by number (default)
        
        # Apply limit after date sorting
        proposals = proposals[:limit]
        
        return proposals
    
    def _fetch_proposal_details(self, repo: str, file: Dict, config: Dict) -> Optional[Dict]:
        """Fetch detailed proposal information"""
        try:
            # Get file content
            content_url = f"https://api.github.com/repos/{repo}/contents/{file['path']}"
            response = self.session.get(content_url)
            response.raise_for_status()
            
            file_data = response.json()
            
            # Decode content
            content = base64.b64decode(file_data['content']).decode('utf-8')
            
            # Parse proposal metadata
            proposal_info = self._parse_proposal_content(content, file['name'], config)
            
            # Add GitHub metadata
            proposal_info.update({
                'file_url': file_data['html_url'],
                'last_modified': file_data.get('last_modified', 'Unknown'),
                'size': file_data['size']
            })
            
            return proposal_info
            
        except Exception as e:
            # Return basic info if detailed fetch fails
            return {
                'number': self._extract_proposal_number(file['name']),
                'title': file['name'].replace(config['prefix'], '').replace(config['file_extension'], ''),
                'status': 'Unknown',
                'author': 'Unknown',
                'created': 'Unknown',
                'file_url': f"https://github.com/{repo}/blob/master/{file['path']}",
                'summary': 'Details unavailable'
            }
    
    def _parse_proposal_content(self, content: str, filename: str, config: Dict) -> Dict:
        """Parse proposal content to extract metadata"""
        proposal_number = self._extract_proposal_number(filename)
        
        # Initialize default values
        proposal_data = {
            'number': proposal_number,
            'title': f"Proposal {proposal_number}",
            'status': 'Unknown',
            'author': 'Unknown',
            'created': 'Unknown',
            'summary': content[:200] + '...' if len(content) > 200 else content
        }
        
        try:
            # Parse different formats
            if config['file_extension'] == '.md':
                # Check for YAML frontmatter (EIPs)
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        frontmatter = parts[1]
                        body = parts[2]
                        
                        # Parse YAML-like frontmatter
                        for line in frontmatter.split('\n'):
                            if ':' in line:
                                key, value = line.split(':', 1)
                                key = key.strip().lower()
                                value = value.strip().strip('"\'')
                                
                                if key == 'title':
                                    proposal_data['title'] = value
                                elif key == 'status':
                                    proposal_data['status'] = value
                                elif key in ['author', 'authors']:
                                    proposal_data['author'] = value
                                elif key in ['created', 'date']:
                                    proposal_data['created'] = value
                        
                        # Get summary from body
                        body_lines = [line.strip() for line in body.split('\n') if line.strip()]
                        if body_lines:
                            proposal_data['summary'] = ' '.join(body_lines[:3])[:300] + '...'
                
                # Check for TIP format (starts with ``` code block)
                elif content.startswith('```'):
                    # TIP format with code block frontmatter
                    lines = content.split('\n')
                    in_frontmatter = False
                    body_start = 0
                    
                    for i, line in enumerate(lines):
                        line = line.strip()
                        
                        if line == '```' and not in_frontmatter:
                            in_frontmatter = True
                            continue
                        elif line == '```' and in_frontmatter:
                            in_frontmatter = False
                            body_start = i + 1
                            break
                        elif in_frontmatter and ':' in line:
                            key, value = line.split(':', 1)
                            key = key.strip().lower()
                            value = value.strip().strip('"\'')
                            
                            if key == 'title':
                                proposal_data['title'] = value
                            elif key == 'status':
                                proposal_data['status'] = value
                            elif key in ['author', 'authors']:
                                # Handle author format like "name email@domain.com"
                                if '@' in value and ' ' in value:
                                    proposal_data['author'] = value.split()[0]  # Get just the name
                                else:
                                    proposal_data['author'] = value
                            elif key in ['created', 'date']:
                                proposal_data['created'] = value
                            elif key == 'tip':
                                # TIP-specific number field - but prioritize filename if there's a mismatch
                                content_number = value
                                filename_number = self._extract_proposal_number(filename)
                                
                                # Use filename number if there's a significant mismatch (repo error)
                                if abs(int(content_number) - filename_number) > 1:
                                    proposal_data['number'] = filename_number
                                    # Keep original for reference
                                    proposal_data['content_number'] = content_number
                                else:
                                    proposal_data['number'] = content_number
                            elif key == 'category':
                                proposal_data['category'] = value
                            elif key == 'type':
                                proposal_data['type'] = value
                    
                    # Get summary from body after frontmatter
                    if body_start < len(lines):
                        body_lines = [line.strip() for line in lines[body_start:] if line.strip() and not line.startswith('#')]
                        if body_lines:
                            proposal_data['summary'] = ' '.join(body_lines[:3])[:300] + '...'
            
            elif config['file_extension'] == '.mediawiki':
                # MediaWiki format (BIPs)
                lines = content.split('\n')
                for line in lines[:20]:  # Check first 20 lines
                    line = line.strip()
                    if line.startswith('BIP:'):
                        proposal_data['number'] = line.split(':', 1)[1].strip()
                    elif line.startswith('Title:'):
                        proposal_data['title'] = line.split(':', 1)[1].strip()
                    elif line.startswith('Status:'):
                        proposal_data['status'] = line.split(':', 1)[1].strip()
                    elif line.startswith('Author:'):
                        proposal_data['author'] = line.split(':', 1)[1].strip()
                    elif line.startswith('Created:'):
                        proposal_data['created'] = line.split(':', 1)[1].strip()
        
        except Exception:
            pass  # Use defaults if parsing fails
        
        return proposal_data
    
    def _extract_proposal_number(self, filename: str) -> int:
        """Extract proposal number from filename"""
        try:
            # Extract number from filename like "eip-1559.md" or "bip-0001.mediawiki"
            numbers = re.findall(r'\d+', filename)
            return int(numbers[0]) if numbers else 0
        except:
            return 0
    
    def _parse_date_for_sorting(self, date_str: str) -> str:
        """Parse date string for sorting (newest first)"""
        if not date_str or date_str == 'Unknown':
            return '1900-01-01'  # Very old date for unknown dates
        
        # Try to extract YYYY-MM-DD format dates
        try:
            import re
            # Look for YYYY-MM-DD pattern
            date_match = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', str(date_str))
            if date_match:
                year, month, day = date_match.groups()
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            
            # Look for just year
            year_match = re.search(r'(\d{4})', str(date_str))
            if year_match:
                return f"{year_match.group(1)}-01-01"
            
            return '1900-01-01'
        except:
            return '1900-01-01'
    
    def _filter_by_status(self, proposals: List[Dict], status_filter: str) -> List[Dict]:
        """Filter proposals by status"""
        if status_filter == 'draft':
            valid_statuses = ['draft', 'idea', 'open']
        elif status_filter == 'active':
            valid_statuses = ['active', 'review', 'last call', 'lastcall']  # Handle LASTCALL variation
        elif status_filter == 'final' or status_filter == 'production':
            valid_statuses = ['final', 'accepted', 'closed']
        elif status_filter == 'withdrawn':
            valid_statuses = ['withdrawn', 'rejected', 'superseded']
        elif status_filter == 'review':
            valid_statuses = ['review', 'last call', 'lastcall']
        else:
            return proposals
        
        # Debug: Show all unique statuses found
        all_statuses = set(p.get('status', '').lower() for p in proposals)
        st.info(f"🔍 Debug: All statuses found: {sorted(all_statuses)}")
        st.info(f"🔍 Debug: Looking for statuses: {valid_statuses}")
        
        # Find matching proposals
        matching = []
        for p in proposals:
            p_status = p.get('status', '').lower()
            if p_status in valid_statuses:
                matching.append(p)
                st.info(f"🔍 Debug: MATCH - TIP-{p.get('number', 'N/A')} has status '{p.get('status', 'Unknown')}'")
        
        return matching
    
    def _get_fallback_proposals(self, protocol: str, limit: int) -> List[Dict]:
        """Fallback mock proposals when API fails"""
        mock_proposals = []
        
        for i in range(min(limit, 5)):
            mock_proposals.append({
                'number': f"{protocol.upper()}-{1000 + i}",
                'title': f"Sample {protocol.capitalize()} Proposal {i + 1}",
                'status': ['Draft', 'Active', 'Final'][i % 3],
                'author': f"Author {i + 1}",
                'created': (datetime.now() - timedelta(days=i * 10)).strftime('%Y-%m-%d'),
                'summary': f"This is a sample proposal for {protocol} demonstrating the proposal interface.",
                'file_url': f"https://github.com/example/{protocol}/proposals/{i + 1}"
            })
        
        return mock_proposals
    
    def get_proposal_stats(self) -> Dict[str, Any]:
        """Get statistics about proposals across all protocols"""
        stats = {}
        
        for protocol in self.repositories.keys():
            try:
                proposals = self.get_latest_proposals(protocol, limit=50)
                
                status_counts = {}
                for proposal in proposals:
                    status = proposal.get('status', 'Unknown').lower()
                    status_counts[status] = status_counts.get(status, 0) + 1
                
                stats[protocol] = {
                    'total': len(proposals),
                    'status_breakdown': status_counts,
                    'latest': proposals[0] if proposals else None
                }
            except:
                stats[protocol] = {'total': 0, 'status_breakdown': {}, 'latest': None}
        
        return stats
    
    def search_proposals(self, query: str, protocols: List[str] = None) -> List[Dict]:
        """Search proposals across protocols"""
        if not protocols:
            protocols = list(self.repositories.keys())
        
        results = []
        query_lower = query.lower()
        
        # Special handling for broad searches like "TIPS" or "ALL"
        search_limit = 200 if query_lower in ['tips', 'eips', 'bips', 'beps', 'all'] else 100
        
        for protocol in protocols:
            proposals = self.get_latest_proposals(protocol, limit=search_limit, sort_by='number', status_filter=None)
            
            for proposal in proposals:
                # Special handling for protocol-specific searches
                if query_lower in ['tips', 'eips', 'bips', 'beps']:
                    proposal_type = proposal.get('type', '').lower()
                    if query_lower == 'tips' and protocol == 'tron':
                        proposal['protocol'] = protocol
                        results.append(proposal)
                    elif query_lower == 'eips' and protocol == 'ethereum':
                        proposal['protocol'] = protocol
                        results.append(proposal)
                    elif query_lower == 'bips' and protocol == 'bitcoin':
                        proposal['protocol'] = protocol
                        results.append(proposal)
                    elif query_lower == 'beps' and protocol == 'binance_smart_chain':
                        proposal['protocol'] = protocol
                        results.append(proposal)
                elif query_lower == 'all':
                    # Return all proposals
                    proposal['protocol'] = protocol
                    results.append(proposal)
                else:
                    # Regular text search in title and summary
                    title = proposal.get('title', '').lower()
                    summary = proposal.get('summary', '').lower()
                    
                    if query_lower in title or query_lower in summary:
                        proposal['protocol'] = protocol
                        results.append(proposal)
        
        # For protocol-specific searches like "TIPS", sort by number only (latest first)
        # For text searches, sort by relevance first, then by number
        if query_lower in ['tips', 'eips', 'bips', 'beps', 'all']:
            # Simple sort by proposal number (latest first)
            def get_number_sort_key(proposal):
                try:
                    number = proposal.get('number', 0)
                    if isinstance(number, str):
                        import re
                        match = re.search(r'(\d+)', str(number))
                        number = int(match.group(1)) if match else 0
                    return -int(number)  # Negative for descending order
                except (ValueError, TypeError):
                    return 0
            
            results.sort(key=get_number_sort_key)
        else:
            # Sort by relevance (title matches first, then by proposal number)
            def get_sort_key(proposal):
                title_match = query_lower not in proposal.get('title', '').lower()
                # Safely convert number to int for sorting
                try:
                    number = proposal.get('number', 0)
                    if isinstance(number, str):
                        # Extract number from string like "eip-7998" -> 7998
                        import re
                        match = re.search(r'(\d+)', str(number))
                        number = int(match.group(1)) if match else 0
                    return (title_match, -int(number))
                except (ValueError, TypeError):
                    return (title_match, 0)
            
            results.sort(key=get_sort_key)
        
        return results[:20]  # Return top 20 matches
    
    def _is_cached(self, key: str) -> bool:
        """Check if data is cached and still valid"""
        if key not in self.cache:
            return False
        
        age = time.time() - self.cache[key]['timestamp']
        return age < self.cache_duration
    
    def _cache_data(self, key: str, data: Any):
        """Cache data with timestamp"""
        self.cache[key] = {
            'data': data,
            'timestamp': time.time()
        }
    
    def check_rate_limit(self) -> Dict[str, Any]:
        """Check current GitHub API rate limit status"""
        try:
            response = self.session.get('https://api.github.com/rate_limit')
            if response.status_code == 200:
                return response.json()
        except:
            pass
        
        return {
            'rate': {
                'limit': self.rate_limit,
                'remaining': self.rate_limit,
                'reset': int(time.time()) + 3600
            }
        }

# Global instance
realtime_proposals = RealtimeProposalsService()