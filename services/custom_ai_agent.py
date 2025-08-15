"""
Custom AI Agent for Blockchain Research & Advisory
Focused on proposal fetching and research guidance
"""
import re
import json
from typing import Dict, List, Optional, Any, Tuple
from services.governance_data_service import GovernanceDataService
# from services.latest_proposals_fetcher import LatestProposalsFetcher  # Removed - replaced by scraped data
from services.blockchain_research_advisor import BlockchainResearchAdvisor
import streamlit as st

class CustomBlockchainAIAgent:
    """
    Custom AI agent specialized in blockchain research and proposal analysis
    Provides proposal fetching and research guidance
    """
    
    def __init__(self):
        self.governance_service = GovernanceDataService()
        # self.proposals_fetcher = LatestProposalsFetcher()  # Removed - replaced by scraped data
        self.research_advisor = BlockchainResearchAdvisor()
        self.conversation_context = []
        
    def get_chat_response(self, user_input: str, conversation_history: List[Dict]) -> str:
        """Generate AI response for user query focused on research and proposals"""
        
        try:
            # Analyze user intent
            intent_analysis = self._analyze_user_intent(user_input)
            
            # Route to appropriate handler
            if intent_analysis['type'] == 'proposals':
                return self._handle_proposal_request(user_input, intent_analysis)
            elif intent_analysis['type'] == 'research':
                return self.research_advisor.provide_research_guidance(user_input)
            elif intent_analysis['type'] == 'governance':
                return self._handle_governance_query(user_input, intent_analysis)
            else:
                return self._generate_general_response(user_input)
                
        except Exception as e:
            return f"❌ I encountered an error processing your request: {str(e)}\n\nPlease try rephrasing your question or ask about blockchain proposals or research guidance."
    
    def _analyze_user_intent(self, user_input: str) -> Dict:
        """Analyze user intent to determine appropriate response type"""
        
        query_lower = user_input.lower()
        
        # Proposal-related queries
        if any(term in query_lower for term in ['latest', 'newest', 'recent', 'eip', 'bip', 'sup', 'tip', 'bep', 'lip', 'proposal', 'improvement', 'draft', 'production']):
            return {
                'type': 'proposals',
                'confidence': 0.9,
                'keywords': ['proposals', 'improvements']
            }
        
        # Research guidance queries
        elif any(term in query_lower for term in ['research', 'analyze', 'parameters', 'metrics', 'how to evaluate', 'what to look for']):
            return {
                'type': 'research', 
                'confidence': 0.8,
                'keywords': ['research', 'analysis']
            }
        
        # Governance queries
        elif any(term in query_lower for term in ['governance', 'voting', 'dao', 'community', 'decision']):
            return {
                'type': 'governance',
                'confidence': 0.7,
                'keywords': ['governance']
            }
        
        else:
            return {
                'type': 'general',
                'confidence': 0.5,
                'keywords': []
            }
    
    def _handle_proposal_request(self, user_input: str, intent_analysis: Dict) -> str:
        """Handle requests for latest proposals"""
        
        # Use the research advisor's proposal handling
        return self.research_advisor.provide_research_guidance(user_input)
    
    def _handle_governance_query(self, user_input: str, intent_analysis: Dict) -> str:
        """Handle governance-related queries"""
        
        try:
            # Try to get governance data
            governance_data = self.governance_service.get_governance_overview()
            
            if governance_data:
                return self._generate_governance_response(governance_data)
            else:
                return "# 🏛️ **Blockchain Governance Research**\n\n" + \
                       "I can help you research blockchain governance models and decision-making processes. " + \
                       "Ask me about specific governance mechanisms, voting systems, or DAO structures."
                       
        except Exception as e:
            return "# 🏛️ **Governance Analysis**\n\n" + \
                   "I can provide guidance on blockchain governance research. " + \
                   "What specific aspect of governance would you like to explore?"
    
    def _generate_governance_response(self, governance_data: Dict) -> str:
        """Generate response based on governance data"""
        
        response = "# 🏛️ **Blockchain Governance Overview**\n\n"
        
        if governance_data.get('total_proposals'):
            response += f"**Total Active Proposals**: {governance_data['total_proposals']}\n"
        
        if governance_data.get('active_protocols'):
            response += f"**Protocols Monitored**: {len(governance_data['active_protocols'])}\n\n"
            
            for protocol in governance_data['active_protocols'][:5]:
                name = protocol.get('name', 'Unknown')
                proposal_count = protocol.get('proposal_count', 0)
                response += f"• **{name}**: {proposal_count} active proposals\n"
        
        response += "\n**Ask me about specific governance mechanisms or voting systems!**"
        
        return response
    
    def _generate_general_response(self, user_input: str) -> str:
        """Generate general response for unclear queries"""
        
        return """# 🤖 **Blockchain Research Assistant**

I specialize in helping you research blockchain technology! Here's what I can help with:

## 🔗 **Latest Proposals**
- Get newest EIPs, BIPs, SUPs and other improvement proposals
- Track blockchain protocol updates and changes

## 🔬 **Research Guidance** 
- Framework for analyzing blockchain parameters
- Guidance on consensus mechanisms, security, and performance
- Research methodology for blockchain selection

## 🏛️ **Governance Analysis**
- Blockchain governance models and mechanisms
- DAO structures and voting systems

## 💡 **Try asking:**
- *"Show me the latest EIPs"*
- *"What parameters should I research?"*
- *"Latest Bitcoin proposals"*
- *"How to evaluate blockchain security?"*

**What would you like to research today?**"""
    
    def is_blockchain_related(self, query: str) -> bool:
        """Check if query is blockchain-related"""
        
        blockchain_keywords = [
            'blockchain', 'crypto', 'bitcoin', 'ethereum', 'solana', 'polygon',
            'smart contract', 'defi', 'dao', 'nft', 'consensus', 'mining',
            'proof of stake', 'proof of work', 'layer 1', 'layer 2', 'protocol',
            'eip', 'bip', 'sup', 'proposal', 'improvement', 'governance'
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in blockchain_keywords)
    
    def get_response_confidence(self, query: str) -> float:
        """Calculate confidence score for handling the query"""
        
        if not self.is_blockchain_related(query):
            return 0.1
        
        intent = self._analyze_user_intent(query)
        return intent.get('confidence', 0.5)