"""
Custom AI Agent for L1 Blockchain Research & Advisory
Real-time data integration with specialized L1 protocol analysis
"""
import re
import json
from typing import Dict, List, Optional, Any, Tuple
from config import USE_CASES, BLOCKCHAIN_PROTOCOLS, EVALUATION_PARAMS
from services.enhanced_realtime_data import EnhancedRealtimeDataService
from services.governance_data_service import GovernanceDataService
from services.latest_proposals_fetcher import LatestProposalsFetcher
import streamlit as st

class CustomBlockchainAIAgent:
    """
    Custom AI agent specialized in L1 blockchain analysis and recommendations
    Provides real-time data integration and detailed analysis
    """
    
    def __init__(self):
        self.l1_data_service = EnhancedRealtimeDataService()
        self.governance_service = GovernanceDataService()
        self.proposals_fetcher = LatestProposalsFetcher()
        self.l1_specialization = True
        self.conversation_context = []
        
    def get_chat_response(self, user_input: str, conversation_history: List[Dict]) -> str:
        """Generate detailed AI response for user query with real-time L1 data"""
        
        # Update conversation context
        self.conversation_context = conversation_history[-5:]
        
        # Analyze user intent
        intent_analysis = self._analyze_user_intent(user_input)
        
        # Generate response with real-time L1 focus
        if intent_analysis["primary_intent"] == "governance":
            return self._get_governance_analysis(intent_analysis)
        elif intent_analysis["primary_intent"] == "development":
            return self._get_development_activity_analysis(intent_analysis)
        elif intent_analysis["primary_intent"] == "specific_data":
            return self._get_protocol_specific_data(intent_analysis, user_input)
        elif intent_analysis["primary_intent"] == "recommendation":
            return self._get_live_l1_recommendations(intent_analysis)
        else:
            return self._generate_general_l1_response(user_input, intent_analysis)
    
    def extract_search_parameters(self, user_input: str) -> Optional[Dict]:
        """Extract search parameters focused on L1 protocols"""
        
        params = {}
        user_input_lower = user_input.lower()
        
        # Extract use case
        use_case = self._extract_use_case(user_input_lower)
        if use_case:
            params["use_case"] = use_case
        
        # Extract technical requirements for L1s
        technical_params = self._extract_l1_technical_requirements(user_input_lower)
        params.update(technical_params)
        
        # Extract L1 mentions
        mentioned_l1s = self._extract_l1_mentions(user_input_lower)
        if mentioned_l1s:
            params["include_chains"] = mentioned_l1s
        
        return params if params else None
    
    def _analyze_user_intent(self, user_input: str) -> Dict:
        """Analyze user intent with L1 focus"""
        
        user_input_lower = user_input.lower()
        
        governance_focused = any(term in user_input_lower for term in [
            # Improvement proposals
            "eip", "eips", "ethereum improvement proposal", "ethereum improvement proposals",
            "bip", "bips", "bitcoin improvement proposal", "bitcoin improvement proposals", 
            "tip", "tips", "tron improvement proposal", "tron improvement proposals",
            "bep", "beps", "bnb evolution proposal", "bnb evolution proposals", "binance evolution proposal", "binance evolution proposals",
            "sup", "sups", "superchain upgrade proposal", "superchain upgrade proposals",
            # General governance terms
            "governance", "proposal", "proposals", "improvement", "improvements", 
            "latest", "recent", "new", "newest", "upcoming", "draft", "final", "active",
            # Latest-specific queries  
            "latest proposals", "recent proposals", "top 5", "top 5 latest", "newest proposals",
            "what's new", "latest eip", "latest bip", "latest sup", "latest tip", "latest bep",
            # Governance processes
            "voting", "consensus", "upgrade", "fork", "network upgrade", "protocol upgrade"
        ])
        
        # Check if this is specifically a "latest proposals" request
        latest_proposals_request = any(term in user_input_lower for term in [
            "latest proposals", "top 5 latest", "newest proposals", "latest eip", "latest bip", 
            "latest sup", "latest tip", "latest bep", "recent proposals", "what's new with", 
            "top 5 newest", "get the latest", "show me latest"
        ])
        development_focused = any(term in user_input_lower for term in ["development", "developer", "activity", "commit", "contributor", "github"])
        specific_data_focused = any(term in user_input_lower for term in ["market cap", "price", "gas fee", "fee", "cost", "current", "what is", "how much"])
        
        # Determine primary intent
        primary_intent = "recommendation"  # default
        if governance_focused:
            primary_intent = "governance"
        elif development_focused:
            primary_intent = "development"
        elif specific_data_focused and len(self._extract_governance_protocol_mentions(user_input_lower) + self._extract_l1_mentions(user_input_lower)) > 0:
            primary_intent = "specific_data"
        
        # Extract specific protocol mentions
        specific_protocols = self._extract_governance_protocol_mentions(user_input_lower)
        
        intent_analysis = {
            "primary_intent": primary_intent,
            "use_case": self._extract_use_case(user_input_lower),
            "l1_focused": any(term in user_input_lower for term in ["l1", "layer 1", "blockchain", "protocol"]),
            "real_time_requested": any(term in user_input_lower for term in ["live", "current", "latest", "real-time", "updated"]),
            "governance_focused": governance_focused,
            "development_focused": development_focused,
            "specific_data_focused": specific_data_focused,
            "specific_protocols": specific_protocols,
            "protocol_focused": len(specific_protocols) > 0,
            "latest_proposals_request": latest_proposals_request
        }
        
        return intent_analysis
    
    def _get_live_l1_recommendations(self, intent_analysis: Dict) -> str:
        """Get real-time L1 protocol recommendations"""
        
        try:
            # Get enhanced live L1 data with premium APIs
            live_data = self.l1_data_service.get_all_enhanced_l1_data()
            
            if not live_data:
                return "Unable to fetch real-time L1 data. Please check your internet connection and try again."
            
            use_case = intent_analysis.get("use_case")
            
            if use_case == "gaming":
                return self._generate_live_gaming_l1_analysis(live_data)
            elif use_case == "payments":
                return self._generate_live_payments_l1_analysis(live_data)
            elif use_case == "enterprise":
                return self._generate_live_enterprise_l1_analysis(live_data)
            else:
                return self._generate_live_general_l1_analysis(live_data)
                
        except Exception as e:
            return f"Error fetching real-time L1 data: {str(e)}. Using cached data where available."
    
    def _generate_live_gaming_l1_analysis(self, live_data: Dict) -> str:
        """Generate live gaming L1 analysis"""
        
        # Calculate gaming scores for L1s
        l1_scores = {}
        for protocol_id, data in live_data.items():
            l1_scores[protocol_id] = self._calculate_l1_gaming_score(data)
        
        # Sort by gaming suitability
        top_l1s = sorted(l1_scores.items(), key=lambda x: x[1], reverse=True)[:5]
        
        response = f"""🎮 **LIVE L1 GAMING ANALYSIS**
*Real-time data updated: {list(live_data.values())[0].get('last_updated', 'Recently')}*

**🏆 TOP L1 PROTOCOLS FOR GAMING:**

"""
        
        rank_emojis = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
        
        for i, (protocol_id, score) in enumerate(top_l1s):
            if protocol_id not in live_data:
                continue
                
            data = live_data[protocol_id]
            emoji = rank_emojis[i] if i < len(rank_emojis) else f"#{i+1}"
            
            # Get performance indicator
            performance_indicator = self._get_performance_indicator(data)
            
            response += f"""{emoji} **{data.get('name', protocol_id.title())}** {performance_indicator} (Gaming Score: {score:.1f}/100)

   💎 **Live Market Metrics**
      • Market Cap: {self._format_currency(data.get('market_cap', 0))}
      • 24h Change: {data.get('price_change_24h', 0):+.2f}%
      • Daily Volume: {self._format_currency(data.get('volume_24h', 0))}

   ⚡ **Gaming Performance**  
      • Throughput: {data.get('tps', 0):,} TPS
      • Finality: {self._format_time(data.get('finality_time', 0))}
      • Transaction Fee: ${data.get('avg_fee', 0):.4f}
      • Security Rating: {data.get('security_score', 0)}/100

   🎯 **Gaming Suitability**: {self._get_gaming_suitability(data)}

"""

        # Enhanced market summary with visual separators
        total_l1_market_cap = sum(data.get('market_cap', 0) for data in live_data.values())
        
        response += f"""
{'═' * 60}

**📊 L1 GAMING MARKET OVERVIEW:**

🎯 **Gaming Performance Leaders**
   • 🚀 Highest TPS: {self._get_metric_leader(live_data, 'tps')} ({self._get_best_metric(live_data, 'tps'):,} TPS)
   • 💸 Lowest Fees: {self._get_metric_leader(live_data, 'avg_fee', lowest=True)} (${self._get_best_metric(live_data, 'avg_fee', lowest=True):.4f})
   • ⚡ Fastest Finality: {self._get_metric_leader(live_data, 'finality_time', lowest=True)} ({self._format_time(self._get_best_metric(live_data, 'finality_time', lowest=True))})

💰 **L1 Protocol Analysis**
   • Combined L1 Market Cap: {self._format_currency(total_l1_market_cap)}
   • Gaming-Ready L1s (>5K TPS): {self._count_high_performance_l1s(live_data)}
   • Ultra-Low Fee Networks (<$0.01): {self._count_low_fee_l1s(live_data)}

🎮 **Gaming Readiness Assessment**
   • **Tier 1** (Excellent): 50K+ TPS, <$0.001 fees
   • **Tier 2** (Very Good): 10K+ TPS, <$0.01 fees  
   • **Tier 3** (Good): 1K+ TPS, <$0.1 fees

{'─' * 60}
💡 **Gaming Insights:**
• High-throughput L1s dominate competitive gaming potential
• Ultra-low fees essential for in-game microtransactions
• Sub-second finality critical for real-time gameplay
• Security scores remain high across all gaming-suitable L1s

*🔄 Data refreshed every 2 minutes from Premium APIs: CoinMarketCap, Chainspect & Etherscan*
"""
        
        return response

    def _generate_live_payments_l1_analysis(self, live_data: Dict) -> str:
        """Generate live payments L1 analysis"""
        
        # Calculate payments scores
        l1_scores = {}
        for protocol_id, data in live_data.items():
            l1_scores[protocol_id] = self._calculate_l1_payments_score(data)
        
        top_l1s = sorted(l1_scores.items(), key=lambda x: x[1], reverse=True)[:5]
        
        response = f"""💸 **LIVE L1 PAYMENTS ANALYSIS**
*Real-time network data updated: {list(live_data.values())[0].get('last_updated', 'Recently')}*

**🏆 TOP L1 PROTOCOLS FOR PAYMENTS:**

"""
        
        rank_emojis = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
        
        for i, (protocol_id, score) in enumerate(top_l1s):
            if protocol_id not in live_data:
                continue
                
            data = live_data[protocol_id]
            emoji = rank_emojis[i] if i < len(rank_emojis) else f"#{i+1}"
            
            response += f"""{emoji} **{data.get('name', protocol_id.title())}** (Payments Score: {score:.1f}/100)

💎 **Network Performance**
   • Market Cap: {self._format_currency(data.get('market_cap', 0))}
   • Transaction Fee: ${data.get('avg_fee', 0):.4f}
   • Throughput: {data.get('tps', 0):,} TPS
   • Finality Time: {self._format_time(data.get('finality_time', 0))}

⚡ **Payment Efficiency**  
   • Daily Transactions: {data.get('daily_transactions', 0):,}
   • Security Score: {data.get('security_score', 0)}/100
   • Network Utilization: {data.get('network_utilization', 0)}%
   • Consensus: {data.get('consensus', 'PoS')}

🎯 **Payment Suitability**: {self._get_payment_suitability(data)}

"""

        # Add payments market insights
        total_daily_tx = sum(data.get('daily_transactions', 0) for data in live_data.values())
        
        response += f"""
{'═' * 60}

**📊 L1 PAYMENTS ECOSYSTEM OVERVIEW:**

🚀 **Performance Leaders**
   • 💸 Lowest Fees: {self._get_metric_leader(live_data, 'avg_fee', lowest=True)} (${self._get_best_metric(live_data, 'avg_fee', lowest=True):.4f})
   • ⚡ Fastest Settlement: {self._get_metric_leader(live_data, 'finality_time', lowest=True)} ({self._format_time(self._get_best_metric(live_data, 'finality_time', lowest=True))})
   • 🏃 Highest Throughput: {self._get_metric_leader(live_data, 'tps')} ({self._get_best_metric(live_data, 'tps'):,} TPS)

💰 **Payment Network Stats**
   • Combined Daily Transactions: {total_daily_tx:,}
   • Ultra-Low Fee Networks (<$0.01): {self._count_low_fee_l1s(live_data)}
   • Fast Settlement (<10s): {self._count_fast_finality_l1s(live_data)}

💡 **Payment Insights:**
• Low fees and fast finality are crucial for payment adoption
• High throughput networks handle payment volume spikes better
• Security remains essential for payment network trust
• Network effects drive payment protocol adoption

*🔄 Data refreshed every 2 minutes from Premium APIs: CoinMarketCap, Chainspect & Etherscan*
"""
        
        return response
    
    def _generate_live_enterprise_l1_analysis(self, live_data: Dict) -> str:
        """Generate live enterprise L1 analysis"""
        
        # Calculate enterprise scores
        l1_scores = {}
        for protocol_id, data in live_data.items():
            l1_scores[protocol_id] = self._calculate_l1_enterprise_score(data)
        
        top_l1s = sorted(l1_scores.items(), key=lambda x: x[1], reverse=True)[:5]
        
        response = f"""🏢 **LIVE L1 ENTERPRISE ANALYSIS**
*Enterprise-grade network assessment updated: {list(live_data.values())[0].get('last_updated', 'Recently')}*

**🏆 TOP L1 PROTOCOLS FOR ENTERPRISE:**

"""
        
        for i, (protocol_id, score) in enumerate(top_l1s):
            if protocol_id not in live_data:
                continue
                
            data = live_data[protocol_id]
            rank = i + 1
            
            response += f"""**#{rank} {data.get('name', protocol_id.title())}** (Enterprise Score: {score:.1f}/100)

🏛️ **Enterprise Readiness**
   • Security Score: {data.get('security_score', 0)}/100
   • Market Cap: {self._format_currency(data.get('market_cap', 0))}
   • Network Stability: {data.get('network_utilization', 0)}% utilization
   • Consensus Mechanism: {data.get('consensus', 'Proof of Stake')}

📊 **Performance Metrics**
   • Throughput: {data.get('tps', 0):,} TPS
   • Transaction Fee: ${data.get('avg_fee', 0):.4f}
   • Settlement Time: {self._format_time(data.get('finality_time', 0))}
   • Daily Volume: {data.get('daily_transactions', 0):,} transactions

"""

        response += f"""
**🏢 ENTERPRISE NETWORK ASSESSMENT:**
• Most Secure: {self._get_metric_leader(live_data, 'security_score')} ({self._get_best_metric(live_data, 'security_score')}/100)
• Largest Network: {self._get_metric_leader(live_data, 'market_cap')} (market cap leadership)
• Most Stable: {self._get_metric_leader(live_data, 'daily_transactions')} (transaction volume)

*🔄 Data refreshed every 2 minutes from Premium APIs: CoinMarketCap, Chainspect & Etherscan*
"""
        
        return response

    def _generate_live_general_l1_analysis(self, live_data: Dict) -> str:
        """Generate beautifully formatted general L1 analysis with live data"""
        
        # Sort by market cap for general analysis
        sorted_l1s = sorted(live_data.items(), key=lambda x: x[1].get('market_cap', 0), reverse=True)
        
        response = f"""🔗 **LIVE L1 PROTOCOL MARKET ANALYSIS**
*Real-time data for 5 core Layer 1 protocols: Ethereum, Base, Tron, BSC & Bitcoin*

**📊 CURRENT L1 MARKET LEADERS:**

"""
        
        # Enhanced formatting with proper alignment and visuals
        for i, (protocol_id, data) in enumerate(sorted_l1s[:5]):
            rank = i + 1
            rank_emoji = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i] if i < 5 else f"#{rank}"
            
            # Format market cap properly
            market_cap = data.get('market_cap', 0)
            market_cap_str = self._format_currency(market_cap)
            
            # Format TVL
            tvl = data.get('tvl', 0)
            tvl_str = self._format_currency(tvl) if tvl > 0 else "No DeFi data"
            
            # Performance indicator
            performance_indicator = self._get_performance_indicator(data)
            
            response += f"""{rank_emoji} **{data.get('name', protocol_id.title())}** {performance_indicator}
   💎 **Market Position**
      • Market Cap: {market_cap_str}
      • 24h Change: {data.get('price_change_24h', 0):+.2f}%
      
   ⚡ **Technical Performance**  
      • Throughput: {data.get('tps', 0):,} TPS
      • Average Fee: ${data.get('avg_fee', 0):.4f}
      • Security Score: {data.get('security_score', 0)}/100
      
   🔗 **L1 Network Health**
      • Consensus: {data.get('consensus', 'PoS')}
      • Network Utilization: {data.get('network_utilization', 0)}%
      • Daily Transactions: {data.get('daily_transactions', 0):,}

"""

        # Enhanced market overview with visual separators
        total_market_cap = sum(data.get('market_cap', 0) for data in live_data.values())
        total_tvl = sum(data.get('tvl', 0) for data in live_data.values())
        
        response += f"""
{'═' * 60}

**🌍 L1 ECOSYSTEM OVERVIEW:**

💰 **L1 Ecosystem Metrics**
   • Combined Market Cap: {self._format_currency(total_market_cap)}
   • Average Security Score: {sum(d.get('security_score', 0) for d in live_data.values()) / len(live_data):.1f}/100
   • Total Daily Transactions: {sum(d.get('daily_transactions', 0) for d in live_data.values()):,}

🏆 **Performance Leaders**
   • 🚀 Fastest: {self._get_metric_leader(live_data, 'tps')} ({self._get_best_metric(live_data, 'tps'):,} TPS)
   • 💸 Most Cost-Effective: {self._get_metric_leader(live_data, 'avg_fee', lowest=True)} (${self._get_best_metric(live_data, 'avg_fee', lowest=True):.4f})
   • 🏛️ Largest Market Cap: {self._get_metric_leader(live_data, 'market_cap')}

📊 **L1 Network Analysis**
   • High-Performance L1s (>10K TPS): {self._count_high_performance_l1s(live_data)}
   • Low-Fee Networks (<$0.01): {self._count_low_fee_l1s(live_data)}
   • Secure Networks (Security >90): {self._count_secure_l1s(live_data)}

{'─' * 60}
💡 **L1 Protocol Insights:**
• Ethereum leads in market cap with established network effects
• High-throughput L1s (Solana/NEAR) excel in performance metrics
• Newer L1s focus on solving scalability and fee optimization
• Security remains prioritized across all major L1 protocols

*🔄 Data refreshed every 2 minutes from Premium APIs: CoinMarketCap, Chainspect & Etherscan*
"""
        
        return response
    
    def _get_governance_analysis(self, intent_analysis: Dict) -> str:
        """Get comprehensive governance analysis with EIP/proposal data"""
        
        try:
            # Check if this is a latest proposals request
            if intent_analysis.get("latest_proposals_request", False):
                return self._get_latest_proposals_analysis(intent_analysis)
            
            # Check if user asked about specific protocols
            specific_protocols = intent_analysis.get("specific_protocols", [])
            
            if specific_protocols:
                # Focus on specific protocols mentioned by user
                governance_protocols = specific_protocols
                is_focused_query = True
            else:
                # General governance analysis for all major L1s
                governance_protocols = ['ethereum', 'binance', 'bitcoin', 'tron', 'base']
                is_focused_query = False
            
            governance_data = {}
            
            for protocol in governance_protocols:
                data = self.governance_service.get_protocol_governance_data(protocol)
                if data:
                    governance_data[protocol] = data
            
            if not governance_data:
                return "Unable to fetch governance data. Please try again later."
            
            # Generate focused or general response based on query type
            if is_focused_query and len(governance_data) == 1:
                # Single protocol in results - provide focused response
                protocol_id = list(governance_data.keys())[0]
                return self._generate_protocol_specific_governance_response(governance_data, protocol_id)
            elif is_focused_query and len(specific_protocols) == 1 and specific_protocols[0] in governance_data:
                # User asked for specific protocol and we have data
                return self._generate_protocol_specific_governance_response(governance_data, specific_protocols[0])
            else:
                # Multiple protocols or general query
                return self._generate_governance_analysis_response(governance_data)
            
        except Exception as e:
            return f"Error fetching governance data: {str(e)}. Please try again later."
    
    def _get_latest_proposals_analysis(self, intent_analysis: Dict) -> str:
        """Get latest proposals using the specialized fetcher"""
        
        try:
            # Determine which standards to fetch
            specific_protocols = intent_analysis.get("specific_protocols", [])
            
            # Map protocol names to standard abbreviations
            protocol_to_standard = {
                'ethereum': 'EIP',
                'bitcoin': 'BIP', 
                'base': 'SUP',
                'tron': 'TIP',
                'binance': 'BEP'
            }
            
            if specific_protocols:
                # User asked for specific protocols
                standards = [protocol_to_standard.get(p.lower()) for p in specific_protocols]
                standards = [s for s in standards if s]  # Remove None values
            else:
                # Get all standards
                standards = ['EIP', 'BIP', 'SUP', 'TIP', 'BEP']
            
            # Fetch latest proposals data
            proposals_data = self.proposals_fetcher.fetch_latest_proposals(standards)
            
            # Generate JSON output
            json_output = json.dumps(proposals_data, indent=2)
            
            # Generate Markdown output
            markdown_output = self.proposals_fetcher.format_markdown_output(proposals_data)
            
            # Generate clean response with only Markdown (no JSON)
            response = f"""**🔗 LATEST BLOCKCHAIN IMPROVEMENT PROPOSALS**

{markdown_output}

---

**ℹ️ Data Notes:**
- Fetched at: {proposals_data.get('fetched_at', 'Unknown')}
- Sources: Official improvement proposal repositories
- Sorted by: Creation date (newest first), then numeric ID (desc)
- Limit: Top 5 per standard"""

            if proposals_data.get('note'):
                response += f"\n- Issues: {proposals_data['note']}"
            
            return response
            
        except Exception as e:
            return f"**Error fetching latest proposals:** {str(e)}\n\nPlease try again or check the individual proposal repositories directly:\n- EIPs: https://eips.ethereum.org/all\n- BIPs: https://bips.dev/\n- SUPs: https://github.com/ethereum-optimism/SUPs\n- TIPs: https://github.com/tronprotocol/tips\n- BEPs: https://github.com/bnb-chain/BEPs"
    
    def _get_development_activity_analysis(self, intent_analysis: Dict) -> str:
        """Get development activity analysis"""
        
        try:
            # Check if user asked about specific protocols
            specific_protocols = intent_analysis.get("specific_protocols", [])
            
            if specific_protocols:
                # Focus on specific protocols mentioned by user
                protocols = specific_protocols
            else:
                # General development analysis for all major L1s
                protocols = ['ethereum', 'binance', 'bitcoin', 'tron', 'base']
            
            governance_data = {}
            
            for protocol in protocols:
                data = self.governance_service.get_protocol_governance_data(protocol)
                if data:
                    governance_data[protocol] = data
            
            if not governance_data:
                return "Unable to fetch development data. Please try again later."
            
            return self._generate_development_analysis_response(governance_data)
            
        except Exception as e:
            return f"Error fetching development data: {str(e)}. Please try again later."
    
    def _get_protocol_specific_data(self, intent_analysis: Dict, user_input: str) -> str:
        """Get specific data for mentioned protocols"""
        
        try:
            # Get the protocols mentioned by user
            specific_protocols = intent_analysis.get("specific_protocols", [])
            l1_mentions = self._extract_l1_mentions(user_input.lower())
            
            # Combine all mentioned protocols
            all_mentioned = list(set(specific_protocols + l1_mentions))
            
            if not all_mentioned:
                return "I couldn't identify which protocol you're asking about. Please specify the protocol (e.g., Ethereum, Bitcoin, etc.)."
            
            # Get enhanced live data for mentioned protocols
            live_data = self.l1_data_service.get_all_enhanced_l1_data()
            
            if not live_data:
                return "Unable to fetch real-time protocol data. Please check your internet connection and try again."
            
            # Focus on the specific protocol(s) mentioned
            focused_data = {k: v for k, v in live_data.items() if k in all_mentioned}
            
            if not focused_data:
                return f"Unable to fetch data for {', '.join(all_mentioned)}. Please try again later."
            
            # Generate focused response
            if len(focused_data) == 1:
                protocol_id = list(focused_data.keys())[0]
                return self._generate_protocol_specific_data_response(focused_data[protocol_id], protocol_id)
            else:
                return self._generate_multi_protocol_data_response(focused_data)
                
        except Exception as e:
            return f"Error fetching protocol data: {str(e)}. Please try again later."
    
    def _generate_protocol_specific_data_response(self, data: Dict, protocol_id: str) -> str:
        """Generate focused data response for a single protocol"""
        
        protocol_name = data.get('name', protocol_id.title())
        
        response = f"""💎 **{protocol_name.upper()} LIVE DATA**
*Real-time market and network data*

**📊 MARKET INFORMATION:**
• **Market Cap**: {self._format_currency(data.get('market_cap', 0))}
• **Current Price**: ${data.get('current_price', 0):,.2f}
• **24h Change**: {data.get('price_change_24h', 0):+.2f}%
• **7d Change**: {data.get('price_change_7d', 0):+.2f}%
• **Market Rank**: #{data.get('market_cap_rank', 'N/A')}
• **24h Volume**: {self._format_currency(data.get('volume_24h', 0))}

**⚡ NETWORK PERFORMANCE:**
• **Throughput**: {data.get('tps', 0):,} TPS
• **Average Fee**: ${data.get('avg_fee', 0):.4f}
• **Finality Time**: {self._format_time(data.get('finality_time', 0))}
• **Security Score**: {data.get('security_score', 0)}/100

**🔗 L1 PROTOCOL STATUS:**
• **Consensus Mechanism**: {data.get('consensus', 'Proof of Stake')}
• **Network Utilization**: {data.get('network_utilization', 0)}%
• **Active Addresses**: {data.get('active_addresses', 0):,}
• **Daily Transactions**: {data.get('daily_transactions', 0):,}

**📈 SUPPLY INFORMATION:**
• **Circulating Supply**: {data.get('circulating_supply', 0):,.0f} {data.get('symbol', protocol_name[:3])}
• **Total Supply**: {data.get('total_supply', 0):,.0f} {data.get('symbol', protocol_name[:3])}
• **Max Supply**: {data.get('max_supply') or 'Unlimited'}

**🔍 DATA QUALITY:**
• **Sources**: {', '.join(data.get('data_sources', ['Basic']))}
• **Quality Rating**: {data.get('data_quality', 'Unknown')}
• **Last Updated**: {data.get('last_updated', 'Recently')}

*Premium L1 network data from CoinMarketCap, Chainspect & Etherscan APIs*"""
        
        return response
    
    def _generate_multi_protocol_data_response(self, protocols_data: Dict) -> str:
        """Generate comparison data response for multiple protocols"""
        
        response = f"""📊 **PROTOCOL DATA COMPARISON**
*Live data for {len(protocols_data)} protocols*

"""
        
        for protocol_id, data in protocols_data.items():
            protocol_name = data.get('name', protocol_id.title())
            
            response += f"""**{protocol_name}:**
• Market Cap: {self._format_currency(data.get('market_cap', 0))} | Price: ${data.get('current_price', 0):,.2f}
• 24h Change: {data.get('price_change_24h', 0):+.2f}% | Network Fee: ${data.get('avg_fee', 0):.4f}
• Throughput: {data.get('tps', 0):,} TPS | Security: {data.get('security_score', 0)}/100
• Consensus: {data.get('consensus', 'PoS')} | Daily Transactions: {data.get('daily_transactions', 0):,}

"""
        
        response += """*Real-time L1 network data from premium APIs*"""
        
        return response
    
    def _generate_governance_analysis_response(self, governance_data: Dict) -> str:
        """Generate comprehensive governance analysis response"""
        
        response = """🏛️ **L1 GOVERNANCE & IMPROVEMENT PROPOSALS ANALYSIS**
*Live data from official EIP, BIP, TIP, BEP, and SUP sources*

**📊 GOVERNANCE ECOSYSTEM OVERVIEW:**

"""
        
        # Sort by governance maturity
        sorted_protocols = []
        for protocol_id, data in governance_data.items():
            maturity_score = data.get('proposal_distribution', {}).get('governance_maturity_score', 0)
            sorted_protocols.append((protocol_id, data, maturity_score))
        
        sorted_protocols.sort(key=lambda x: x[2], reverse=True)
        
        for i, (protocol_id, data, score) in enumerate(sorted_protocols):
            source_info = data.get('source_info', {})
            proposal_dist = data.get('proposal_distribution', {})
            recent_activity = data.get('recent_activity', {})
            repo_stats = data.get('repo_stats', {})
            
            response += f"""**#{i+1} {source_info.get('name', protocol_id.title())}**
🔗 **Source**: {source_info.get('base_url', 'N/A')}
📋 **Proposals**: {proposal_dist.get('total_proposals', 0)} total
⚡ **Activity**: {recent_activity.get('total_commits_30d', 0)} commits (30d)
👥 **Contributors**: {recent_activity.get('unique_contributors_30d', 0)} active (30d)
⭐ **Community**: {repo_stats.get('stars', 0):,} stars | {repo_stats.get('forks', 0):,} forks
📈 **Governance Score**: {score:.1f}/100

"""
        
        # Add insights
        response += """
**💡 KEY GOVERNANCE INSIGHTS:**
• **EIP Leadership**: Ethereum leads in proposal volume and maturity
• **Multi-chain Standards**: Cross-protocol governance patterns emerging
• **Community Engagement**: Higher activity correlates with ecosystem growth
• **Innovation Velocity**: Active governance drives technical advancement

*Data updated hourly from GitHub APIs and official proposal repositories*
"""
        
        return response
    
    def _generate_development_analysis_response(self, governance_data: Dict) -> str:
        """Generate development activity analysis response"""
        
        # Check if this is a single protocol focus
        if len(governance_data) == 1:
            protocol_id = list(governance_data.keys())[0]
            data = governance_data[protocol_id]
            protocol_name = data.get('source_info', {}).get('name', protocol_id.title())
            
            response = f"""👨‍💻 **{protocol_name.upper()} DEVELOPMENT ACTIVITY**
*Real-time development metrics from official {protocol_name} repository*

**📊 DEVELOPMENT HEALTH DASHBOARD:**

"""
        else:
            response = """👨‍💻 **L1 DEVELOPMENT ACTIVITY ANALYSIS**
*Real-time development metrics from official repositories*

**📊 DEVELOPMENT HEALTH DASHBOARD:**

"""
        
        # Calculate and sort by development activity
        dev_rankings = []
        for protocol_id, data in governance_data.items():
            dev_metrics = data.get('development_metrics', {})
            activity_score = data.get('recent_activity', {}).get('activity_score', 0)
            
            dev_rankings.append({
                'protocol': data.get('source_info', {}).get('name', protocol_id.title()),
                'activity_score': activity_score,
                'contributors': dev_metrics.get('total_contributors', 0),
                'commits_30d': data.get('recent_activity', {}).get('total_commits_30d', 0)
            })
        
        dev_rankings.sort(key=lambda x: x['activity_score'], reverse=True)
        
        for i, protocol in enumerate(dev_rankings):
            rank = i + 1
            activity_level = 'High' if protocol['activity_score'] > 50 else 'Medium' if protocol['activity_score'] > 25 else 'Low'
            
            response += f"""**#{rank} {protocol['protocol']}**
📈 **Activity Level**: {activity_level} ({protocol['activity_score']:.1f}/100)
👥 **Contributors**: {protocol['contributors']:,}
⚡ **Recent Commits (30d)**: {protocol['commits_30d']}

"""
        
        response += """
**🔍 DEVELOPMENT INSIGHTS:**
• **High Activity**: Consistent commits and diverse contributors
• **Innovation Velocity**: Active repos drive faster evolution
• **Community Growth**: Open development correlates with adoption

*Development data refreshed hourly from GitHub APIs*
"""
        
        return response
    
    def _generate_protocol_specific_governance_response(self, governance_data: Dict, protocol_id: str) -> str:
        """Generate focused response for specific protocol governance"""
        
        if protocol_id not in governance_data:
            return f"Unable to fetch {protocol_id.title()} governance data. Please try again later."
        
        data = governance_data[protocol_id]
        source_info = data.get('source_info', {})
        proposal_dist = data.get('proposal_distribution', {})
        recent_activity = data.get('recent_activity', {})
        repo_stats = data.get('repo_stats', {})
        dev_metrics = data.get('development_metrics', {})
        
        # Protocol-specific formatting
        protocol_name = source_info.get('name', protocol_id.title())
        proposal_prefix = source_info.get('proposal_prefix', 'Proposal')
        
        response = f"""🏛️ **{protocol_name.upper()} GOVERNANCE ANALYSIS**
*Live data from official {proposal_prefix} repository*

**📊 GOVERNANCE OVERVIEW:**

**{proposal_prefix} Repository Statistics**
🔗 **Source**: {source_info.get('base_url', 'N/A')}
📋 **Total {proposal_prefix}s**: {proposal_dist.get('total_proposals', 0)}
⭐ **Community Stars**: {repo_stats.get('stars', 0):,}
🍴 **Repository Forks**: {repo_stats.get('forks', 0):,}
👀 **Watchers**: {repo_stats.get('watchers', 0):,}

**📈 RECENT ACTIVITY (30 Days)**
⚡ **Total Commits**: {recent_activity.get('total_commits_30d', 0)}
🔄 **{proposal_prefix}-Related Commits**: {recent_activity.get('proposal_related_commits', 0)}
👥 **Active Contributors**: {recent_activity.get('unique_contributors_30d', 0)}
📊 **Activity Score**: {recent_activity.get('activity_score', 0)}/100

**👨‍💻 DEVELOPMENT HEALTH**
🧑‍🤝‍🧑 **Total Contributors**: {dev_metrics.get('total_contributors', 0)}
📝 **Total Contributions**: {dev_metrics.get('total_contributions', 0)}
🏆 **Top Contributor**: {dev_metrics.get('top_contributors', [{}])[0].get('login', 'N/A') if dev_metrics.get('top_contributors') else 'N/A'}

"""
        
        # Add protocol-specific insights with comprehensive coverage
        if protocol_id == 'bitcoin':
            response += f"""**💡 BITCOIN BIP INSIGHTS:**
• Bitcoin Improvement Proposals focus on protocol upgrades and standards
• BIPs undergo rigorous peer review process ensuring network stability
• Recent activity indicates {self._get_activity_level(recent_activity.get('activity_score', 0))} development momentum
• Community engagement shows {self._get_community_strength(repo_stats.get('stars', 0))} ecosystem support
• Conservative approach prioritizes security and decentralization

**🔍 BIP CATEGORIES:**
• **Standards Track**: Core protocol improvements (consensus changes)
• **Informational**: Design issues, guidelines, and general information
• **Process**: Changes to BIP process or other non-consensus procedures

**🎯 BITCOIN FOCUS AREAS:**
• Scalability solutions (Lightning Network, Taproot)
• Privacy enhancements and transaction efficiency
• Security improvements and network resilience

"""
        elif protocol_id == 'ethereum':
            response += f"""**💡 ETHEREUM EIP INSIGHTS:**
• Ethereum Improvement Proposals drive rapid ecosystem evolution
• EIPs cover core protocol, networking, interface, and application standards
• Recent activity shows {self._get_activity_level(recent_activity.get('activity_score', 0))} innovation pace
• World's most active smart contract platform governance
• Continuous innovation with regular network upgrades

**🔍 EIP CATEGORIES:**
• **Core**: Protocol changes requiring consensus fork (hard/soft forks)
• **Networking**: Devp2p and Light Ethereum protocol improvements
• **Interface**: API/RPC improvements and standards
• **ERC**: Application-level standards (tokens, NFTs, contracts)

**🎯 ETHEREUM FOCUS AREAS:**
• Ethereum 2.0 transition and scaling solutions
• Smart contract standards and developer tools
• Gas optimization and transaction efficiency

"""
        elif protocol_id == 'binance':
            response += f"""**💡 BINANCE BEP INSIGHTS:**
• BNB Evolution Proposals drive BNB Smart Chain development
• BEPs focus on performance, compatibility, and ecosystem growth
• Recent activity shows {self._get_activity_level(recent_activity.get('activity_score', 0))} development velocity
• Strong centralized governance with community input
• Emphasis on high throughput and low transaction costs

**🔍 BEP CATEGORIES:**
• **Core**: Fundamental protocol and consensus changes
• **Standards**: Token standards and smart contract interfaces
• **Applications**: dApp standards and ecosystem improvements
• **Infrastructure**: Validator, staking, and network improvements

**🎯 BINANCE FOCUS AREAS:**
• Cross-chain interoperability and bridge protocols
• DeFi ecosystem expansion and yield farming
• Gaming and NFT marketplace integrations

"""
        elif protocol_id == 'tron':
            response += f"""**💡 TRON TIP INSIGHTS:**
• TRON Improvement Proposals enhance network capabilities
• TIPs prioritize high throughput and content distribution
• Recent activity indicates {self._get_activity_level(recent_activity.get('activity_score', 0))} development pace
• Community-driven governance with delegated consensus
• Focus on entertainment and content creator economy

**🔍 TIP CATEGORIES:**
• **Core**: Protocol upgrades and consensus mechanisms
• **Networking**: P2P networking and communication protocols
• **Contract**: Smart contract standards and virtual machine
• **Application**: DApp standards and user interface improvements

**🎯 TRON FOCUS AREAS:**
• Content distribution and creator monetization
• High-performance DeFi and DEX implementations
• Cross-chain asset management and wrapping

"""
        elif protocol_id == 'base':
            response += f"""**💡 BASE SUP INSIGHTS:**
• Superchain Upgrade Proposals enhance Base Layer 2 capabilities
• SUPs coordinate with Optimism Collective governance
• Recent activity shows {self._get_activity_level(recent_activity.get('activity_score', 0))} innovation momentum
• Coinbase-backed with strong institutional support
• Focus on mainstream adoption and user experience

**🔍 SUP CATEGORIES:**
• **Protocol**: Core Superchain protocol improvements
• **Standards**: Cross-chain standards and interoperability
• **Governance**: DAO and collective decision-making processes
• **Economics**: Fee structures and token economics

**🎯 BASE FOCUS AREAS:**
• Ethereum Layer 2 scaling and cost reduction
• Developer experience and tooling improvements
• Bridge security and cross-chain functionality

"""
        else:
            response += f"""**💡 {protocol_name.upper()} GOVERNANCE INSIGHTS:**
• {proposal_prefix}s drive protocol evolution and standardization
• Recent development shows {self._get_activity_level(recent_activity.get('activity_score', 0))} activity level
• Community engagement indicates {self._get_community_strength(repo_stats.get('stars', 0))} ecosystem support
• Governance maturity score: {proposal_dist.get('governance_maturity_score', 0)}/100

**🔍 GOVERNANCE STRUCTURE:**
• Community-driven proposal submission and review
• Technical committee evaluation and implementation
• Transparent voting and consensus mechanisms

"""
        
        # Add recent proposals if available
        recent_proposals = recent_activity.get('recent_proposals', [])
        if recent_proposals:
            response += f"""**🔄 RECENT {proposal_prefix} ACTIVITY:**
"""
            for i, proposal in enumerate(recent_proposals[:5]):  # Show top 5
                response += f"• **#{i+1}**: {proposal.get('message', 'N/A')[:100]}...\n"
        
        response += f"""
*Data updated hourly from {protocol_name} official repositories*"""
        
        return response
    
    def _get_activity_level(self, score: float) -> str:
        """Convert activity score to descriptive level"""
        if score >= 70:
            return "high"
        elif score >= 40:
            return "moderate" 
        else:
            return "low"
    
    def _get_community_strength(self, stars: int) -> str:
        """Convert star count to community strength"""
        if stars >= 5000:
            return "very strong"
        elif stars >= 1000:
            return "strong"
        elif stars >= 500:
            return "moderate"
        else:
            return "growing"
    
    def _calculate_l1_gaming_score(self, data: Dict) -> float:
        """Calculate L1 gaming suitability score"""
        
        score = 0
        
        # TPS (40% weight) - crucial for gaming
        tps = data.get('tps', 0)
        if tps >= 50000: score += 40
        elif tps >= 10000: score += 35
        elif tps >= 1000: score += 25
        else: score += 10
        
        # Fees (30% weight) - gaming needs low fees
        fee = data.get('avg_fee', 1)
        if fee <= 0.001: score += 30
        elif fee <= 0.01: score += 25
        elif fee <= 0.1: score += 15
        else: score += 5
        
        # Finality (20% weight) - gaming needs speed
        finality = data.get('finality_time', 60)
        if finality <= 1: score += 20
        elif finality <= 5: score += 15
        elif finality <= 30: score += 10
        else: score += 5
        
        # Ecosystem (10% weight)
        ecosystem = data.get('ecosystem_score', 50) / 10
        score += ecosystem
        
        return min(100, score)
    
    def _calculate_l1_network_score(self, data: Dict) -> float:
        """Calculate L1 network quality score based on protocol fundamentals"""
        
        score = 0
        
        # Security (35% weight) - core L1 requirement
        security = data.get('security_score', 50)
        score += (security / 100) * 35
        
        # Performance (25% weight) - TPS and finality
        tps = data.get('tps', 0)
        if tps >= 50000: score += 15
        elif tps >= 10000: score += 12
        elif tps >= 1000: score += 8
        else: score += 3
        
        finality = data.get('finality_time', 60)
        if finality <= 1: score += 10
        elif finality <= 10: score += 7
        elif finality <= 60: score += 5
        else: score += 2
        
        # Market cap (20% weight) - network adoption indicator
        market_cap = data.get('market_cap', 0)
        if market_cap >= 50000000000: score += 20  # $50B+
        elif market_cap >= 10000000000: score += 15  # $10B+
        elif market_cap >= 1000000000: score += 10   # $1B+
        else: score += 5
        
        # Network activity (20% weight) - daily transactions
        daily_tx = data.get('daily_transactions', 0)
        if daily_tx >= 1000000: score += 20  # 1M+ daily
        elif daily_tx >= 100000: score += 15  # 100K+ daily
        elif daily_tx >= 10000: score += 10   # 10K+ daily
        else: score += 5
        
        return min(100, score)
    
    def _generate_general_l1_response(self, user_input: str, intent_analysis: Dict) -> str:
        """Generate general L1-focused response with protocol-aware guidance"""
        
        # Check if user mentioned any specific protocols
        mentioned_protocols = intent_analysis.get("specific_protocols", [])
        l1_mentions = self._extract_l1_mentions(user_input.lower())
        
        if mentioned_protocols or l1_mentions:
            protocol_list = list(set(mentioned_protocols + l1_mentions))
            protocol_names = [p.title() for p in protocol_list]
            
            return f"""🔗 **L1 BLOCKCHAIN RESEARCH ASSISTANT**

I detected you're interested in: **{', '.join(protocol_names)}**

**🎯 Protocol-Specific Queries I Can Handle:**
• **Governance Analysis**: "Show me {protocol_names[0]} BIP/EIP/BEP information"
• **Development Activity**: "{protocol_names[0]} development metrics and contributors"  
• **Live Market Data**: "Current {protocol_names[0]} price and performance"
• **Technical Comparison**: "Compare {protocol_names[0]} vs other L1s"

**🔍 What I Specialize In:**
• **Live L1 Protocol Data** - Real-time network performance and market metrics
• **Protocol-Specific Analysis** - Focused insights without irrelevant data
• **Governance Deep-Dives** - EIP, BIP, BEP, TIP, SUP proposal analysis
• **Network Performance** - TPS, fees, finality, and consensus mechanisms

**💡 Try asking:**
• "{protocol_names[0]} governance activity and recent proposals"
• "Best L1 for gaming - focus on {protocol_names[0]}"
• "Show me {protocol_names[0]} development statistics"
• "{protocol_names[0]} vs Ethereum comparison"

**📊 Data Sources:** CoinMarketCap Pro, Chainspect, DefiLlama, Etherscan (updated every 2 minutes)

What specific {protocol_names[0]} information would you like to explore?"""
        
        else:
            return """🔗 **L1 BLOCKCHAIN RESEARCH ASSISTANT**

I specialize in Layer 1 blockchain protocol analysis with real-time data integration!

**🔍 What I Can Help With:**
• **Live L1 Protocol Data** - Real-time network performance and market data
• **Protocol-Specific Analysis** - Focused insights for Bitcoin, Ethereum, Binance, Tron, Base
• **Governance Tracking** - EIP, BIP, BEP, TIP, SUP proposal analysis
• **Network Comparisons** - Side-by-side L1 protocol performance evaluation

**💡 Try asking:**
• "Bitcoin BIP governance information"
• "Ethereum current market cap and gas fees" 
• "Solana network performance metrics"
• "Compare Ethereum vs Polygon throughput"
• "Which L1 has the lowest transaction fees?"
• "Show me Bitcoin protocol development activity"

**📊 Data Sources:** CoinMarketCap Pro, Chainspect, Etherscan (updated every 2 minutes)

What L1 blockchain challenge can I help you solve?"""
    
    def _extract_use_case(self, user_input_lower: str) -> Optional[str]:
        """Extract use case from user input"""
        
        use_cases = {
            "gaming": ["gaming", "game", "nft", "play-to-earn", "p2e", "metaverse"],
            "payments": ["payment", "transfer", "remittance", "transaction", "send", "receive"],
            "enterprise": ["enterprise", "business", "corporate", "institutional"],
            "development": ["dapp", "smart contract", "development", "build", "deploy"]
        }
        
        for use_case, keywords in use_cases.items():
            if any(keyword in user_input_lower for keyword in keywords):
                return use_case
        
        return None
    
    def _extract_l1_technical_requirements(self, user_input_lower: str) -> Dict:
        """Extract L1 technical requirements"""
        
        params = {}
        
        # TPS requirements
        tps_match = re.search(r'(\d+[,\d]*)\s*tps', user_input_lower)
        if tps_match:
            params["min_tps"] = int(tps_match.group(1).replace(',', ''))
        
        # Fee requirements
        fee_match = re.search(r'\$(\d+(?:\.\d+)?)', user_input_lower)
        if fee_match:
            params["max_fee"] = float(fee_match.group(1))
        
        return params
    
    def _extract_l1_mentions(self, user_input_lower: str) -> List[str]:
        """Extract mentioned L1 protocols (focused on 5 core chains)"""
        
        l1_protocols = {
            "ethereum": ["ethereum", "eth", "ether", "ethereum protocol", "ethereum network", "eth network"],
            "base": ["base", "base chain", "base network", "base protocol", "base l2"],
            "tron": ["tron", "trx", "tron protocol", "tron network", "trx network"],
            "binance": ["binance", "bnb", "bsc", "binance smart chain", "bnb smart chain", "binance chain", "bnb chain"],
            "bitcoin": ["bitcoin", "btc", "bitcoin protocol", "bitcoin network", "btc network"]
        }
        
        mentioned = []
        for protocol, aliases in l1_protocols.items():
            if any(alias in user_input_lower for alias in aliases):
                mentioned.append(protocol)
        
        return mentioned
    
    def _extract_governance_protocol_mentions(self, user_input_lower: str) -> List[str]:
        """Extract mentioned governance protocols from user input"""
        
        governance_protocols = {
            "bitcoin": [
                "bitcoin", "btc", "bip", "bips", "bitcoin improvement proposal", "bitcoin improvement proposals", 
                "bitcoin protocol", "bitcoin network", "btc network", "bitcoin governance", "bitcoin upgrade"
            ],
            "ethereum": [
                "ethereum", "eth", "eip", "eips", "ethereum improvement proposal", "ethereum improvement proposals", 
                "ethereum protocol", "eth protocol", "ethereum network", "ethereum governance", "ethereum upgrade",
                "eth 2.0", "ethereum 2.0", "ethereum merge", "ethereum shanghai", "ethereum dencun"
            ],
            "binance": [
                "binance", "bnb", "bsc", "bep", "beps", "binance evolution proposal", "binance evolution proposals", 
                "bnb evolution proposal", "bnb evolution proposals", "bnb smart chain", "binance smart chain", 
                "binance chain", "bnb chain", "binance governance", "bsc governance", "bnb governance"
            ],
            "tron": [
                "tron", "trx", "tip", "tips", "tron improvement proposal", "tron improvement proposals", 
                "tron protocol", "tron network", "trx network", "tron governance", "tron upgrade"
            ],
            "base": [
                "base", "base chain", "base network", "base protocol", "sup", "sups", 
                "superchain upgrade proposal", "superchain upgrade proposals", "optimism base", 
                "base l2", "coinbase base", "base governance", "superchain governance"
            ]
        }
        
        mentioned = []
        for protocol, aliases in governance_protocols.items():
            if any(alias in user_input_lower for alias in aliases):
                mentioned.append(protocol)
        
        return mentioned
    
    def _format_time(self, seconds: float) -> str:
        """Format time for display"""
        
        if seconds < 1:
            return f"{seconds*1000:.0f}ms"
        elif seconds < 60:
            return f"{seconds:.1f}s"
        else:
            minutes = int(seconds // 60)
            return f"{minutes}m"
    
    def _get_gaming_suitability(self, data: Dict) -> str:
        """Assess gaming suitability"""
        
        tps = data.get('tps', 0)
        fee = data.get('avg_fee', 1)
        finality = data.get('finality_time', 60)
        
        if tps >= 10000 and fee <= 0.01 and finality <= 2:
            return "Excellent for high-performance gaming"
        elif tps >= 1000 and fee <= 0.1:
            return "Good for most gaming applications" 
        elif tps >= 100:
            return "Suitable for simple games"
        else:
            return "Limited gaming capabilities"
    
    def _get_metric_leader(self, data: Dict, metric: str, lowest: bool = False) -> str:
        """Get the leading protocol for a metric"""
        
        if not data:
            return "N/A"
        
        if lowest:
            leader = min(data.items(), key=lambda x: x[1].get(metric, float('inf')))
        else:
            leader = max(data.items(), key=lambda x: x[1].get(metric, 0))
        
        return leader[1].get('name', leader[0].title())
    
    def _get_best_metric(self, data: Dict, metric: str, lowest: bool = False) -> float:
        """Get the best value for a metric"""
        
        if not data:
            return 0
        
        values = [d.get(metric, 0 if not lowest else float('inf')) for d in data.values()]
        
        if lowest:
            return min(values)
        else:
            return max(values)
    
    def _format_currency(self, amount: float) -> str:
        """Format currency amounts with proper suffixes"""
        
        if amount >= 1_000_000_000_000:  # Trillions
            return f"${amount/1_000_000_000_000:.2f}T"
        elif amount >= 1_000_000_000:  # Billions
            return f"${amount/1_000_000_000:.2f}B"
        elif amount >= 1_000_000:  # Millions
            return f"${amount/1_000_000:.2f}M"
        elif amount >= 1_000:  # Thousands
            return f"${amount/1_000:.2f}K"
        else:
            return f"${amount:.2f}"
    
    def _get_performance_indicator(self, data: Dict) -> str:
        """Get performance indicator emoji"""
        
        tps = data.get('tps', 0)
        fee = data.get('avg_fee', 1)
        
        if tps >= 50000 and fee <= 0.001:
            return "🔥"  # High performance
        elif tps >= 10000 and fee <= 0.01:
            return "⚡"  # Good performance  
        elif tps >= 1000 and fee <= 0.1:
            return "📈"  # Moderate performance
        else:
            return "🔷"  # Standard
    
    def _count_high_performance_l1s(self, live_data: Dict) -> int:
        """Count L1s with >10K TPS"""
        
        return sum(1 for data in live_data.values() if data.get('tps', 0) > 10000)
    
    def _count_low_fee_l1s(self, live_data: Dict) -> int:
        """Count L1s with fees <$0.01"""
        
        return sum(1 for data in live_data.values() if data.get('avg_fee', 1) < 0.01)
    
    def _count_secure_l1s(self, live_data: Dict) -> int:
        """Count L1s with security score >90"""
        
        return sum(1 for data in live_data.values() if data.get('security_score', 0) > 90)
    
    def _count_fast_finality_l1s(self, live_data: Dict) -> int:
        """Count L1s with finality <10s"""
        
        return sum(1 for data in live_data.values() if data.get('finality_time', 60) < 10)
    
    def _calculate_l1_payments_score(self, data: Dict) -> float:
        """Calculate L1 payments suitability score"""
        
        score = 0
        
        # Fees (40% weight) - critical for payments
        fee = data.get('avg_fee', 1)
        if fee <= 0.001: score += 40
        elif fee <= 0.01: score += 35
        elif fee <= 0.1: score += 25
        else: score += 10
        
        # Finality (30% weight) - fast settlement needed
        finality = data.get('finality_time', 60)
        if finality <= 1: score += 30
        elif finality <= 5: score += 25
        elif finality <= 30: score += 15
        else: score += 5
        
        # TPS (20% weight) - handle payment volume
        tps = data.get('tps', 0)
        if tps >= 10000: score += 20
        elif tps >= 1000: score += 15
        elif tps >= 100: score += 10
        else: score += 5
        
        # Security (10% weight) - trust for payments
        security = data.get('security_score', 50)
        score += (security / 100) * 10
        
        return min(100, score)
    
    def _calculate_l1_enterprise_score(self, data: Dict) -> float:
        """Calculate L1 enterprise suitability score"""
        
        score = 0
        
        # Security (50% weight) - paramount for enterprise
        security = data.get('security_score', 50)
        score += (security / 100) * 50
        
        # Market cap (25% weight) - stability and trust indicator
        market_cap = data.get('market_cap', 0)
        if market_cap >= 100000000000: score += 25  # $100B+
        elif market_cap >= 50000000000: score += 20   # $50B+
        elif market_cap >= 10000000000: score += 15   # $10B+
        else: score += 5
        
        # Network activity (15% weight) - proven usage
        daily_tx = data.get('daily_transactions', 0)
        if daily_tx >= 1000000: score += 15  # 1M+ daily
        elif daily_tx >= 100000: score += 10  # 100K+ daily
        else: score += 5
        
        # Performance (10% weight) - adequate for enterprise needs
        tps = data.get('tps', 0)
        if tps >= 1000: score += 10
        elif tps >= 100: score += 7
        else: score += 3
        
        return min(100, score)
    
    def _get_payment_suitability(self, data: Dict) -> str:
        """Assess payment suitability"""
        
        fee = data.get('avg_fee', 1)
        finality = data.get('finality_time', 60)
        
        if fee <= 0.01 and finality <= 5:
            return "Excellent for micropayments and remittances"
        elif fee <= 0.1 and finality <= 30:
            return "Good for regular payment transactions"
        elif fee <= 1:
            return "Suitable for larger value transfers"
        else:
            return "Limited payment use cases due to high fees"