"""
Advanced Analytics Component for Deep Protocol Analysis
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from services.blockchain_service import BlockchainService
from typing import Dict, List
import time
from datetime import datetime, timedelta

def render_analytics():
    """Render advanced analytics dashboard"""
    
    st.markdown("---")
    st.markdown("### 📈 Advanced Analytics")
    
    blockchain_service = BlockchainService()
    
    # Protocol selector
    protocols = blockchain_service._fetch_protocol_data()
    protocol_names = [p['name'] for p in protocols]
    
    selected_protocol_name = st.selectbox(
        "Select protocol for detailed analysis:",
        options=protocol_names,
        index=0 if not hasattr(st.session_state, 'selected_protocol') else 
              next((i for i, p in enumerate(protocols) if p['id'] == st.session_state.get('selected_protocol')), 0)
    )
    
    selected_protocol = next(p for p in protocols if p['name'] == selected_protocol_name)
    
    # Render analytics sections
    render_protocol_overview(selected_protocol)
    render_performance_analysis(selected_protocol)
    render_ecosystem_analysis(selected_protocol)
    render_risk_analysis(selected_protocol)
    render_competitive_positioning(selected_protocol, protocols)

def render_protocol_overview(protocol: Dict):
    """Render detailed protocol overview"""
    
    st.markdown(f"### 🔍 {protocol['name']} Deep Dive")
    
    # Key metrics cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Market Rank",
            "#2",  # Mock ranking
            delta="↑1",
            help="Ranking by market capitalization"
        )
    
    with col2:
        market_cap = protocol.get('market_cap', 0)
        st.metric(
            "Market Cap",
            f"${market_cap/1e9:.1f}B",
            delta=f"{np.random.uniform(-5, 15):.1f}%",
            help="Current market capitalization"
        )
    
    with col3:
        tvl = protocol.get('tvl', 0)
        st.metric(
            "Total Value Locked",
            f"${tvl/1e9:.1f}B",
            delta=f"{np.random.uniform(-10, 25):.1f}%",
            help="Total value locked in DeFi protocols"
        )
    
    with col4:
        daily_txns = np.random.randint(100000, 5000000)
        st.metric(
            "Daily Transactions",
            f"{daily_txns:,}",
            delta=f"{np.random.uniform(-15, 30):.1f}%",
            help="24-hour transaction volume"
        )
    
    # Protocol details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 Technical Specifications")
        
        specs_data = {
            "Consensus Mechanism": protocol.get('consensus', 'Unknown'),
            "Block Time": f"{np.random.uniform(0.1, 15):.1f} seconds",
            "Block Size": f"{np.random.randint(1, 32)} MB",
            "Programming Language": get_programming_language(protocol['id']),
            "Virtual Machine": get_virtual_machine(protocol['id']),
            "Staking Required": "Yes" if protocol.get('consensus') != 'Proof of Work' else "No"
        }
        
        for key, value in specs_data.items():
            st.markdown(f"**{key}:** {value}")
    
    with col2:
        st.markdown("#### 🌟 Ecosystem Health")
        
        # Create ecosystem health chart
        render_ecosystem_health_chart(protocol)

def render_performance_analysis(protocol: Dict):
    """Render performance analysis with time series data"""
    
    st.markdown("---")
    st.markdown("### ⚡ Performance Analysis")
    
    # Generate mock time series data
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    
    # Mock performance data
    base_tps = protocol.get('tps', 1000)
    tps_data = base_tps + np.random.normal(0, base_tps * 0.1, len(dates))
    
    base_fee = protocol.get('avg_fee', 0.01)
    fee_data = base_fee + np.random.normal(0, base_fee * 0.2, len(dates))
    fee_data = np.maximum(fee_data, 0.0001)  # Ensure positive fees
    
    latency_data = np.random.uniform(0.1, 5, len(dates))
    
    df = pd.DataFrame({
        'Date': dates,
        'TPS': tps_data,
        'Fee': fee_data,
        'Latency': latency_data
    })
    
    # Render performance charts
    col1, col2 = st.columns(2)
    
    with col1:
        render_tps_trend(df)
    
    with col2:
        render_fee_trend(df)
    
    # Network utilization
    render_network_utilization(protocol)

def render_tps_trend(df: pd.DataFrame):
    """Render TPS trend chart"""
    
    st.markdown("#### 📊 TPS Trend (30 Days)")
    
    fig = px.line(
        df, 
        x='Date', 
        y='TPS',
        title="Transaction Throughput Over Time"
    )
    
    fig.update_layout(
        height=300,
        font=dict(family="Inter, sans-serif"),
        xaxis_title="Date",
        yaxis_title="Transactions per Second"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_fee_trend(df: pd.DataFrame):
    """Render fee trend chart"""
    
    st.markdown("#### 💰 Fee Trend (30 Days)")
    
    fig = px.line(
        df,
        x='Date',
        y='Fee', 
        title="Average Transaction Fee Over Time"
    )
    
    fig.update_layout(
        height=300,
        font=dict(family="Inter, sans-serif"),
        xaxis_title="Date",
        yaxis_title="Average Fee (USD)"
    )
    
    fig.update_layout(yaxis=dict(tickformat="$.4f"))
    
    st.plotly_chart(fig, use_container_width=True)

def render_network_utilization(protocol: Dict):
    """Render network utilization analysis"""
    
    st.markdown("#### 🌐 Network Utilization")
    
    # Mock utilization data
    hours = list(range(24))
    utilization = [np.random.uniform(20, 95) for _ in hours]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=hours,
        y=utilization,
        mode='lines+markers',
        name='Network Utilization %',
        line=dict(color='#3B82F6', width=3),
        fill='tonexty'
    ))
    
    fig.update_layout(
        title="Network Utilization by Hour (24h)",
        xaxis_title="Hour of Day",
        yaxis_title="Utilization %",
        height=300,
        font=dict(family="Inter, sans-serif")
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_ecosystem_analysis(protocol: Dict):
    """Render ecosystem and adoption analysis"""
    
    st.markdown("---")
    st.markdown("### 🌟 Ecosystem Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        render_dapp_categories(protocol)
    
    with col2:
        render_developer_activity(protocol)
    
    # Partnership and integration analysis
    render_partnerships_analysis(protocol)

def render_dapp_categories(protocol: Dict):
    """Render dApp ecosystem breakdown"""
    
    st.markdown("#### 🏗️ dApp Categories")
    
    # Mock dApp data
    categories = ['DeFi', 'Gaming', 'NFT', 'Social', 'Infrastructure', 'Other']
    values = np.random.randint(10, 200, len(categories))
    
    fig = px.pie(
        values=values,
        names=categories,
        title=f"dApp Distribution on {protocol['name']}"
    )
    
    fig.update_layout(
        height=400,
        font=dict(family="Inter, sans-serif")
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_developer_activity(protocol: Dict):
    """Render developer activity metrics"""
    
    st.markdown("#### 👨‍💻 Developer Activity")
    
    # Mock developer data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    commits = np.random.randint(500, 2000, len(months))
    active_devs = np.random.randint(100, 800, len(months))
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(x=months, y=commits, name="Commits", marker_color="#3B82F6"),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(x=months, y=active_devs, mode='lines+markers', name="Active Developers", 
                  line=dict(color="#DC2626", width=3)),
        secondary_y=True,
    )
    
    fig.update_xaxes(title_text="Month")
    fig.update_yaxes(title_text="Commits", secondary_y=False)
    fig.update_yaxes(title_text="Active Developers", secondary_y=True)
    
    fig.update_layout(
        height=400,
        font=dict(family="Inter, sans-serif")
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_partnerships_analysis(protocol: Dict):
    """Render partnerships and integrations"""
    
    st.markdown("#### 🤝 Key Partnerships & Integrations")
    
    # Mock partnership data
    partnerships = [
        {"Partner": "Major Exchange A", "Type": "Trading", "Status": "Active", "Impact": "High"},
        {"Partner": "DeFi Protocol B", "Type": "Integration", "Status": "Active", "Impact": "Medium"},
        {"Partner": "Enterprise C", "Type": "Adoption", "Status": "Planned", "Impact": "High"},
        {"Partner": "Infrastructure D", "Type": "Technical", "Status": "Active", "Impact": "Low"}
    ]
    
    df = pd.DataFrame(partnerships)
    
    # Add status colors
    def get_status_color(status):
        colors = {"Active": "🟢", "Planned": "🟡", "Inactive": "🔴"}
        return colors.get(status, "⚪")
    
    df['Status Icon'] = df['Status'].apply(get_status_color)
    
    st.dataframe(
        df[['Status Icon', 'Partner', 'Type', 'Impact']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Status Icon": "Status",
            "Partner": "Partner Organization",
            "Type": "Partnership Type",
            "Impact": "Business Impact"
        }
    )

def render_risk_analysis(protocol: Dict):
    """Render risk analysis dashboard"""
    
    st.markdown("---")
    st.markdown("### ⚠️ Risk Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        render_security_score_breakdown(protocol)
    
    with col2:
        render_risk_factors(protocol)

def render_security_score_breakdown(protocol: Dict):
    """Render detailed security score breakdown"""
    
    st.markdown("#### 🛡️ Security Score Breakdown")
    
    # Mock security metrics
    security_factors = {
        'Consensus Security': np.random.randint(80, 95),
        'Smart Contract Audits': np.random.randint(70, 90),
        'Network Decentralization': np.random.randint(75, 92),
        'Historical Incidents': np.random.randint(85, 98),
        'Bug Bounty Program': np.random.randint(80, 95)
    }
    
    categories = list(security_factors.keys())
    values = list(security_factors.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Security Score',
        line=dict(color='#059669', width=2)
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        height=400,
        font=dict(family="Inter, sans-serif")
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_risk_factors(protocol: Dict):
    """Render key risk factors analysis"""
    
    st.markdown("#### ⚠️ Key Risk Factors")
    
    risk_factors = [
        {"Risk": "Centralization", "Level": "Medium", "Score": 6},
        {"Risk": "Smart Contract Bugs", "Level": "Low", "Score": 3},
        {"Risk": "Regulatory Compliance", "Level": "Medium", "Score": 5},
        {"Risk": "Market Volatility", "Level": "High", "Score": 8},
        {"Risk": "Technical Scalability", "Level": "Low", "Score": 2}
    ]
    
    df = pd.DataFrame(risk_factors)
    
    # Create risk level chart
    fig = px.bar(
        df,
        x='Risk',
        y='Score',
        color='Level',
        color_discrete_map={
            'Low': '#059669',
            'Medium': '#D97706', 
            'High': '#DC2626'
        },
        title="Risk Assessment"
    )
    
    fig.update_layout(
        height=300,
        font=dict(family="Inter, sans-serif"),
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_competitive_positioning(protocol: Dict, all_protocols: List[Dict]):
    """Render competitive positioning analysis"""
    
    st.markdown("---")
    st.markdown("### 🏆 Competitive Positioning")
    
    # Create competitive landscape
    render_competitive_landscape(protocol, all_protocols)
    
    # Strengths and weaknesses
    col1, col2 = st.columns(2)
    
    with col1:
        render_strengths_analysis(protocol)
    
    with col2:
        render_weaknesses_analysis(protocol)

def render_competitive_landscape(protocol: Dict, all_protocols: List[Dict]):
    """Render competitive landscape bubble chart"""
    
    st.markdown("#### 🗺️ Competitive Landscape")
    
    # Prepare competitive data
    df = pd.DataFrame([
        {
            "Protocol": p['name'],
            "TPS": p.get('tps', 0),
            "Security Score": p.get('security_score', 0),
            "Market Cap": p.get('market_cap', 0),
            "Selected": p['name'] == protocol['name']
        }
        for p in all_protocols
    ])
    
    # Create bubble chart
    fig = px.scatter(
        df,
        x="TPS",
        y="Security Score",
        size="Market Cap",
        color="Selected",
        hover_name="Protocol",
        color_discrete_map={True: "#DC2626", False: "#3B82F6"},
        title="Performance vs Security vs Market Cap"
    )
    
    fig.update_layout(
        height=500,
        font=dict(family="Inter, sans-serif"),
        xaxis_title="Transactions Per Second (TPS)",
        yaxis_title="Security Score"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_strengths_analysis(protocol: Dict):
    """Render protocol strengths"""
    
    st.markdown("#### ✅ Key Strengths")
    
    # Mock strengths based on protocol characteristics
    strengths = get_protocol_strengths(protocol)
    
    for strength in strengths:
        st.markdown(f"**{strength['title']}**")
        st.progress(strength['score'] / 100)
        st.markdown(f"*{strength['description']}*")
        st.markdown("")

def render_weaknesses_analysis(protocol: Dict):
    """Render protocol weaknesses"""
    
    st.markdown("#### ⚠️ Areas for Improvement")
    
    # Mock weaknesses based on protocol characteristics  
    weaknesses = get_protocol_weaknesses(protocol)
    
    for weakness in weaknesses:
        st.markdown(f"**{weakness['title']}**")
        st.progress(weakness['severity'] / 100)
        st.markdown(f"*{weakness['description']}*")
        st.markdown("")

# Helper functions
def get_programming_language(protocol_id: str) -> str:
    """Get programming language for protocol"""
    languages = {
        'ethereum': 'Solidity',
        'solana': 'Rust', 
        'polygon': 'Solidity',
        'binance': 'Solidity',
        'avalanche': 'Solidity'
    }
    return languages.get(protocol_id, 'Various')

def get_virtual_machine(protocol_id: str) -> str:
    """Get virtual machine for protocol"""
    vms = {
        'ethereum': 'EVM',
        'solana': 'Sealevel VM',
        'polygon': 'EVM',
        'binance': 'EVM', 
        'avalanche': 'EVM'
    }
    return vms.get(protocol_id, 'Custom VM')

def render_ecosystem_health_chart(protocol: Dict):
    """Render ecosystem health gauge"""
    
    ecosystem_score = protocol.get('ecosystem_score', 75)
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = ecosystem_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Ecosystem Health"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "#3B82F6"},
            'steps': [
                {'range': [0, 50], 'color': "#FEE2E2"},
                {'range': [50, 80], 'color': "#FEF3C7"},
                {'range': [80, 100], 'color': "#D1FAE5"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=300)
    
    st.plotly_chart(fig, use_container_width=True)

def get_protocol_strengths(protocol: Dict) -> List[Dict]:
    """Get protocol strengths based on metrics"""
    
    strengths = []
    
    if protocol.get('tps', 0) > 10000:
        strengths.append({
            'title': 'High Throughput',
            'score': 90,
            'description': 'Excellent transaction processing capability'
        })
    
    if protocol.get('avg_fee', 1) < 0.01:
        strengths.append({
            'title': 'Low Transaction Costs',
            'score': 95,
            'description': 'Very affordable for users and applications'
        })
    
    if protocol.get('security_score', 0) > 85:
        strengths.append({
            'title': 'Strong Security',
            'score': protocol.get('security_score', 85),
            'description': 'Robust security track record and design'
        })
    
    return strengths[:3]  # Return top 3 strengths

def get_protocol_weaknesses(protocol: Dict) -> List[Dict]:
    """Get protocol weaknesses based on metrics"""
    
    weaknesses = []
    
    if protocol.get('tps', 0) < 1000:
        weaknesses.append({
            'title': 'Limited Throughput',
            'severity': 70,
            'description': 'May face scalability challenges during high demand'
        })
    
    if protocol.get('avg_fee', 0) > 1.0:
        weaknesses.append({
            'title': 'High Transaction Costs',
            'severity': 80,
            'description': 'Expensive for frequent transactions and micro-payments'
        })
    
    if protocol.get('ecosystem_score', 100) < 70:
        weaknesses.append({
            'title': 'Limited Ecosystem',
            'severity': 60,
            'description': 'Smaller developer and application ecosystem'
        })
    
    return weaknesses[:3]  # Return top 3 weaknesses