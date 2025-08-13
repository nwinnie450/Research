"""
L1 Protocol Market Analyzer
Generates accurate market analysis with real-time data and proper TPS rankings
"""
from typing import Dict, List, Optional, Any
from datetime import datetime
from services.live_l1_data_service import LiveL1DataService

class L1ProtocolMarketAnalyzer:
    """
    Analyzer for L1 blockchain market with accurate TPS rankings and real-time data
    """
    
    def __init__(self):
        self.data_service = LiveL1DataService()
    
    def get_tps_ranking_analysis(self) -> str:
        """Generate TPS-focused market analysis with accurate rankings"""
        
        # Get live L1 data
        market_data = self.data_service.get_live_l1_market_analysis()
        
        if not market_data.get('protocols'):
            return self._generate_error_response()
        
        protocols = market_data['protocols']
        rankings = market_data['rankings']
        overview = market_data['market_overview']
        
        response = "# 🚀 **LIVE L1 PROTOCOL TPS RANKINGS**\n\n"
        response += f"*Real-time data from verified sources • Updated: {datetime.now().strftime('%b %d, %Y %H:%M UTC')}*\n\n"
        
        # TPS Rankings Section
        response += "## 📊 **Layer 1 TPS Rankings** (Live Measurements)\n\n"
        
        if rankings.get('by_tps'):
            for i, (protocol_id, data) in enumerate(rankings['by_tps'][:10], 1):
                name = data.get('name', protocol_id.title())
                current_tps = data.get('current_tps', 0)
                avg_tps = data.get('avg_tps_24h', current_tps)
                data_source = data.get('data_source', 'live')
                
                # Medal for top 3
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"#{i}"
                
                response += f"{medal} **{name}**: {current_tps:,.1f} TPS\n"
                
                # Show 24h range if different from current
                if abs(avg_tps - current_tps) > 1:
                    response += f"   • 24h Average: {avg_tps:,.1f} TPS\n"
                
                # Add context for notable rankings
                if i == 1:
                    response += f"   • **Highest Live TPS** among major L1 blockchains\n"
                elif current_tps < 50 and data.get('market_cap', 0) > 10000000000:  # < 50 TPS but > $10B mcap
                    response += f"   • **Note**: High market cap despite limited throughput\n"
                elif current_tps > 1000:
                    response += f"   • **High Performance**: Capable of handling enterprise-scale loads\n"
                
                # Show data source confidence
                if data_source == 'chainspect_live':
                    response += f"   • **Source**: Live measurement from Chainspect\n"
                elif data_source == 'verified_fallback':
                    response += f"   • **Source**: Verified real-world performance data\n"
                
                response += "\n"
        
        # Market Overview
        response += "## 🌐 **L1 Market Overview**\n\n"
        
        if overview:
            total_mcap = overview.get('total_market_cap', 0)
            total_tvl = overview.get('total_tvl', 0)
            highest_tps_name = overview.get('highest_tps_protocol', 'Unknown')
            highest_tps_value = overview.get('highest_tps_value', 0)
            
            response += f"• **Total L1 Market Cap**: ${total_mcap:,.0f}\n"
            if total_tvl > 0:
                response += f"• **Total L1 TVL**: ${total_tvl:,.0f}\n"
            response += f"• **Performance Leader**: {highest_tps_name} ({highest_tps_value:,.1f} TPS)\n"
            response += f"• **Protocols Analyzed**: {overview.get('total_protocols', 0)} Layer 1 blockchains\n\n"
        
        # Performance Analysis
        response += "## ⚡ **Performance Categories**\n\n"
        
        perf_metrics = market_data.get('performance_metrics', {})
        if perf_metrics:
            high_perf = perf_metrics.get('performance_distribution', {}).get('high', [])
            medium_perf = perf_metrics.get('performance_distribution', {}).get('medium', [])
            low_perf = perf_metrics.get('performance_distribution', {}).get('low', [])
            
            if high_perf:
                response += f"**High Performance (>100 TPS)**: {', '.join(high_perf)}\n"
            if medium_perf:
                response += f"**Medium Performance (10-100 TPS)**: {', '.join(medium_perf)}\n"
            if low_perf:
                response += f"**Specialized/Low TPS (<10 TPS)**: {', '.join(low_perf)}\n"
        
        response += "\n"
        
        # Key Insights
        response += "## 🔍 **Key Insights**\n\n"
        
        if rankings.get('by_tps') and len(rankings['by_tps']) >= 2:
            leader = rankings['by_tps'][0][1]
            second = rankings['by_tps'][1][1]
            
            leader_tps = leader.get('current_tps', 0)
            second_tps = second.get('current_tps', 0)
            
            if leader_tps > 0 and second_tps > 0:
                multiplier = leader_tps / second_tps
                response += f"• **TPS Leader**: {leader.get('name')} processes {multiplier:.1f}x more transactions than {second.get('name')}\n"
            
            # Find biggest market cap vs TPS discrepancy
            mcap_leader = max(protocols.values(), key=lambda x: x.get('market_cap', 0), default={})
            if mcap_leader.get('name') != leader.get('name'):
                response += f"• **Market vs Performance**: {mcap_leader.get('name')} has largest market cap but {leader.get('name')} has highest TPS\n"
        
        # Data Quality Notice
        response += f"\n---\n"
        response += f"**Data Sources**: Chainspect API, CoinGecko, DeFiLlama\n"
        response += f"**Update Frequency**: Real-time (1-minute cache)\n"
        response += f"**Methodology**: Live network measurements, not theoretical maximums\n"
        
        return response
    
    def get_comprehensive_l1_analysis(self) -> str:
        """Generate comprehensive L1 market analysis"""
        
        market_data = self.data_service.get_live_l1_market_analysis()
        
        if not market_data.get('protocols'):
            return self._generate_error_response()
        
        protocols = market_data['protocols']
        rankings = market_data['rankings']
        
        response = "# 🌐 **COMPREHENSIVE L1 PROTOCOL ANALYSIS**\n\n"
        response += f"*Live market data • {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}*\n\n"
        
        # Multi-metric rankings
        response += "## 📊 **Multi-Metric Rankings**\n\n"
        
        # Top 5 by TPS
        if rankings.get('by_tps'):
            response += "### ⚡ **By Transaction Throughput (TPS)**\n"
            for i, (pid, data) in enumerate(rankings['by_tps'][:5], 1):
                tps = data.get('current_tps', 0)
                response += f"{i}. {data.get('name', pid)}: {tps:,.1f} TPS\n"
            response += "\n"
        
        # Top 5 by Market Cap
        if rankings.get('by_market_cap'):
            response += "### 💰 **By Market Capitalization**\n"
            for i, (pid, data) in enumerate(rankings['by_market_cap'][:5], 1):
                mcap = data.get('market_cap', 0)
                if mcap > 0:
                    response += f"{i}. {data.get('name', pid)}: ${mcap:,.0f}\n"
            response += "\n"
        
        # Top 5 by TVL (DeFi-enabled chains only)
        if rankings.get('by_tvl') and rankings['by_tvl']:
            response += "### 🏦 **By Total Value Locked (DeFi)**\n"
            for i, (pid, data) in enumerate(rankings['by_tvl'][:5], 1):
                tvl = data.get('tvl', 0)
                response += f"{i}. {data.get('name', pid)}: ${tvl:,.0f}\n"
            response += "\n"
        
        # Protocol details table
        response += "## 📋 **Protocol Comparison Table**\n\n"
        response += "| Protocol | TPS | Market Cap | TVL | Consensus |\n"
        response += "|----------|-----|------------|-----|-----------||\n"
        
        # Show top protocols by TPS
        if rankings.get('by_tps'):
            for pid, data in rankings['by_tps'][:8]:
                name = data.get('name', pid)[:12]  # Truncate long names
                tps = f"{data.get('current_tps', 0):,.0f}"
                mcap = f"${data.get('market_cap', 0)/1e9:.1f}B" if data.get('market_cap', 0) > 0 else "N/A"
                tvl = f"${data.get('tvl', 0)/1e9:.1f}B" if data.get('tvl', 0) > 0 else "N/A"
                consensus = data.get('consensus', 'Unknown')[:15]  # Truncate
                
                response += f"| {name} | {tps} | {mcap} | {tvl} | {consensus} |\n"
        
        response += "\n"
        
        return response
    
    def get_protocol_details(self, protocol_name: str) -> str:
        """Get detailed analysis for a specific L1 protocol"""
        
        market_data = self.data_service.get_live_l1_market_analysis()
        protocols = market_data.get('protocols', {})
        
        # Find protocol by name
        target_protocol = None
        target_id = None
        
        for pid, data in protocols.items():
            if protocol_name.lower() in data.get('name', '').lower():
                target_protocol = data
                target_id = pid
                break
        
        if not target_protocol:
            return f"❌ Protocol '{protocol_name}' not found. Available L1 protocols: {', '.join([d.get('name', '') for d in protocols.values()])}"
        
        name = target_protocol.get('name', protocol_name)
        
        response = f"# 🔍 **{name} (L1) - Detailed Analysis**\n\n"
        response += f"*Live data updated: {target_protocol.get('last_updated', 'Unknown')}*\n\n"
        
        # Performance metrics
        response += "## ⚡ **Performance Metrics**\n\n"
        
        current_tps = target_protocol.get('current_tps', 0)
        avg_tps = target_protocol.get('avg_tps_24h', 0)
        max_tps = target_protocol.get('max_tps_24h', 0)
        
        response += f"• **Current TPS**: {current_tps:,.1f}\n"
        if avg_tps > 0 and avg_tps != current_tps:
            response += f"• **24h Average TPS**: {avg_tps:,.1f}\n"
        if max_tps > 0 and max_tps != current_tps:
            response += f"• **24h Peak TPS**: {max_tps:,.1f}\n"
        
        utilization = target_protocol.get('tps_utilization', 0)
        if utilization > 0:
            response += f"• **Network Utilization**: {utilization:.1f}%\n"
        
        # Market data
        response += "\n## 💰 **Market Data**\n\n"
        
        market_cap = target_protocol.get('market_cap', 0)
        if market_cap > 0:
            response += f"• **Market Cap**: ${market_cap:,.0f}\n"
            response += f"• **Market Cap Rank**: #{target_protocol.get('market_cap_rank', 'Unknown')}\n"
        
        price = target_protocol.get('current_price', 0)
        if price > 0:
            response += f"• **Current Price**: ${price:,.2f}\n"
            
            change_24h = target_protocol.get('price_change_24h', 0)
            if change_24h != 0:
                direction = "↗️" if change_24h > 0 else "↘️"
                response += f"• **24h Change**: {direction} {change_24h:+.2f}%\n"
        
        # Network stats
        response += "\n## 🌐 **Network Statistics**\n\n"
        
        daily_tx = target_protocol.get('daily_transactions', 0)
        if daily_tx > 0:
            response += f"• **Daily Transactions**: {daily_tx:,}\n"
        
        active_addresses = target_protocol.get('active_addresses', 0)
        if active_addresses > 0:
            response += f"• **Active Addresses**: {active_addresses:,}\n"
        
        avg_fee = target_protocol.get('avg_fee_usd', 0)
        if avg_fee > 0:
            response += f"• **Average Fee**: ${avg_fee:.4f}\n"
        
        # Technical details
        response += "\n## 🔧 **Technical Details**\n\n"
        response += f"• **Consensus Mechanism**: {target_protocol.get('consensus', 'Unknown')}\n"
        response += f"• **Symbol**: {target_protocol.get('symbol', 'N/A')}\n"
        response += f"• **Launch Year**: {target_protocol.get('launch_year', 'Unknown')}\n"
        
        # DeFi data if available
        tvl = target_protocol.get('tvl', 0)
        if tvl > 0:
            response += f"• **Total Value Locked (DeFi)**: ${tvl:,.0f}\n"
        
        return response
    
    def _generate_error_response(self) -> str:
        """Generate error response when data is unavailable"""
        
        return """# ⚠️ **L1 Market Data Temporarily Unavailable**

Unable to fetch live L1 protocol data at this time. This could be due to:

• API rate limits or temporary outages
• Network connectivity issues
• Data source maintenance

**Please try again in a few minutes.**

In the meantime, you can:
• Ask about blockchain research methodology
• Request latest improvement proposals (EIPs, BIPs, SUPs)
• Get guidance on blockchain parameter analysis
"""