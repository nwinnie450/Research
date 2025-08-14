"""
Blockchain Research & Advisory AI Agent
Streamlit Application Main Entry Point
"""
import streamlit as st
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config import PAGE_CONFIG, APP_TITLE, APP_DESCRIPTION, VERSION, COLORS
from utils.session_manager import init_session_state
from components.sidebar import render_sidebar
from components.header import render_header
from components.chat_interface import render_chat_interface
from components.dashboard import render_dashboard
from components.comparison import render_comparison
from components.analytics import render_analytics
from components.proposals import render_proposals_interface
from styles.custom_css import load_custom_css

def main():
    """Main application entry point"""
    
    # Configure Streamlit page
    st.set_page_config(**PAGE_CONFIG)
    
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    init_session_state()
    
    # Render header
    render_header()
    
    # Main layout - eliminate all gaps between sidebar and content
    with st.container():
        col1, col2 = st.columns([1, 5], gap="small")
        
        with col1:
            # Render sidebar navigation
            selected_page = render_sidebar()
        
        with col2:
            # Route to appropriate page based on selection
            if selected_page == "🏠 Home":
                render_home_page()
            elif selected_page == "💬 Chat":
                render_chat_interface()
            elif selected_page == "📊 Compare":
                render_comparison()
            elif selected_page == "📈 Analytics": 
                render_analytics()
            elif selected_page == "📋 Proposals":
                render_proposals_interface()
            elif selected_page == "🔍 Advanced":
                render_advanced_search()
            else:
                render_home_page()

def render_home_page():
    """Render the main home/dashboard page"""
    
    # Hero section - compact
    st.markdown("""
    <div class="hero-section">
        <h1 style="text-align: center; color: #1E3A8A; margin-bottom: 0.25rem;">
            Top 5 L1 Blockchain Protocol Analysis
        </h1>
        <p style="text-align: center; color: #6B7280; font-size: 1rem; margin-bottom: 1rem;">
            <strong>Ethereum • Base • Tron • BSC • Bitcoin</strong><br>
            AI-powered research with live data & improvement proposals
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick action cards focused on Improvement Proposals and L1 protocols - compact
    st.markdown("### 🚀 Quick Start - Improvement Proposals & L1 Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Browse TIPs", use_container_width=True):
            st.session_state.current_page = "📋 Proposals"
            st.rerun()
    
    with col2:
        if st.button("🔗 Latest EIPs", use_container_width=True):
            st.session_state.selected_use_case = "eips"
            st.session_state.current_page = "💬 Chat"
            st.rerun()
    
    with col3:
        if st.button("⚡ L1 Performance", use_container_width=True):
            st.session_state.selected_use_case = "l1_performance"
            st.session_state.current_page = "💬 Chat"
            st.rerun()
    
    # Main dashboard content
    render_dashboard()

def render_advanced_search():
    """Render advanced search interface with detailed filters"""
    st.markdown("---")
    st.markdown("### 🔍 Advanced Blockchain Search")
    
    # Advanced filtering interface
    with st.expander("⚙️ Advanced Filters", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Technical Requirements")
            min_tps = st.number_input("Minimum TPS", min_value=1, max_value=100000, value=1000)
            max_latency = st.number_input("Maximum Latency (seconds)", min_value=0.1, max_value=60.0, value=5.0)
            consensus_type = st.multiselect(
                "Consensus Mechanisms",
                ["Proof of Work", "Proof of Stake", "Delegated PoS", "Optimistic Rollup"],
                default=["Proof of Stake"]
            )
        
        with col2:
            st.markdown("#### Economic Parameters")
            max_fee = st.number_input("Maximum Transaction Fee ($)", min_value=0.0001, max_value=100.0, value=1.0)
            min_market_cap = st.number_input("Minimum Market Cap (Millions)", min_value=1, max_value=100000, value=100)
            staking_available = st.checkbox("Staking Available", value=False)
    
    # Search button
    if st.button("🔍 Search Protocols", type="primary", use_container_width=True):
        with st.spinner("Searching blockchain protocols..."):
            # Get real protocol data from the live service
            from services.live_l1_data_service import LiveL1DataService
            live_data_service = LiveL1DataService()
            market_analysis = live_data_service.get_live_l1_market_analysis()
            protocols_dict = market_analysis.get('protocols', {})
            
            # Convert to searchable format
            all_protocols = []
            for protocol_id, data in protocols_dict.items():
                protocol = {
                    'id': protocol_id,
                    'name': data.get('name', protocol_id.title()),
                    'symbol': data.get('symbol', ''),
                    'tps': data.get('current_tps', 0),
                    'avg_fee': data.get('avg_fee_usd', 0),
                    'consensus': data.get('consensus', 'Proof of Stake'),
                    'market_cap': data.get('market_cap', 0),
                    'type': 'Layer 1',
                    'staking': True if data.get('consensus') in ['Proof of Stake', 'Delegated PoS'] else False
                }
                all_protocols.append(protocol)
            
            # Apply filters
            filtered_protocols = []
            for protocol in all_protocols:
                # TPS filter
                if protocol['tps'] < min_tps:
                    continue
                
                # Fee filter
                if protocol['avg_fee'] > max_fee:
                    continue
                
                # Market cap filter
                if protocol['market_cap'] / 1e6 < min_market_cap:
                    continue
                
                # Consensus filter
                if consensus_type and protocol['consensus'] not in consensus_type:
                    continue
                
                # Staking filter
                if staking_available and not protocol['staking']:
                    continue
                
                filtered_protocols.append(protocol)
            
            # Sort by relevance score
            def calculate_relevance_score(protocol):
                # Higher TPS, lower fees, higher market cap = better score
                tps_score = min(protocol['tps'] / 1000, 100)  # Cap at 100
                fee_score = max(0, 100 - (protocol['avg_fee'] * 10))  # Lower fees = higher score
                mcap_score = min(protocol['market_cap'] / 1e9 * 10, 100)  # Market cap factor
                return (tps_score + fee_score + mcap_score) / 3
            
            filtered_protocols.sort(key=calculate_relevance_score, reverse=True)
            
            # Display results
            if filtered_protocols:
                st.success(f"Found {len(filtered_protocols)} protocols matching your criteria!")
                
                # Display results in a proper format
                st.markdown("### 📊 Search Results")
                
                # Create results grid
                cols = st.columns(min(3, len(filtered_protocols)))
                
                for i, protocol in enumerate(filtered_protocols):
                    col = cols[i % len(cols)]
                    
                    with col:
                        with st.container():
                            st.markdown(f"**{protocol['name']} ({protocol['symbol']})**")
                            st.caption(f"{protocol['consensus']} blockchain")
                            
                            # Metrics
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("TPS", f"{protocol['tps']:,}")
                                st.metric("Fee", f"${protocol['avg_fee']:.4f}")
                            with col2:
                                st.metric("Market Cap", f"${protocol['market_cap']/1e9:.1f}B")
                                st.metric("Type", protocol['type'])
                            
                            # Action button
                            if st.button(f"Analyze {protocol['name']}", key=f"search_{protocol['id']}", use_container_width=True):
                                st.session_state.selected_protocol = protocol['id']
                                st.session_state.current_page = "📈 Analytics"
                                st.rerun()
            else:
                st.warning("No protocols found matching your criteria. Try adjusting your filters.")

if __name__ == "__main__":
    main()