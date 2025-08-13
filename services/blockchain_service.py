"""
Blockchain Data Service for real-time protocol information and analysis
"""
import requests
import json
import time
from typing import Dict, List, Optional, Any
from config import ANKR_API_KEY, ANKR_API_URL, BLOCKCHAIN_PROTOCOLS, USE_CASES, API_CONFIG
import streamlit as st

class BlockchainService:
    """Service for blockchain data retrieval and analysis"""
    
    def __init__(self):
        self.ankr_api_key = ANKR_API_KEY
        self.ankr_api_url = ANKR_API_URL
        self.timeout = API_CONFIG["timeout"]
        self.cache_ttl = API_CONFIG["cache_ttl"]
        
        # Mock data for development (replace with real API calls)
        self.mock_data = self._generate_mock_data()
    
    def get_recommendations(self, search_params: Dict) -> List[Dict]:
        """Get blockchain recommendations based on search parameters"""
        
        try:
            # Get protocol data
            protocols = self._fetch_protocol_data()
            
            # Filter and score protocols
            filtered_protocols = self._filter_protocols(protocols, search_params)
            scored_protocols = self._score_protocols(filtered_protocols, search_params)
            
            # Sort by score and return top recommendations
            recommendations = sorted(scored_protocols, key=lambda x: x['score'], reverse=True)
            
            return recommendations[:10]  # Top 10 recommendations
            
        except Exception as e:
            st.error(f"Blockchain Service Error: {str(e)}")
            return []
    
    def get_protocol_details(self, protocol_id: str) -> Optional[Dict]:
        """Get detailed information for a specific blockchain protocol"""
        
        try:
            if protocol_id in self.mock_data:
                return self.mock_data[protocol_id]
            else:
                # Fetch from real API
                return self._fetch_protocol_from_api(protocol_id)
                
        except Exception as e:
            st.error(f"Error fetching protocol details: {str(e)}")
            return None
    
    def get_comparative_analysis(self, protocol_ids: List[str]) -> Dict:
        """Get comparative analysis of multiple protocols"""
        
        try:
            protocols = []
            for pid in protocol_ids:
                protocol_data = self.get_protocol_details(pid)
                if protocol_data:
                    protocols.append(protocol_data)
            
            return self._generate_comparison_metrics(protocols)
            
        except Exception as e:
            st.error(f"Comparison analysis error: {str(e)}")
            return {}
    
    def _fetch_protocol_data(self) -> List[Dict]:
        """Fetch current protocol data from APIs"""
        
        # For now, return mock data
        # TODO: Implement real API integration with Ankr
        return list(self.mock_data.values())
    
    def _fetch_protocol_from_api(self, protocol_id: str) -> Optional[Dict]:
        """Fetch single protocol data from Ankr API"""
        
        try:
            # TODO: Implement real Ankr API integration
            headers = {
                "Content-Type": "application/json"
            }
            
            if self.ankr_api_key:
                headers["Authorization"] = f"Bearer {self.ankr_api_key}"
            
            # Mock API call for now
            time.sleep(0.1)  # Simulate API delay
            return self.mock_data.get(protocol_id)
            
        except Exception as e:
            # Silently handle API fetch errors
            return None
    
    def _filter_protocols(self, protocols: List[Dict], params: Dict) -> List[Dict]:
        """Filter protocols based on search parameters"""
        
        filtered = []
        
        for protocol in protocols:
            # Check minimum TPS requirement
            if params.get("min_tps") and protocol.get("tps", 0) < params["min_tps"]:
                continue
            
            # Check maximum fee requirement
            if params.get("max_fee") and protocol.get("avg_fee", float('inf')) > params["max_fee"]:
                continue
            
            # Check use case compatibility
            if params.get("use_case"):
                use_case = params["use_case"]
                if use_case not in protocol.get("suitable_for", []):
                    continue
            
            # Check included chains filter
            if params.get("include_chains"):
                if protocol["id"] not in params["include_chains"]:
                    continue
            
            # Check consensus mechanism
            if params.get("consensus_types"):
                if protocol.get("consensus") not in params["consensus_types"]:
                    continue
            
            filtered.append(protocol)
        
        return filtered
    
    def _score_protocols(self, protocols: List[Dict], params: Dict) -> List[Dict]:
        """Score protocols based on search parameters and use case"""
        
        use_case = params.get("use_case", "general")
        use_case_weights = USE_CASES.get(use_case, {}).get("priorities", {
            "tps": 0.25, "fees": 0.25, "security": 0.25, "ecosystem": 0.25
        })
        
        scored_protocols = []
        
        for protocol in protocols:
            score = 0
            max_score = 0
            reasoning_parts = []
            
            # TPS Score (normalized to 0-100)
            if "tps" in use_case_weights:
                tps_score = min(protocol.get("tps", 0) / 100000 * 100, 100)  # Max at 100k TPS
                weight = use_case_weights["tps"]
                score += tps_score * weight
                max_score += 100 * weight
                if tps_score > 70:
                    reasoning_parts.append(f"Excellent throughput ({protocol.get('tps', 0):,} TPS)")
            
            # Fee Score (inverted - lower fees = higher score)  
            if "fees" in use_case_weights:
                avg_fee = protocol.get("avg_fee", 1.0)
                fee_score = max(0, 100 - (avg_fee * 100))  # $1 fee = 0 score
                weight = use_case_weights["fees"]
                score += fee_score * weight
                max_score += 100 * weight
                if fee_score > 90:
                    reasoning_parts.append(f"Very low fees (${avg_fee:.4f})")
            
            # Security Score
            if "security" in use_case_weights:
                security_score = protocol.get("security_score", 70)
                weight = use_case_weights["security"]
                score += security_score * weight
                max_score += 100 * weight
                if security_score > 85:
                    reasoning_parts.append("Strong security track record")
            
            # Ecosystem Score
            if "ecosystem" in use_case_weights:
                ecosystem_score = protocol.get("ecosystem_score", 60)
                weight = use_case_weights["ecosystem"]
                score += ecosystem_score * weight
                max_score += 100 * weight
                if ecosystem_score > 80:
                    reasoning_parts.append("Rich developer ecosystem")
            
            # Normalize score to 0-100
            final_score = int((score / max_score * 100) if max_score > 0 else 0)
            
            protocol_copy = protocol.copy()
            protocol_copy["score"] = final_score
            protocol_copy["reasoning"] = "; ".join(reasoning_parts) if reasoning_parts else "Good overall match"
            
            scored_protocols.append(protocol_copy)
        
        return scored_protocols
    
    def _generate_comparison_metrics(self, protocols: List[Dict]) -> Dict:
        """Generate comparison metrics for protocols"""
        
        if not protocols:
            return {}
        
        metrics = {
            "protocols": protocols,
            "comparison_matrix": {},
            "rankings": {},
            "summary": {}
        }
        
        # Generate comparison matrix
        comparison_fields = ["tps", "avg_fee", "finality_time", "security_score", "ecosystem_score"]
        
        for field in comparison_fields:
            metrics["comparison_matrix"][field] = {}
            values = [p.get(field, 0) for p in protocols]
            
            for i, protocol in enumerate(protocols):
                metrics["comparison_matrix"][field][protocol["name"]] = values[i]
        
        # Generate rankings
        for field in comparison_fields:
            sorted_protocols = sorted(protocols, 
                key=lambda x: x.get(field, 0), 
                reverse=(field != "avg_fee"))  # Lower fees are better
            
            metrics["rankings"][field] = [p["name"] for p in sorted_protocols]
        
        return metrics
    
    def _generate_mock_data(self) -> Dict[str, Dict]:
        """Generate accurate L1 blockchain protocol data - Focus on Ethereum, Base, Tron, BSC, Bitcoin"""
        
        return {
            "ethereum": {
                "id": "ethereum",
                "name": "Ethereum", 
                "symbol": "ETH",
                "tps": 18,
                "avg_fee": 4.20,
                "finality_time": 768,  # ~12.8 minutes (64 blocks)
                "security_score": 98,
                "ecosystem_score": 100,
                "market_cap": 280000000000,  # ~$280B
                "tvl": 28000000000,  # ~$28B TVL
                "consensus": "Proof of Stake",
                "type": "Layer 1",
                "suitable_for": ["enterprise", "nft", "dao", "institutional", "smart_contracts"],
                "description": "World's leading smart contract platform with extensive enterprise and institutional adoption",
                "website": "https://ethereum.org",
                "active_developers": 5200,
                "dapp_count": 3500,
                "validator_count": 1000000,
                "network_hashrate": "N/A (PoS)",
                "energy_consumption": "Low (PoS)",
                "last_updated": time.time()
            },
            "base": {
                "id": "base",
                "name": "Base", 
                "symbol": "ETH",
                "tps": 350,
                "avg_fee": 0.15,
                "finality_time": 2,  # ~2 seconds
                "security_score": 92,
                "ecosystem_score": 85,
                "market_cap": 0,  # No native token
                "tvl": 2800000000,  # ~$2.8B TVL
                "consensus": "Optimistic Rollup (Ethereum L2)",
                "type": "Layer 2",
                "suitable_for": ["consumer", "social", "gaming", "payments", "mainstream"],
                "description": "Coinbase's Ethereum L2 solution designed for mainstream adoption with low fees and high security",
                "website": "https://base.org",
                "active_developers": 800,
                "dapp_count": 250,
                "validator_count": 0,  # Inherits Ethereum security
                "network_hashrate": "Inherits from Ethereum",
                "energy_consumption": "Very Low (L2)",
                "last_updated": time.time()
            },
            "tron": {
                "id": "tron",
                "name": "TRON",
                "symbol": "TRX", 
                "tps": 2000,
                "avg_fee": 0.001,
                "finality_time": 3,  # ~3 seconds
                "security_score": 78,
                "ecosystem_score": 75,
                "market_cap": 12000000000,  # ~$12B
                "tvl": 8500000000,  # ~$8.5B TVL (mainly USDT)
                "consensus": "Delegated Proof of Stake",
                "type": "Layer 1",
                "suitable_for": ["payments", "stablecoins", "gaming", "content"],
                "description": "High-throughput blockchain optimized for USDT transfers and entertainment applications",
                "website": "https://tron.network",
                "active_developers": 1200,
                "dapp_count": 600,
                "validator_count": 27,  # Super Representatives
                "network_hashrate": "N/A (DPoS)",
                "energy_consumption": "Low",
                "last_updated": time.time()
            },
            "bsc": {
                "id": "bsc",
                "name": "BNB Smart Chain", 
                "symbol": "BNB",
                "tps": 2100,
                "avg_fee": 0.30,
                "finality_time": 3,  # ~3 seconds
                "security_score": 82,
                "ecosystem_score": 88,
                "market_cap": 42000000000,  # ~$42B (BNB)
                "tvl": 5200000000,  # ~$5.2B TVL
                "consensus": "Proof of Stake Authority",
                "type": "Layer 1",
                "suitable_for": ["gaming", "payments", "high_volume", "business"],
                "description": "EVM-compatible blockchain with fast transactions and strong application ecosystem",
                "website": "https://www.bnbchain.org",
                "active_developers": 1800,
                "dapp_count": 1100,
                "validator_count": 21,  # Active validators
                "network_hashrate": "N/A (PoSA)",
                "energy_consumption": "Low",
                "last_updated": time.time()
            },
            "bitcoin": {
                "id": "bitcoin",
                "name": "Bitcoin",
                "symbol": "BTC",
                "tps": 7,
                "avg_fee": 8.50,
                "finality_time": 3600,  # ~1 hour (6 confirmations)
                "security_score": 100,
                "ecosystem_score": 65,
                "market_cap": 920000000000,  # ~$920B
                "tvl": 0,  # No DeFi/smart contracts
                "consensus": "Proof of Work",
                "type": "Layer 1",
                "suitable_for": ["store-of-value", "payments", "institutional", "treasury"],
                "description": "The original and most secure cryptocurrency, primarily used as digital gold and store of value",
                "website": "https://bitcoin.org",
                "active_developers": 800,
                "dapp_count": 0,  # No smart contracts
                "validator_count": 0,  # Miners, not validators
                "network_hashrate": "450 EH/s",
                "energy_consumption": "High (PoW)",
                "last_updated": time.time()
            }
        }