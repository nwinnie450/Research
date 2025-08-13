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
    
    # Main layout
    col1, col2 = st.columns([1, 3])
    
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
        elif selected_page == "🔍 Advanced":
            render_advanced_search()
        else:
            render_home_page()

def render_home_page():
    """Render the main home/dashboard page"""
    st.markdown("---")
    
    # Hero section
    st.markdown("""
    <div class="hero-section">
        <h1 style="text-align: center; color: #1E3A8A; margin-bottom: 0.5rem;">
            Find Your Perfect L1 Blockchain Protocol
        </h1>
        <p style="text-align: center; color: #6B7280; font-size: 1.2rem; margin-bottom: 2rem;">
            AI-powered analysis of Ethereum, Base, Tron, BSC & Bitcoin
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick action cards focused on L1 protocols
    st.markdown("### 🚀 Quick Start - L1 Protocol Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎮 L1 Gaming Analysis", use_container_width=True):
            st.session_state.selected_use_case = "gaming"
            st.session_state.current_page = "💬 Chat"
            st.rerun()
    
    with col2:
        if st.button("💰 L1 Payment Solutions", use_container_width=True):
            st.session_state.selected_use_case = "payments"
            st.session_state.current_page = "💬 Chat"
            st.rerun()
    
    with col3:
        if st.button("🏢 L1 Enterprise Analysis", use_container_width=True):
            st.session_state.selected_use_case = "enterprise"
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
                ["Proof of Work", "Proof of Stake", "Delegated PoS", "Byzantine Fault Tolerance"],
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
            # This would integrate with the actual search logic
            st.success("Found 8 protocols matching your criteria!")
            
            # Display mock results
            st.markdown("### Results")
            for i in range(3):
                with st.container():
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Protocol", f"Protocol {i+1}")
                    with col2:
                        st.metric("TPS", f"{1000*(i+1):,}")
                    with col3:
                        st.metric("Fee", f"${0.01*(i+1):.3f}")
                    with col4:
                        st.metric("Score", f"{90-i*5}/100")

if __name__ == "__main__":
    main()