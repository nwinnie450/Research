"""
Custom AI Agent for Blockchain Research & Advisory
Advanced response generation with detailed analysis and recommendations
Specialized for L1 protocols with real-time data integration
"""
import re
import json
from typing import Dict, List, Optional, Any, Tuple
from config import USE_CASES, BLOCKCHAIN_PROTOCOLS, EVALUATION_PARAMS
from services.realtime_l1_data import RealtimeL1DataService
import streamlit as st

class CustomBlockchainAIAgent:
    """
    Custom AI agent specialized in blockchain analysis and recommendations
    Provides detailed, contextual responses with comprehensive analysis
    """
    
    def __init__(self):
        self.knowledge_base = self._initialize_knowledge_base()
        self.response_templates = self._initialize_response_templates()
        self.conversation_context = []
        self.l1_data_service = RealtimeL1DataService()
        
        # Focus on L1 protocols for specialized analysis
        self.l1_specialization = True
        
    def get_chat_response(self, user_input: str, conversation_history: List[Dict]) -> str:
        """Generate detailed AI response for user query"""
        
        # Update conversation context
        self.conversation_context = conversation_history[-5:]  # Keep last 5 exchanges
        
        # Analyze user intent and extract key information
        intent_analysis = self._analyze_user_intent(user_input)
        
        # Generate contextual response based on intent
        response = self._generate_contextual_response(user_input, intent_analysis)
        
        return response
    
    def extract_search_parameters(self, user_input: str) -> Optional[Dict]:
        """Extract detailed search parameters from natural language"""
        
        params = {}
        user_input_lower = user_input.lower()
        
        # Extract use case with advanced pattern matching
        use_case = self._extract_use_case(user_input_lower)
        if use_case:
            params["use_case"] = use_case
        
        # Extract technical requirements
        technical_params = self._extract_technical_requirements(user_input_lower)
        params.update(technical_params)
        
        # Extract economic requirements  
        economic_params = self._extract_economic_requirements(user_input_lower)
        params.update(economic_params)
        
        # Extract specific blockchain mentions
        mentioned_chains = self._extract_blockchain_mentions(user_input_lower)
        if mentioned_chains:
            params["include_chains"] = mentioned_chains
        
        return params if params else None
    
    def _analyze_user_intent(self, user_input: str) -> Dict:
        """Analyze user intent and categorize the query"""
        
        user_input_lower = user_input.lower()
        
        intent_analysis = {
            "primary_intent": "general_inquiry",
            "use_case": None,
            "comparison_request": False,
            "technical_focus": False,
            "specific_chains": [],
            "detail_level": "medium",
            "urgency": "normal"
        }
        
        # Detect primary intent
        if any(word in user_input_lower for word in ["compare", "vs", "versus", "difference", "better"]):
            intent_analysis["primary_intent"] = "comparison"
            intent_analysis["comparison_request"] = True
        elif any(word in user_input_lower for word in ["best", "recommend", "suggest", "top", "find"]):
            intent_analysis["primary_intent"] = "recommendation"
        elif any(word in user_input_lower for word in ["how", "implement", "build", "develop", "integrate"]):
            intent_analysis["primary_intent"] = "implementation"
            intent_analysis["technical_focus"] = True
        elif any(word in user_input_lower for word in ["what", "explain", "tell me about", "overview"]):
            intent_analysis["primary_intent"] = "explanation"
        
        # Detect use case
        intent_analysis["use_case"] = self._extract_use_case(user_input_lower)
        
        # Detect detail level
        if any(word in user_input_lower for word in ["detailed", "comprehensive", "in-depth", "thorough"]):
            intent_analysis["detail_level"] = "high"
        elif any(word in user_input_lower for word in ["quick", "brief", "summary", "overview"]):
            intent_analysis["detail_level"] = "low"
        
        # Detect specific blockchains mentioned
        intent_analysis["specific_chains"] = self._extract_blockchain_mentions(user_input_lower)
        
        return intent_analysis
    
    def _generate_contextual_response(self, user_input: str, intent_analysis: Dict) -> str:
        """Generate detailed contextual response based on intent analysis"""
        
        primary_intent = intent_analysis["primary_intent"]
        use_case = intent_analysis["use_case"]
        detail_level = intent_analysis["detail_level"]
        
        if primary_intent == "comparison":
            return self._generate_comparison_response(user_input, intent_analysis)
        elif primary_intent == "recommendation":
            return self._generate_recommendation_response(user_input, intent_analysis)
        elif primary_intent == "implementation":
            return self._generate_implementation_response(user_input, intent_analysis)
        elif primary_intent == "explanation":
            return self._generate_explanation_response(user_input, intent_analysis)
        else:
            return self._generate_general_response(user_input, intent_analysis)
    
    def _generate_recommendation_response(self, user_input: str, intent_analysis: Dict) -> str:
        """Generate detailed recommendation response"""
        
        use_case = intent_analysis["use_case"]
        detail_level = intent_analysis["detail_level"]
        
        if use_case == "gaming":
            return self._get_gaming_recommendations(detail_level)
        elif use_case == "defi":
            return self._get_defi_recommendations(detail_level)
        elif use_case == "enterprise":
            return self._get_enterprise_recommendations(detail_level)
        elif use_case == "payments":
            return self._get_payments_recommendations(detail_level)
        elif use_case == "nft":
            return self._get_nft_recommendations(detail_level)
        else:
            return self._get_general_recommendations(user_input, detail_level)
    
    def _get_live_l1_recommendations(self, use_case: str, detail_level: str) -> str:
        """Get real-time L1 protocol recommendations with live data"""
        
        try:
            # Get live data for all L1 protocols
            live_data = self.l1_data_service.get_all_l1_protocols_data()
            
            if not live_data:
                return "Unable to fetch real-time L1 data. Please try again later."
            
            # Filter for use case and generate response
            if use_case == "gaming":
                return self._generate_live_gaming_recommendations(live_data, detail_level)
            elif use_case == "defi":
                return self._generate_live_defi_recommendations(live_data, detail_level)
            else:
                return self._generate_live_general_recommendations(live_data, use_case, detail_level)
                
        except Exception as e:
            return f"Error fetching real-time L1 data: {str(e)}"
    
    def _generate_live_gaming_recommendations(self, live_data: Dict, detail_level: str) -> str:
        """Generate live gaming recommendations with real-time data"""
        
        # Rank L1s for gaming based on real-time metrics
        gaming_scores = {}
        for protocol_id, data in live_data.items():
            score = self._calculate_gaming_score(data)
            gaming_scores[protocol_id] = score
        
        # Sort by score
        top_l1s = sorted(gaming_scores.items(), key=lambda x: x[1], reverse=True)[:5]
        
        response = f"""🎮 **GAMING L1 PROTOCOLS - LIVE ANALYSIS** 
*Updated: {live_data[list(live_data.keys())[0]].get('last_updated', 'Recently')}*

**📊 REAL-TIME PERFORMANCE METRICS:**

"""
        
        rank_emojis = ["🏆", "🥈", "🥉", "4️⃣", "5️⃣"]
        
        for i, (protocol_id, score) in enumerate(top_l1s):
            if protocol_id not in live_data:
                continue
                
            data = live_data[protocol_id]
            emoji = rank_emojis[i] if i < len(rank_emojis) else f"{i+1}."
            
            response += f"""**{emoji} {data.get('name', protocol_id.title())}** (Gaming Score: {score:.1f}/100)
   💎 **Live Market Data**
      • Market Cap: ${data.get('market_cap', 0):,.0f}
      • 24h Change: {data.get('price_change_24h', 0):+.2f}%
      • Volume: ${data.get('volume_24h', 0):,.0f}
      • TVL: ${data.get('tvl', 0):,.0f}

   ⚡ **Performance Metrics**
      • TPS: {data.get('tps', 0):,}
      • Finality: {self._format_finality(data.get('finality_time', 0))}
      • Avg Fee: ${data.get('avg_fee', 0):.4f}
      • Security Score: {data.get('security_score', 0)}/100

   🎯 **Gaming Suitability**: {self._get_gaming_analysis(data)}

"""

        # Add market overview
        total_market_cap = sum(data.get('market_cap', 0) for data in live_data.values())
        total_tvl = sum(data.get('tvl', 0) for data in live_data.values())
        
        response += f"""
**🌍 LIVE L1 MARKET OVERVIEW:**
• Total L1 Market Cap: ${total_market_cap:,.0f}
• Total L1 TVL: ${total_tvl:,.0f}
• Active L1 Protocols Analyzed: {len(live_data)}

**💡 REAL-TIME INSIGHTS:**
• **Speed Leader**: {self._get_metric_leader(live_data, 'tps')} ({self._get_max_value(live_data, 'tps'):,} TPS)
• **Lowest Fees**: {self._get_metric_leader(live_data, 'avg_fee', lowest=True)} (${self._get_min_value(live_data, 'avg_fee'):.4f})
• **Market Leader**: {self._get_metric_leader(live_data, 'market_cap')} (${self._get_max_value(live_data, 'market_cap'):,.0f})

*Data refreshed every 5 minutes from CoinGecko, DeFiLlama, and network APIs*
"""
        
        return response

    def _generate_live_defi_recommendations(self, live_data: Dict, detail_level: str) -> str:
        """Generate live DeFi recommendations with real-time data"""
        
        # Calculate DeFi scores
        defi_scores = {}
        for protocol_id, data in live_data.items():
            score = self._calculate_defi_score(data)
            defi_scores[protocol_id] = score
        
        top_l1s = sorted(defi_scores.items(), key=lambda x: x[1], reverse=True)[:5]
        
        response = f"""🏦 **DEFI L1 PROTOCOLS - INSTITUTIONAL ANALYSIS**
*Live Data Updated: {live_data[list(live_data.keys())[0]].get('last_updated', 'Recently')}*

**💰 REAL-TIME DEFI METRICS:**

"""
        
        for i, (protocol_id, score) in enumerate(top_l1s):
            if protocol_id not in live_data:
                continue
                
            data = live_data[protocol_id]
            rank_emoji = ["🏆", "🥈", "🥉", "4️⃣", "5️⃣"][i] if i < 5 else f"{i+1}."
            
            response += f"""**{rank_emoji} {data.get('name', protocol_id.title())}** (DeFi Score: {score:.1f}/100)
   💎 **Live Market Position**
      • Market Cap: ${data.get('market_cap', 0):,.0f} (Rank #{data.get('market_cap_rank', 'N/A')})
      • TVL: ${data.get('tvl', 0):,.0f}
      • Protocol Count: {data.get('protocol_count', 0)}
      • 24h Volume: ${data.get('volume_24h', 0):,.0f}

   🏛️ **DeFi Infrastructure**
      • Ecosystem Score: {data.get('ecosystem_score', 0)}/100
      • Developer Activity: {data.get('development_activity', 0)}/100
      • Security Rating: {data.get('security_score', 0)}/100

   💸 **Cost Analysis**
      • Average Fee: ${data.get('avg_fee', 0):.4f}
      • Finality Time: {self._format_finality(data.get('finality_time', 0))}
      • Gas Efficiency: {self._get_gas_efficiency_rating(data)}

"""
        
        response += f"""
**📊 LIVE DEFI ECOSYSTEM STATS:**
• Total DeFi TVL: ${sum(data.get('tvl', 0) for data in live_data.values()):,.0f}
• Average Protocol Count: {sum(data.get('protocol_count', 0) for data in live_data.values()) / len(live_data):.1f}
• Market Dominance Leader: {self._get_metric_leader(live_data, 'tvl')}

**🎯 CURRENT MARKET CONDITIONS:**
• Best for Large Trades: {self._get_metric_leader(live_data, 'tvl')} (deepest liquidity)
• Most Cost Effective: {self._get_metric_leader(live_data, 'avg_fee', lowest=True)} 
• Fastest Settlement: {self._get_metric_leader(live_data, 'finality_time', lowest=True)}

*Real-time data from multiple blockchain APIs and DeFi protocols*
"""
        
        return response

    def _calculate_gaming_score(self, data: Dict) -> float:
        """Calculate gaming suitability score based on real-time data"""
        
        score = 0
        
        # TPS weight (40%) - gaming needs high throughput
        tps = data.get('tps', 0)
        if tps >= 10000:
            score += 40
        elif tps >= 1000:
            score += 30
        elif tps >= 100:
            score += 20
        else:
            score += 10
        
        # Fee weight (30%) - gaming needs low fees
        fee = data.get('avg_fee', 1)
        if fee <= 0.01:
            score += 30
        elif fee <= 0.1:
            score += 20
        elif fee <= 1:
            score += 10
        else:
            score += 5
        
        # Finality weight (20%) - gaming needs fast finality
        finality = data.get('finality_time', 60)
        if finality <= 2:
            score += 20
        elif finality <= 10:
            score += 15
        elif finality <= 60:
            score += 10
        else:
            score += 5
        
        # Ecosystem weight (10%)
        ecosystem_score = data.get('ecosystem_score', 50)
        score += (ecosystem_score / 100) * 10
        
        return min(100, score)

    def _calculate_defi_score(self, data: Dict) -> float:
        """Calculate DeFi suitability score based on real-time data"""
        
        score = 0
        
        # TVL weight (35%) - DeFi needs liquidity
        tvl = data.get('tvl', 0)
        if tvl >= 1000000000:  # $1B+
            score += 35
        elif tvl >= 100000000:  # $100M+
            score += 25
        elif tvl >= 10000000:   # $10M+
            score += 15
        else:
            score += 5
        
        # Security weight (30%)
        security = data.get('security_score', 50)
        score += (security / 100) * 30
        
        # Ecosystem weight (20%)
        ecosystem = data.get('ecosystem_score', 50)
        score += (ecosystem / 100) * 20
        
        # Fee efficiency (15%)
        fee = data.get('avg_fee', 1)
        if fee <= 0.1:
            score += 15
        elif fee <= 1:
            score += 10
        elif fee <= 10:
            score += 5
        else:
            score += 2
        
        return min(100, score)

    def _get_gaming_recommendations(self, detail_level: str) -> str:
        """Comprehensive gaming blockchain recommendations with live data"""
        
        return self._get_live_l1_recommendations("gaming", detail_level)

    def _get_defi_recommendations(self, detail_level: str) -> str:
        """Comprehensive DeFi blockchain recommendations with live data"""
        
        return self._get_live_l1_recommendations("defi", detail_level)

    def _format_finality(self, finality_seconds: float) -> str:
        """Format finality time for readability"""
        
        if finality_seconds < 1:
            return f"{finality_seconds*1000:.0f}ms"
        elif finality_seconds < 60:
            return f"{finality_seconds:.1f}s"
        else:
            minutes = int(finality_seconds // 60)
            seconds = int(finality_seconds % 60)
            if seconds > 0:
                return f"{minutes}m {seconds}s"
            return f"{minutes}m"

    def _get_gaming_analysis(self, data: Dict) -> str:
        """Get gaming suitability analysis"""
        
        tps = data.get('tps', 0)
        fee = data.get('avg_fee', 1)
        finality = data.get('finality_time', 60)
        
        if tps >= 10000 and fee <= 0.01 and finality <= 2:
            return "Excellent for high-frequency gaming"
        elif tps >= 1000 and fee <= 0.1:
            return "Good for most gaming applications"
        elif tps >= 100:
            return "Suitable for casual gaming"
        else:
            return "Limited gaming performance"

    def _get_gas_efficiency_rating(self, data: Dict) -> str:
        """Get gas efficiency rating"""
        
        fee = data.get('avg_fee', 1)
        if fee <= 0.01:
            return "Excellent"
        elif fee <= 0.1:
            return "Good"
        elif fee <= 1:
            return "Fair"
        else:
            return "Poor"

    def _get_metric_leader(self, live_data: Dict, metric: str, lowest: bool = False) -> str:
        """Get the protocol leader for a specific metric"""
        
        if not live_data:
            return "N/A"
        
        if lowest:
            leader = min(live_data.items(), key=lambda x: x[1].get(metric, float('inf')))
        else:
            leader = max(live_data.items(), key=lambda x: x[1].get(metric, 0))
        
        return leader[1].get('name', leader[0].title())

    def _get_max_value(self, live_data: Dict, metric: str) -> float:
        """Get maximum value for a metric"""
        
        return max(data.get(metric, 0) for data in live_data.values())

    def _get_min_value(self, live_data: Dict, metric: str) -> float:
        """Get minimum value for a metric"""
        
        return min(data.get(metric, float('inf')) for data in live_data.values())

    def _generate_live_general_recommendations(self, live_data: Dict, use_case: str, detail_level: str) -> str:
        """Generate general L1 recommendations with live data"""
        
        response = f"""**🔗 LIVE L1 PROTOCOL ANALYSIS**
*Real-time data for {len(live_data)} major Layer 1 protocols*

**📊 CURRENT MARKET SNAPSHOT:**
"""
        
        for protocol_id, data in list(live_data.items())[:5]:
            response += f"""
**{data.get('name', protocol_id.title())}**
• Market Cap: ${data.get('market_cap', 0):,.0f}
• TPS: {data.get('tps', 0):,} | Fee: ${data.get('avg_fee', 0):.4f}
• TVL: ${data.get('tvl', 0):,.0f} | Protocols: {data.get('protocol_count', 0)}
"""
        
        return response + "\n*Data updated every 5 minutes from live blockchain APIs*"
    
    def _extract_use_case(self, user_input_lower: str) -> Optional[str]:
        """Extract use case from user input with advanced pattern matching"""

**1. Solana** ⭐⭐⭐⭐⭐ (Score: 96/100)
   🔥 **Performance Excellence**
   • Throughput: 65,000 TPS (world-class)
   • Finality: 400ms (lightning fast)
   • Cost: $0.00025 per transaction
   • Block Time: 400ms consistent

   🎯 **Gaming Advantages**
   • Metaplex Protocol for NFT gaming
   • Anchor framework for game development
   • Star Atlas ($100M+ gaming ecosystem)
   • Native composability for game features

   💪 **Why #1 for Gaming**: Unmatched speed-to-cost ratio

**2. Polygon** ⭐⭐⭐⭐⭐ (Score: 94/100)
   🔥 **Ethereum Compatibility Champion**
   • Throughput: 7,000 TPS 
   • Finality: 2 seconds
   • Cost: $0.01 per transaction
   • EVM Compatible: Seamless Ethereum migration

   🎯 **Gaming Ecosystem**
   • The Sandbox, Decentraland partnerships
   • Immutable partnership for NFT gaming
   • 500+ gaming dApps live
   • Unity/Unreal Engine support

   💪 **Why Choose**: Largest gaming ecosystem + Ethereum access

**3. Immutable X** ⭐⭐⭐⭐ (Score: 92/100)
   🔥 **Gaming-First Design**
   • Throughput: 9,000 TPS
   • Finality: Instant for NFT trades
   • Cost: $0 gas fees for NFTs
   • Built specifically for gaming

   🎯 **Gaming Focus**
   • Gods Unchained (leading TCG)
   • Guild of Guardians ecosystem
   • Carbon-neutral NFT minting
   • Order book trading for game assets

   💪 **Why Choose**: Purpose-built for NFT gaming

**4. WAX** ⭐⭐⭐⭐ (Score: 90/100)
   🔥 **Free-to-Play Leader**
   • Throughput: 8,000 TPS
   • Finality: 500ms
   • Cost: Free with CPU staking
   • 200+ active games

   🎯 **Gaming Heritage**
   • Alien Worlds (1M+ players)
   • Splinterlands integration
   • Cloud Wallet for mass adoption
   • vIRL NFT marketplace

   💪 **Why Choose**: Proven P2E gaming ecosystem

**📊 DETAILED PERFORMANCE COMPARISON:**

| Metric | Solana | Polygon | Immutable X | WAX |
|--------|--------|---------|-------------|-----|
| Max TPS | 65,000 | 7,000 | 9,000 | 8,000 |
| Avg Latency | 400ms | 2,000ms | 100ms* | 500ms |
| Gaming dApps | 50+ | 100+ | 20+ | 200+ |
| Daily Users | 50K+ | 200K+ | 30K+ | 300K+ |
| NFT Volume | High | Very High | Medium | High |

**🎯 SELECTION FRAMEWORK:**

**Choose Solana if:**
• Building competitive esports games
• Need maximum throughput (>10K TPS)
• Speed is more important than ecosystem size
• Comfortable with newer technology

**Choose Polygon if:**
• Want Ethereum ecosystem access
• Large existing community matters
• Need extensive DeFi integrations
• Prefer battle-tested infrastructure

**Choose Immutable X if:**
• Focus is primarily NFT trading games
• Zero-gas-fee model is essential
• Environmental concerns are priority
• Trading card games or collectibles

**Choose WAX if:**
• Building free-to-play social games  
• Target mass-market adoption
• P2E mechanics are central
• Want proven gaming user base

**🛠️ IMPLEMENTATION ROADMAP:**

**Phase 1: Foundation (Weeks 1-2)**
• Smart contract architecture design
• Wallet integration (Phantom/MetaMask)
• Basic NFT minting functionality

**Phase 2: Core Features (Weeks 3-6)**
• Game logic implementation
• Asset marketplace integration
• Player progression systems

**Phase 3: Advanced Features (Weeks 7-12)**
• Cross-chain asset bridges
• Advanced trading mechanisms
• Analytics and reporting

**⚠️ TECHNICAL CONSIDERATIONS:**
• **Frontend**: React/Unity Web3 integration required
• **Backend**: Node.js/Rust recommended for blockchain interaction
• **Database**: Hybrid on-chain/off-chain data architecture
• **Scaling**: Consider L2 solutions for high-volume games

**🚀 EMERGING OPPORTUNITIES:**
• **Subnet Gaming**: Avalanche subnets for custom gaming chains
• **App-Specific Rollups**: StarkEx/Arbitrum for dedicated gaming L2s
• **Cross-Chain Gaming**: Multi-blockchain asset interoperability
• **AI Integration**: Blockchain-verified AI gaming experiences

Want specific implementation guidance for any platform, or details about smart contract architecture?"""

    def _get_defi_recommendations(self, detail_level: str) -> str:
        """Comprehensive DeFi blockchain analysis"""
        
        return """🏦 **DEFI ECOSYSTEM ANALYSIS - INSTITUTIONAL GRADE**

Comprehensive analysis of $200B+ DeFi market across 50+ blockchains:

**💰 DEFI SUCCESS FACTORS:**
• **Security**: Battle-tested protocols with extensive audits
• **Liquidity Depth**: High TVL for minimal slippage
• **Composability**: Seamless protocol integration ("DeFi Legos")
• **Cost Efficiency**: Sustainable fees for all user segments  
• **Governance Maturity**: Decentralized decision-making processes
• **Institutional Support**: Enterprise-grade custody and compliance

**🏆 TIER 1 DEFI DOMINATORS:**

**1. Ethereum** ⭐⭐⭐⭐⭐ (DeFi Score: 98/100)
   💎 **Market Leadership**
   • Total TVL: $28.5B (55% market share)
   • Active Protocols: 400+ live applications
   • Daily Volume: $1.2B+ across all DEXs
   • Institutional TVL: $8B+ from major funds

   🔒 **Security Excellence**
   • 8+ years of battle-testing
   • $50M+ in bug bounties paid
   • Formal verification for major protocols
   • Insurance coverage: $1B+ protected

   🏛️ **Ecosystem Depth**
   • **DEXs**: Uniswap V3 ($4B TVL), Curve ($3.2B)
   • **Lending**: Aave ($5.1B), Compound ($2.8B)
   • **Derivatives**: dYdX, Synthetix, GMX
   • **Yield**: Yearn Finance, Convex Finance

   ⚡ **Recent Improvements**
   • Merge: 99.9% energy reduction
   • Layer 2 Integration: Arbitrum/Optimism scaling
   • MEV Protection: Flashbots integration
   • EIP-4844: Blob transactions for L2 scaling

**2. BNB Smart Chain** ⭐⭐⭐⭐ (DeFi Score: 87/100)
   💎 **Performance Leader**
   • Total TVL: $5.8B (strong retention)
   • Transaction Speed: 2,100 TPS average
   • Average Fees: $0.35-0.75
   • Block Finality: 3 seconds

   🏛️ **DeFi Ecosystem**
   • **PancakeSwap**: $1.2B TVL, 2M+ users
   • **Venus Protocol**: $850M lending market
   • **Alpaca Finance**: Leading leveraged yield farming
   • **Ellipsis**: Curve fork with strong adoption

   💼 **Institutional Features**
   • Binance ecosystem integration
   • Regulatory-compliant in 180+ countries
   • Advanced trading features
   • Centralized-DeFi bridge services

**3. Avalanche** ⭐⭐⭐⭐ (DeFi Score: 85/100)
   💎 **Institutional Focus**
   • Total TVL: $1.1B (quality protocols)
   • Subnet Architecture: Custom blockchain deployment
   • Finality: <2 seconds (fastest among majors)
   • Enterprise Partnerships: Deloitte, Mastercard

   🏛️ **Premium DeFi**
   • **Trader Joe**: Advanced AMM with concentrated liquidity
   • **Aave Avalanche**: $400M+ lending market
   • **Platypus**: Stablecoin-optimized DEX
   • **Benqi**: Native liquid staking protocol

   🏢 **Enterprise Adoption**
   • JP Morgan Onyx integration pilot
   • Mastercard payment rail exploration  
   • Deloitte blockchain consulting partnership
   • Custom subnet deployment for enterprises

**4. Polygon** ⭐⭐⭐⭐⭐ (DeFi Score: 89/100)
   💎 **Scaling Champion**
   • Total TVL: $1.6B (rapid growth)
   • Transaction Cost: $0.01-0.05
   • Ethereum Compatibility: 100% EVM
   • Daily Transactions: 3M+ consistently

   🏛️ **Ethereum DeFi Bridge**
   • **QuickSwap**: Leading Polygon DEX
   • **SushiSwap**: Multi-chain presence
   • **Aave Polygon**: Low-cost lending
   • **Curve**: Major stablecoin trading

**📊 COMPREHENSIVE DEFI METRICS:**

| Protocol | TVL | Daily Vol | Protocols | Yield Avg | Risk Score |
|----------|-----|-----------|-----------|-----------|------------|
| Ethereum | $28.5B | $1.2B | 400+ | 4-12% | AAA |
| BSC | $5.8B | $280M | 150+ | 8-25% | AA |
| Avalanche | $1.1B | $120M | 60+ | 6-18% | AA+ |
| Polygon | $1.6B | $180M | 100+ | 5-20% | AA |

**🎯 USE CASE OPTIMIZATION:**

**💱 DEX Trading Strategy**
• **Whale Trades** (>$100K): Ethereum (deepest liquidity)
• **Active Trading** ($1K-100K): Polygon (lowest fees)
• **Yield Farming**: BSC (highest APYs available)
• **Arbitrage**: Avalanche (fastest finality)

**🏦 Lending & Borrowing**
• **Maximum Security**: Ethereum (Aave/Compound)
• **High Leverage**: BSC (Venus Protocol)
• **Stablecoin Focus**: Avalanche (Platypus)
• **Cross-Chain**: Polygon (multichain protocols)

**🌾 Advanced Yield Strategies**
• **Blue-Chip Farming**: Ethereum (Curve/Yearn)
• **High-Risk/High-Reward**: BSC (new protocols)
• **Institutional Yield**: Avalanche (regulated options)
• **Gas-Efficient**: Polygon (frequent compounding)

**⚖️ RISK-ADJUSTED SELECTION:**

**Conservative Portfolio (Institutions):**
• 70% Ethereum (maximum security)
• 20% Avalanche (institutional focus)
• 10% Polygon (cost efficiency)

**Balanced Portfolio (Experienced Users):**
• 50% Ethereum (core DeFi)
• 25% Polygon (scaling benefits)  
• 20% BSC (yield opportunities)
• 5% Avalanche (diversification)

**Aggressive Portfolio (DeFi Natives):**
• 40% Ethereum (foundation)
• 30% BSC (yield farming)
• 20% Emerging L1s (growth potential)
• 10% Avalanche (institutional upside)

**🚨 CURRENT MARKET ANALYSIS:**

**Bullish Indicators:**
• Institutional adoption accelerating
• Layer 2 solutions reducing Ethereum costs
• Regulatory clarity improving globally
• Real-world asset tokenization growing

**Risk Factors:**
• Regulatory uncertainty in key markets
• Smart contract vulnerabilities persist
• Liquidity concentration in few protocols
• Market correlation remains high

**🔮 EMERGING TRENDS (2024-2025):**
• **Real-World Assets**: Tokenized bonds, real estate
• **Institutional DeFi**: Compliance-first protocols
• **Cross-Chain Native**: Multi-blockchain protocols
• **AI-Enhanced DeFi**: Automated strategy optimization

Want specific protocol analysis, yield strategy recommendations, or institutional compliance guidance?"""
    
    def _extract_use_case(self, user_input_lower: str) -> Optional[str]:
        """Extract use case from user input with advanced pattern matching"""
        
        use_case_patterns = {
            "gaming": [
                "gaming", "game", "games", "nft", "collectible", "play-to-earn", "p2e",
                "metaverse", "virtual world", "in-game", "avatar", "esports"
            ],
            "defi": [
                "defi", "decentralized finance", "finance", "trading", "swap", "dex", 
                "lending", "borrowing", "yield", "farming", "liquidity", "staking",
                "amm", "protocol", "vault"
            ],
            "enterprise": [
                "enterprise", "business", "corporate", "company", "organization",
                "supply chain", "logistics", "compliance", "governance", "institutional"
            ],
            "payments": [
                "payment", "payments", "transfer", "send", "money", "remittance",
                "micropayment", "transaction", "settlement", "cross-border"
            ],
            "nft": [
                "nft", "non-fungible", "art", "marketplace", "creator", "royalty",
                "collectible", "digital asset", "mint", "auction"
            ]
        }
        
        for use_case, patterns in use_case_patterns.items():
            if any(pattern in user_input_lower for pattern in patterns):
                return use_case
        
        return None
    
    def _extract_technical_requirements(self, user_input_lower: str) -> Dict:
        """Extract technical requirements with advanced parsing"""
        
        params = {}
        
        # TPS extraction with multiple patterns
        tps_patterns = [
            r"(\d+[,\d]*)\s*tps",
            r"(\d+[,\d]*)\s*transactions?\s*per\s*second",
            r"(\d+[,\d]*)\s*tx/s"
        ]
        
        for pattern in tps_patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                tps_value = match.group(1).replace(",", "")
                if tps_value.isdigit():
                    params["min_tps"] = int(tps_value)
                    break
        
        # High performance keywords
        if any(word in user_input_lower for word in ["high throughput", "fast", "scalable", "performance"]):
            params["min_tps"] = max(params.get("min_tps", 0), 10000)
        
        # Latency requirements
        latency_patterns = [
            r"(\d+(?:\.\d+)?)\s*(?:ms|milliseconds?)",
            r"(\d+(?:\.\d+)?)\s*(?:s|seconds?)\s*finality"
        ]
        
        for pattern in latency_patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                params["max_finality_time"] = float(match.group(1))
                break
        
        return params
    
    def _extract_economic_requirements(self, user_input_lower: str) -> Dict:
        """Extract economic requirements with advanced parsing"""
        
        params = {}
        
        # Fee extraction patterns
        fee_patterns = [
            r"\$(\d+(?:\.\d+)?)\s*(?:fee|cost)",
            r"(\d+(?:\.\d+)?)\s*cents?",
            r"(\d+(?:\.\d+)?)\s*dollars?\s*(?:fee|cost)"
        ]
        
        for pattern in fee_patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                fee_value = float(match.group(1))
                if "cent" in pattern:
                    params["max_fee"] = fee_value / 100
                else:
                    params["max_fee"] = fee_value
                break
        
        # Low cost keywords
        if any(word in user_input_lower for word in ["cheap", "low cost", "affordable", "low fee"]):
            params["max_fee"] = 0.01
        
        return params
    
    def _extract_blockchain_mentions(self, user_input_lower: str) -> List[str]:
        """Extract mentioned blockchain names"""
        
        blockchain_aliases = {
            "ethereum": ["ethereum", "eth", "ether"],
            "solana": ["solana", "sol"],
            "polygon": ["polygon", "matic"],
            "binance": ["binance", "bnb", "bsc", "binance smart chain"],
            "avalanche": ["avalanche", "avax"],
            "cardano": ["cardano", "ada"],
            "polkadot": ["polkadot", "dot"],
            "cosmos": ["cosmos", "atom"],
            "near": ["near", "near protocol"],
            "fantom": ["fantom", "ftm"],
            "algorand": ["algorand", "algo"],
            "tezos": ["tezos", "xtz"]
        }
        
        mentioned = []
        for blockchain, aliases in blockchain_aliases.items():
            if any(alias in user_input_lower for alias in aliases):
                mentioned.append(blockchain)
        
        return mentioned
    
    def _initialize_knowledge_base(self) -> Dict:
        """Initialize comprehensive blockchain knowledge base"""
        
        return {
            "market_trends": {
                "2024_outlook": "DeFi growth, Gaming adoption, Enterprise integration",
                "emerging_l1s": ["Sui", "Aptos", "Sei"],
                "l2_adoption": "Arbitrum and Optimism leading Ethereum scaling"
            },
            "technical_benchmarks": {
                "high_tps": 10000,
                "low_latency": 2.0,
                "low_fees": 0.01
            },
            "institutional_preferences": {
                "security_focused": ["ethereum", "avalanche"],
                "compliance_ready": ["ethereum", "polygon", "avalanche"],
                "enterprise_partnerships": ["polygon", "avalanche", "binance"]
            }
        }
    
    def _initialize_response_templates(self) -> Dict:
        """Initialize response templates for consistent formatting"""
        
        return {
            "analysis_header": "**🔍 BLOCKCHAIN ANALYSIS - {}**\n\n",
            "recommendation_format": "**{rank}. {name}** ⭐⭐⭐⭐⭐ (Score: {score}/100)",
            "section_separator": "\n" + "─" * 60 + "\n\n"
        }
    
    def _generate_comparison_response(self, user_input: str, intent_analysis: Dict) -> str:
        """Generate detailed comparison response"""
        return "Detailed comparison response would be generated here based on the specific blockchains mentioned."
    
    def _generate_implementation_response(self, user_input: str, intent_analysis: Dict) -> str:
        """Generate implementation guidance response"""
        return "Implementation guidance would be provided here with step-by-step instructions."
    
    def _generate_explanation_response(self, user_input: str, intent_analysis: Dict) -> str:
        """Generate educational explanation response"""
        return "Educational explanation would be provided here with comprehensive details."
    
    def _generate_general_response(self, user_input: str, intent_analysis: Dict) -> str:
        """Generate general purpose response"""
        return """I'm your specialized blockchain research assistant! I can help you with:

🔍 **Protocol Recommendations** - Find the perfect blockchain for your needs
📊 **Detailed Comparisons** - Side-by-side analysis with comprehensive metrics  
💡 **Use Case Guidance** - Gaming, DeFi, Enterprise, NFTs, and more
📈 **Technical Analysis** - Performance, security, and ecosystem evaluation
🛠️ **Implementation Support** - Development guidance and best practices

Try asking me something like:
• "Find the best blockchain for gaming with high TPS"
• "Compare Ethereum vs Solana for DeFi applications"
• "What are enterprise-grade blockchain solutions?"

What specific blockchain challenge can I help you solve?"""

    def _get_enterprise_recommendations(self, detail_level: str) -> str:
        """Enterprise blockchain recommendations"""
        return "Enterprise recommendations would be provided here."
    
    def _get_payments_recommendations(self, detail_level: str) -> str:
        """Payments blockchain recommendations"""
        return "Payments recommendations would be provided here."
    
    def _get_nft_recommendations(self, detail_level: str) -> str:
        """NFT blockchain recommendations"""
        return "NFT recommendations would be provided here."
    
    def _get_general_recommendations(self, user_input: str, detail_level: str) -> str:
        """General blockchain recommendations"""
        return "General recommendations would be provided here."