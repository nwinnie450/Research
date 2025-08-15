"""
AI Agent for L1 Blockchain Research & Advisory (Phase 1)
Enhanced with real-time L1 data integration while maintaining proposal functionality
"""
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
# from services.latest_proposals_fetcher import LatestProposalsFetcher  # Removed - replaced by scraped data
from services.l1_market_analyzer import L1ProtocolMarketAnalyzer
from services.scraped_data_service import scraped_data_service

class BlockchainResearchAdvisor:
    """
    AI Agent specialized in blockchain research and proposal analysis
    Phase 1: Parameter research and proposal guidance only
    """
    
    def __init__(self):
        # self.proposals_fetcher = LatestProposalsFetcher()  # Removed - replaced by scraped data
        self.market_analyzer = L1ProtocolMarketAnalyzer()
        
        # Enhanced research areas mapping for intent analysis
        self.research_areas = {
            'proposals': ['proposal', 'eip', 'bip', 'sup', 'tip', 'bep', 'latest', 'newest', 'improvement'],
            'tps_ranking': ['tps ranking', 'fastest', 'speed ranking', 'performance ranking', 'throughput ranking', 'top tps'],
            'market_analysis': ['market analysis', 'market cap', 'comparison', 'comprehensive analysis', 'protocol comparison'],
            'protocol_details': ['details about', 'analyze', 'information about', 'tell me about'],
            'consensus': ['consensus', 'proof of work', 'proof of stake', 'pow', 'pos', 'dpos', 'pbft'],
            'performance': ['speed', 'tps', 'throughput', 'scalability', 'transactions per second'],
            'security': ['security', '51% attack', 'double-spending', 'secure', 'safety', 'hack'],
            'fees': ['fee', 'cost', 'transaction cost', 'gas', 'cheap', 'expensive'],
            'ecosystem': ['ecosystem', 'dapps', 'developers', 'community', 'projects'],
            'governance': ['governance', 'voting', 'dao', 'decentralized', 'community control'],
            'privacy': ['privacy', 'anonymous', 'zero-knowledge', 'confidential', 'private'],
            'compliance': ['compliance', 'regulation', 'legal', 'kyc', 'aml', 'regulatory'],
            'interoperability': ['interoperability', 'cross-chain', 'bridge', 'integration'],
            'tokenomics': ['tokenomics', 'token', 'economics', 'inflation', 'supply']
        }
    
    def provide_research_guidance(self, user_query: str) -> str:
        """Main entry point for blockchain research advisory"""
        
        # Analyze the research intent
        research_intent = self._analyze_research_intent(user_query)
        
        if research_intent['type'] == 'proposals':
            return self._handle_proposal_query(research_intent)
        elif research_intent['type'] == 'tps_ranking':
            return self.market_analyzer.get_tps_ranking_analysis()
        elif research_intent['type'] == 'market_analysis':
            return self.market_analyzer.get_comprehensive_l1_analysis()
        elif research_intent['type'] == 'protocol_details':
            protocol_name = self._extract_protocol_name(research_intent['query'])
            if protocol_name:
                return self.market_analyzer.get_protocol_details(protocol_name)
            else:
                return self.market_analyzer.get_tps_ranking_analysis()
        elif research_intent['type'] == 'parameter_research':
            return self._guide_parameter_research(research_intent)
        else:
            return self._provide_general_research_guidance()
    
    def _analyze_research_intent(self, user_query: str) -> Dict:
        """Analyze what kind of blockchain research guidance is needed"""
        
        query_lower = user_query.lower()
        
        # Detect research type
        research_type = 'general'
        
        if any(term in query_lower for term in ['latest', 'newest', 'recent', 'eip', 'bip', 'bep', 'tip', 'sup', 'proposal']):
            research_type = 'proposals'
        elif any(term in query_lower for term in ['tps ranking', 'fastest', 'speed ranking', 'performance ranking', 'top tps', 'rank by tps']):
            research_type = 'tps_ranking'
        elif any(term in query_lower for term in ['market analysis', 'comprehensive analysis', 'protocol comparison', 'market cap']):
            research_type = 'market_analysis'
        elif any(term in query_lower for term in ['details about', 'analyze', 'information about', 'tell me about']) and self._contains_protocol_name(query_lower):
            research_type = 'protocol_details'
        elif any(term in query_lower for term in ['parameter', 'metric', 'what to look for', 'how to evaluate']):
            research_type = 'parameter_research'
        
        # Extract focus areas
        focus_areas = []
        for area, keywords in self.research_areas.items():
            if any(keyword in query_lower for keyword in keywords):
                focus_areas.append(area)
        
        # Extract mentioned proposal types
        proposal_types = []
        if 'eip' in query_lower:
            proposal_types.append('EIP')
        if 'bip' in query_lower:
            proposal_types.append('BIP')  
        if 'sup' in query_lower:
            proposal_types.append('SUP')
        if 'bep' in query_lower:
            proposal_types.append('BEP')
        if 'tip' in query_lower:
            proposal_types.append('TIP')
        
        # Extract status filter
        status_filter = None
        status_keywords = {
            'production': ['production', 'final', 'active', 'enabled', 'closed'],
            'draft': ['draft', 'open'],
            'proposed': ['proposed', 'proposal'],
            'candidate': ['candidate'],
            'enabled': ['enabled'],
            'review': ['review', 'last call'],
            'withdrawn': ['withdrawn', 'rejected', 'abandoned'],
            'superseded': ['superseded', 'replaced'],
            'living': ['living'],
            'stagnant': ['stagnant'],
            'open': ['open'],  # For SUPs and GitHub-based proposals
            'closed': ['closed']  # For TIPs specifically
        }
        
        for status, keywords in status_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                status_filter = status
                break
        
        return {
            'type': research_type,
            'focus_areas': focus_areas,
            'proposal_types': proposal_types,
            'status_filter': status_filter,
            'query': user_query
        }
    
    def _handle_proposal_query(self, intent: Dict) -> str:
        """Handle queries about latest proposals"""
        
        proposal_types = intent.get('proposal_types', [])
        status_filter = intent.get('status_filter')
        
        if not proposal_types:
            # Default to all proposal types if not specified
            proposal_types = ['EIP', 'BIP', 'SUP']
        
        # Build response header with status filter info
        header = "# 🔗 **LATEST BLOCKCHAIN IMPROVEMENT PROPOSALS**\n\n"
        if status_filter:
            header = f"# 🔗 **{status_filter.upper()} BLOCKCHAIN IMPROVEMENT PROPOSALS**\n\n"
        response = header
        
        try:
            # Use scraped data service for proposals
            proposals_by_type = {}
            protocol_map = {
                'EIP': 'ethereum',
                'BIP': 'bitcoin', 
                'TIP': 'tron',
                'BEP': 'binance_smart_chain'
            }
            
            for proposal_type in proposal_types:
                if proposal_type in protocol_map:
                    protocol = protocol_map[proposal_type]
                    proposals = scraped_data_service.get_latest_proposals(
                        protocol, 
                        limit=10,
                        status_filter=status_filter
                    )
                    proposals_by_type[proposal_type] = proposals
            
            for proposal_type in proposal_types:
                proposals = proposals_by_type.get(proposal_type, [])
                # Status filtering is now handled by scraped_data_service
                
                if proposals:
                    status_text = f" ({status_filter.title()} Status)" if status_filter else " (Latest 5)"
                    response += f"## {proposal_type}s{status_text}\n\n"
                    
                    # Show more proposals for better coverage
                    limit = 10 if status_filter else 5  # More results when filtering
                    for proposal in proposals[:limit]:
                        number = proposal.get('number', 'N/A')
                        title = proposal.get('title', f'{proposal_type} {number}')
                        url = proposal.get('url', '#')
                        status = proposal.get('status', 'Unknown')
                        author = proposal.get('author', 'Unknown')
                        
                        response += f"• **{proposal_type}-{number}**: {title}\n"
                        response += f"  - Status: {status} | Author: {author}\n"
                        response += f"  - [📖 View Proposal]({url})\n\n"
                else:
                    status_text = f" with {status_filter} status" if status_filter else ""
                    response += f"## {proposal_type}s\n\n❌ No {proposal_type}s found{status_text} at this time.\n\n"
        
        except Exception as e:
            response += f"❌ Error fetching proposals: {str(e)}\n"
        
        return response
    
    def _guide_parameter_research(self, intent: Dict) -> str:
        """Guide user on what parameters to research"""
        
        focus_areas = intent.get('focus_areas', [])
        
        response = "# 🔬 **Blockchain Analysis Framework**\n\n"
        
        response += "## 🎯 **Key Research Areas**\n\n"
        
        research_framework = {
            'consensus_mechanism': {
                'importance': 'Security, energy efficiency, and decentralization foundation',
                'considerations': 'Evaluate energy efficiency, decentralization level, and security guarantees'
            },
            'transaction_speed': {
                'importance': 'Critical for scalability and high-volume use cases',  
                'considerations': 'Consider both theoretical maximum and real-world sustained throughput'
            },
            'security_features': {
                'importance': 'Trust and reliability foundation',
                'considerations': 'Review attack resistance, economic security, and historical incidents'
            },
            'fee_structure': {
                'importance': 'Cost-effectiveness for different use cases',
                'considerations': 'Analyze fee predictability, gas optimization, and scaling solutions'
            },
            'ecosystem_health': {
                'importance': 'Long-term viability and developer support',
                'considerations': 'Assess developer activity, dApp diversity, and community growth'
            }
        }
        
        # Show relevant research areas based on focus
        if focus_areas:
            response += f"**Based on your interest in: {', '.join(focus_areas)}**\n\n"
            
        for i, (field, info) in enumerate(research_framework.items(), 1):
            if not focus_areas or any(area in field for area in focus_areas):
                response += f"### {i}. {field.replace('_', ' ').title()}\n"
                response += f"**Importance**: {info['importance']}\n"
                response += f"**Key Considerations**: {info['considerations']}\n\n"
        
        response += "## 📋 **Research Methodology**\n\n"
        response += "1. **Define Use Case**: Identify your specific blockchain requirements\n"
        response += "2. **Prioritize Metrics**: Weight different parameters based on your needs\n"
        response += "3. **Gather Live Data**: Use verified sources for real-time network data\n"
        response += "4. **Compare Objectively**: Avoid marketing claims, focus on measurable metrics\n"
        response += "5. **Test Integration**: Consider development complexity and tooling\n"
        
        return response
    
    def _provide_general_research_guidance(self) -> str:
        """Provide general blockchain research guidance"""
        
        response = "# 🧭 **Blockchain Research Guidance**\n\n"
        
        response += "## 🔍 **What I can help you research:**\n\n"
        response += "• **Latest Proposals**: Get newest EIPs, BIPs, SUPs, and other improvement proposals\n"
        response += "• **Live TPS Rankings**: Real-time L1 blockchain performance data with accurate rankings\n"
        response += "• **Market Analysis**: Comprehensive L1 protocol comparison with live data\n"
        response += "• **Protocol Details**: Deep-dive analysis of specific L1 blockchains\n"
        response += "• **Research Framework**: Understand key parameters to analyze when choosing blockchains\n"
        response += "• **Technical Analysis**: Guidance on consensus mechanisms, security, and performance metrics\n\n"
        
        response += "## 💡 **Example queries:**\n\n"
        response += "• *\"Show me the latest EIPs\"*\n"
        response += "• *\"TPS ranking of L1 blockchains\"*\n"
        response += "• *\"Tell me about Solana performance\"*\n"
        response += "• *\"Comprehensive market analysis\"*\n"
        response += "• *\"What parameters should I research for blockchain selection?\"*\n"
        response += "• *\"Latest Bitcoin improvement proposals\"*\n"
        response += "• *\"How to evaluate blockchain security?\"*\n\n"
        
        response += "**Ask me about any blockchain research topic and I'll provide focused guidance!**\n"
        
        return response
    
    def _extract_protocol_name(self, query: str) -> Optional[str]:
        """Extract protocol name from user query"""
        
        protocol_names = [
            'ethereum', 'eth', 'bitcoin', 'btc', 'solana', 'sol', 'cardano', 'ada',
            'polkadot', 'dot', 'avalanche', 'avax', 'binance smart chain', 'bsc', 'bnb',
            'internet computer', 'icp', 'near', 'algorand', 'algo'
        ]
        
        query_lower = query.lower()
        
        for protocol in protocol_names:
            if protocol in query_lower:
                # Map common abbreviations to full names
                name_mapping = {
                    'eth': 'ethereum',
                    'btc': 'bitcoin', 
                    'sol': 'solana',
                    'ada': 'cardano',
                    'dot': 'polkadot',
                    'avax': 'avalanche',
                    'bsc': 'binance smart chain',
                    'bnb': 'binance smart chain',
                    'icp': 'internet computer',
                    'algo': 'algorand'
                }
                
                return name_mapping.get(protocol, protocol)
        
        return None
    
    def _contains_protocol_name(self, query_lower: str) -> bool:
        """Check if query contains a protocol name"""
        
        protocol_names = [
            'ethereum', 'eth', 'bitcoin', 'btc', 'solana', 'sol', 'cardano', 'ada',
            'polkadot', 'dot', 'avalanche', 'avax', 'binance smart chain', 'bsc', 'bnb',
            'internet computer', 'icp', 'near', 'algorand', 'algo'
        ]
        
        return any(protocol in query_lower for protocol in protocol_names)