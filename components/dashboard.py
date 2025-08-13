"""
Main Dashboard Component with Protocol Overview and Quick Stats
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
# from services.blockchain_service import BlockchainService  # Removed - service deleted
from services.live_l1_data_service import LiveL1DataService
from typing import Dict, List

def render_dashboard():
    """Render the main dashboard with protocol overview"""
    
    # Initialize live data service
    live_data_service = LiveL1DataService()
    
    st.markdown("---")
    st.markdown("### 📊 Blockchain Protocol Overview")
    
    # Get all protocol data from live service
    market_analysis = live_data_service.get_live_l1_market_analysis()
    protocols_dict = market_analysis.get('protocols', {})
    
    if not protocols_dict:
        st.error("Unable to load blockchain data")
        return
    
    # Convert and map to format expected by existing functions
    protocols = []
    for protocol_id, data in protocols_dict.items():
        mapped_protocol = {
            'id': protocol_id,  # Add required id field
            'name': data.get('name', protocol_id.title()),
            'symbol': data.get('symbol', ''),
            'tps': data.get('current_tps', 0),
            'avg_fee': data.get('avg_fee_usd', 0),
            'security_score': 100 if data.get('consensus') == 'Proof of Work' else 85,  # Simple mapping
            'ecosystem_score': min(data.get('market_cap', 0) / 1e9 * 10, 100),  # Market cap based
            'market_cap': data.get('market_cap', 0),
            'type': 'Layer 1',
            'description': f"{data.get('name', '')} - {data.get('consensus', '')} blockchain",
            'suitable_for': ['DeFi', 'Payments'] if data.get('tvl', 0) > 0 else ['Payments'],
            'active_developers': max(50, int(data.get('market_cap', 0) / 1e8))  # Estimate based on mcap
        }
        protocols.append(mapped_protocol)
    
    # Key metrics row
    render_key_metrics(protocols)
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        render_tps_comparison(protocols)
    
    with col2:
        render_fee_comparison(protocols)
    
    # Protocol cards
    render_protocol_cards(protocols)
    
    # Market overview
    render_market_overview(protocols)

def render_key_metrics(protocols: List[Dict]):
    """Render key metrics summary"""
    
    # Calculate summary metrics
    total_protocols = len(protocols)
    avg_tps = sum(p.get('tps', 0) for p in protocols) / len(protocols)
    lowest_fee = min(p.get('avg_fee', float('inf')) for p in protocols)
    highest_security = max(p.get('security_score', 0) for p in protocols)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Protocols Tracked",
            value=f"{total_protocols}",
            help="Top 5 L1 protocols: Ethereum, Base, Tron, BSC, Bitcoin"
        )
    
    with col2:
        st.metric(
            label="Average TPS",
            value=f"{avg_tps:,.0f}",
            help="Average transactions per second across all protocols"
        )
    
    with col3:
        st.metric(
            label="Lowest Fee",
            value=f"${lowest_fee:.4f}",
            help="Cheapest transaction fee among all protocols"
        )
    
    with col4:
        st.metric(
            label="Top Security",
            value=f"{highest_security}/100",
            help="Highest security score among all protocols"
        )

def render_tps_comparison(protocols: List[Dict]):
    """Render TPS comparison chart"""
    
    st.markdown("#### ⚡ Transaction Throughput (TPS)")
    
    # Prepare data
    df = pd.DataFrame([
        {"Protocol": p["name"], "TPS": p.get("tps", 0)} 
        for p in protocols
    ])
    df = df.sort_values("TPS", ascending=True)
    
    # Create horizontal bar chart
    fig = px.bar(
        df, 
        x="TPS", 
        y="Protocol",
        orientation='h',
        color="TPS",
        color_continuous_scale="blues",
        title="Transactions Per Second"
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        title_font_size=16,
        font=dict(family="Inter, sans-serif")
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_fee_comparison(protocols: List[Dict]):
    """Render transaction fee comparison chart"""
    
    st.markdown("#### 💰 Average Transaction Fees")
    
    # Prepare data
    df = pd.DataFrame([
        {"Protocol": p["name"], "Fee": p.get("avg_fee", 0)} 
        for p in protocols
    ])
    df = df.sort_values("Fee", ascending=False)
    
    # Create bar chart
    fig = px.bar(
        df,
        x="Protocol", 
        y="Fee",
        color="Fee",
        color_continuous_scale="reds_r",  # Reverse scale (lower fees = better)
        title="Average Transaction Fee (USD)"
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        title_font_size=16,
        font=dict(family="Inter, sans-serif"),
        xaxis_tickangle=-45
    )
    
    # Format y-axis to show dollar amounts
    fig.update_layout(yaxis=dict(tickformat="$.4f"))
    
    st.plotly_chart(fig, use_container_width=True)

def render_protocol_cards(protocols: List[Dict]):
    """Render protocol overview cards"""
    
    st.markdown("### 🔗 Protocol Spotlight")
    
    # Sort protocols by a composite score for featured display
    featured_protocols = sorted(
        protocols,
        key=lambda x: (x.get('ecosystem_score', 0) + x.get('security_score', 0)) / 2,
        reverse=True
    )[:6]  # Top 6 protocols
    
    # Create grid layout
    cols = st.columns(3)
    
    for i, protocol in enumerate(featured_protocols):
        col = cols[i % 3]
        
        with col:
            render_protocol_card(protocol)

def render_protocol_card(protocol: Dict):
    """Render individual protocol card"""
    
    # Determine status colors
    tps = protocol.get('tps', 0)
    fee = protocol.get('avg_fee', 0)
    security = protocol.get('security_score', 0)
    
    # Define status colors inline
    def get_status_color(status_type, value):
        if status_type == "tps":
            if value > 10000:
                return "#059669"  # success_green
            elif value > 1000:
                return "#D97706"  # warning_orange
            else:
                return "#DC2626"  # danger_red
        elif status_type == "fee":
            if value < 0.01:
                return "#059669"  # success_green
            elif value < 1.0:
                return "#D97706"  # warning_orange
            else:
                return "#DC2626"  # danger_red
        elif status_type == "security":
            if value > 85:
                return "#059669"  # success_green
            elif value > 70:
                return "#D97706"  # warning_orange
            else:
                return "#DC2626"  # danger_red
        return "#6B7280"  # default gray
    
    # Use container and columns instead of HTML for better compatibility
    with st.container():
        # Protocol header
        st.markdown(f"**{protocol['name']} ({protocol['symbol']})**")
        st.caption(protocol.get('description', 'Leading blockchain protocol'))
        
        # Metrics in columns
        col1, col2 = st.columns(2)
        
        with col1:
            # TPS with color coding
            tps_color = "🟢" if tps > 1000 else "🟡" if tps > 100 else "🔴"
            st.metric("TPS", f"{tps:,}", delta=None)
            
            # Security score
            sec_color = "🟢" if security > 85 else "🟡" if security > 70 else "🔴"
            st.metric("Security", f"{security}/100", delta=None)
        
        with col2:
            # Fee with color coding  
            fee_color = "🟢" if fee < 0.1 else "🟡" if fee < 1.0 else "🔴"
            st.metric("Fee", f"${fee:.4f}", delta=None)
            
            # Type
            st.metric("Type", protocol.get('type', 'Layer 1'), delta=None)
        
        # Best use cases
        st.markdown(f"**Best for:** {', '.join(protocol.get('suitable_for', ['General use']))}")
        
        # Add some spacing
        st.markdown("---")
    
    if st.button(f"Analyze {protocol['name']}", key=f"analyze_{protocol['id']}", use_container_width=True):
        st.session_state.selected_protocol = protocol['id']
        st.session_state.current_page = "📈 Analytics"
        st.rerun()

def render_market_overview(protocols: List[Dict]):
    """Render market overview section"""
    
    st.markdown("---")
    st.markdown("### 📈 Market Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        render_security_vs_performance(protocols)
    
    with col2:
        render_ecosystem_comparison(protocols)

def render_security_vs_performance(protocols: List[Dict]):
    """Render security vs performance scatter plot"""
    
    st.markdown("#### 🛡️ Security vs Performance")
    
    # Prepare data
    df = pd.DataFrame([
        {
            "Protocol": p["name"],
            "TPS": p.get("tps", 0),
            "Security Score": p.get("security_score", 0),
            "Market Cap": p.get("market_cap", 0)
        }
        for p in protocols
    ])
    
    # Create scatter plot
    fig = px.scatter(
        df,
        x="TPS",
        y="Security Score", 
        size="Market Cap",
        hover_name="Protocol",
        color="Security Score",
        color_continuous_scale="viridis",
        title="Security Score vs Transaction Throughput"
    )
    
    fig.update_layout(
        height=400,
        font=dict(family="Inter, sans-serif")
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_ecosystem_comparison(protocols: List[Dict]):
    """Render ecosystem maturity radar chart"""
    
    st.markdown("#### 🌟 Ecosystem Maturity")
    
    # Select top 5 protocols by ecosystem score
    top_protocols = sorted(
        protocols, 
        key=lambda x: x.get('ecosystem_score', 0), 
        reverse=True
    )[:5]
    
    # Create radar chart
    fig = go.Figure()
    
    categories = ['Ecosystem Score', 'Security Score', 'Performance', 'Adoption', 'Developer Activity']
    
    for protocol in top_protocols:
        # Normalize performance score (TPS to 0-100 scale)
        perf_score = min(protocol.get('tps', 0) / 1000, 100)  # 1k TPS = 100 score
        adoption_score = min(protocol.get('market_cap', 0) / 1e9, 100)  # $1B = 100 score
        dev_score = min(protocol.get('active_developers', 0) / 40, 100)  # 4000 devs = 100 score
        
        values = [
            protocol.get('ecosystem_score', 0),
            protocol.get('security_score', 0), 
            perf_score,
            adoption_score,
            dev_score
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=protocol['name'],
            line=dict(width=2)
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        height=400,
        font=dict(family="Inter, sans-serif")
    )
    
    st.plotly_chart(fig, use_container_width=True)