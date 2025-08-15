#!/usr/bin/env python3
"""
Service for reading scraped proposal data from JSON files (no API calls)
"""
import json
import os
import time
from typing import Dict, List, Optional
import streamlit as st

class ScrapedDataService:
    """Service for reading pre-scraped blockchain proposal data"""
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.cache = {}
        self.cache_duration = 300  # 5 minutes
        
        # Protocol configurations
        self.protocols = {
            'ethereum': {
                'name': 'Ethereum Improvement Proposals (EIPs)',
                'file': 'eips.json',
                'website': 'https://eips.ethereum.org/',
                'color': '#627EEA'
            },
            'tron': {
                'name': 'TRON Improvement Proposals (TIPs)',
                'file': 'tips.json',
                'website': 'https://tip.tronprotocol.org/',
                'color': '#FF0013'
            },
            'bitcoin': {
                'name': 'Bitcoin Improvement Proposals (BIPs)',
                'file': 'bips.json',
                'website': 'https://github.com/bitcoin/bips',
                'color': '#F7931A'
            },
            'binance_smart_chain': {
                'name': 'BNB Chain Evolution Proposals (BEPs)',
                'file': 'beps.json',
                'website': 'https://github.com/bnb-chain/BEPs',
                'color': '#F3BA2F'
            }
        }
    
    def load_protocol_data(self, protocol: str) -> Dict:
        """Load data for a specific protocol"""
        if protocol not in self.protocols:
            return {"generated_at": None, "count": 0, "items": []}
        
        cache_key = f"{protocol}_data"
        
        # Check cache
        if self._is_cached(cache_key):
            return self.cache[cache_key]['data']
        
        try:
            file_path = os.path.join(self.data_dir, self.protocols[protocol]['file'])
            
            if not os.path.exists(file_path):
                st.warning(f"Data file not found: {file_path}. Run scrapers first.")
                return {"generated_at": None, "count": 0, "items": []}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Cache the data
            self._cache_data(cache_key, data)
            return data
            
        except Exception as e:
            st.error(f"Error loading {protocol} data: {e}")
            return {"generated_at": None, "count": 0, "items": []}
    
    def get_latest_proposals(self, protocol: str, limit: int = 10, status_filter: str = None, sort_by: str = 'date') -> List[Dict]:
        """Get latest proposals for a protocol"""
        data = self.load_protocol_data(protocol)
        proposals = data.get('items', [])
        
        if not proposals:
            return []
        
        # Apply status filter
        if status_filter and status_filter != 'all':
            proposals = self._filter_by_status(proposals, status_filter)
        
        # Apply sorting
        if sort_by == 'date':
            # Sort by creation date (newest first)
            proposals.sort(key=lambda x: self._parse_date_for_sorting(x.get('created', '')), reverse=True)
        else:
            # Sort by number (latest first) - default
            proposals.sort(key=lambda x: x.get('number', 0), reverse=True)
        
        # Apply limit
        return proposals[:limit]
    
    def _filter_by_status(self, proposals: List[Dict], status_filter: str) -> List[Dict]:
        """Filter proposals by status"""
        if status_filter == 'draft':
            valid_statuses = ['draft', 'idea', 'open']
        elif status_filter == 'active':
            valid_statuses = ['active', 'review', 'last call', 'lastcall']
        elif status_filter == 'final' or status_filter == 'production':
            valid_statuses = ['final', 'accepted', 'closed', 'enabled']
        elif status_filter == 'proposed':
            valid_statuses = ['proposed']
        elif status_filter == 'withdrawn':
            valid_statuses = ['withdrawn', 'rejected', 'superseded', 'replaced', 'obsolete', 'deferred']
        elif status_filter == 'review':
            valid_statuses = ['review', 'last call', 'lastcall', 'candidate']
        elif status_filter == 'living':
            valid_statuses = ['living']
        elif status_filter == 'stagnant':
            valid_statuses = ['stagnant']
        else:
            return proposals
        
        # Find matching proposals
        matching = []
        for p in proposals:
            p_status = p.get('status', '').lower()
            if p_status in valid_statuses:
                matching.append(p)
        
        return matching
    
    def _parse_date_for_sorting(self, date_str: str) -> str:
        """Parse date string for sorting (newest first)"""
        if not date_str or date_str == 'Unknown':
            return '1900-01-01'
        
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
    
    def search_proposals(self, query: str, protocols: List[str] = None) -> List[Dict]:
        """Search proposals across protocols"""
        if not protocols:
            protocols = list(self.protocols.keys())
        
        results = []
        query_lower = query.lower()
        
        # Special handling for broad searches like "TIPS" or "ALL"
        search_limit = 200 if query_lower in ['tips', 'eips', 'bips', 'beps', 'all'] else 100
        
        for protocol in protocols:
            proposals = self.get_latest_proposals(protocol, limit=search_limit, sort_by='date', status_filter=None)
            
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
        
        # Sort results
        if query_lower in ['tips', 'eips', 'bips', 'beps', 'all']:
            results.sort(key=lambda x: x.get('number', 0), reverse=True)
        else:
            # Sort by relevance (title matches first, then by proposal number)
            def get_sort_key(proposal):
                title_match = query_lower not in proposal.get('title', '').lower()
                return (title_match, -proposal.get('number', 0))
            results.sort(key=get_sort_key)
        
        return results[:20]  # Return top 20 matches
    
    def get_proposal_stats(self) -> Dict:
        """Get statistics about proposals across all protocols"""
        stats = {}
        
        for protocol in self.protocols.keys():
            data = self.load_protocol_data(protocol)
            proposals = data.get('items', [])
            
            if proposals:
                status_counts = {}
                for proposal in proposals:
                    status = proposal.get('status', 'Unknown').lower()
                    status_counts[status] = status_counts.get(status, 0) + 1
                
                stats[protocol] = {
                    'total': len(proposals),
                    'status_breakdown': status_counts,
                    'latest': proposals[0] if proposals else None,
                    'generated_at': data.get('generated_at'),
                    'generated_at_iso': data.get('generated_at_iso', 'Unknown')
                }
            else:
                stats[protocol] = {
                    'total': 0, 
                    'status_breakdown': {}, 
                    'latest': None,
                    'generated_at': None,
                    'generated_at_iso': 'No data'
                }
        
        return stats
    
    def _is_cached(self, key: str) -> bool:
        """Check if data is cached and still valid"""
        if key not in self.cache:
            return False
        
        age = time.time() - self.cache[key]['timestamp']
        return age < self.cache_duration
    
    def _cache_data(self, key: str, data):
        """Cache data with timestamp"""
        self.cache[key] = {
            'data': data,
            'timestamp': time.time()
        }

# Global instance
scraped_data_service = ScrapedDataService()