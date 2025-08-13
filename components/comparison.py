"""
Blockchain Protocol Comparison Component
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from services.blockchain_service import BlockchainService
from typing import Dict, List

def render_comparison():
    """Render the blockchain comparison interface"""
    
    st.markdown("---")
    st.markdown("### 📊 Protocol Comparison")
    
    blockchain_service = BlockchainService()
    protocols = blockchain_service._fetch_protocol_data()
    
    if not protocols:
        st.error("Unable to load blockchain data for comparison")
        return
    
    # Protocol selection interface
    selected_protocols = render_protocol_selector(protocols)
    
    if len(selected_protocols) < 2:
        st.info("👆 Select at least 2 protocols to compare")
        return
    
    # Generate comparison
    comparison_data = blockchain_service.get_comparative_analysis([p['id'] for p in selected_protocols])
    
    # Render comparison results
    render_comparison_results(selected_protocols, comparison_data)

def render_protocol_selector(protocols: List[Dict]) -> List[Dict]:
    """Render protocol selection interface"""
    
    st.markdown("#### 🔍 Select Protocols to Compare")
    
    # Create selection interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        protocol_names = [p['name'] for p in protocols]
        
        # Pre-select top protocols if available from recommendations
        default_selection = []
        if st.session_state.current_recommendations:
            top_recommendations = st.session_state.current_recommendations[:3]
            default_selection = [p['name'] for p in top_recommendations]
        else:
            # Default to top 3 by ecosystem score
            sorted_protocols = sorted(protocols, key=lambda x: x.get('ecosystem_score', 0), reverse=True)
            default_selection = [p['name'] for p in sorted_protocols[:3]]
        
        selected_names = st.multiselect(
            "Choose blockchain protocols:",
            options=protocol_names,
            default=default_selection[:3],
            help="Select 2-5 protocols for detailed comparison"
        )
    
    with col2:
        st.markdown("**Quick Presets:**")
        
        if st.button("🎮 Gaming Leaders", use_container_width=True):
            gaming_protocols = [p for p in protocols if 'gaming' in p.get('suitable_for', [])]
            selected_names = [p['name'] for p in gaming_protocols[:3]]
            st.rerun()
        
        if st.button("🏦 DeFi Giants", use_container_width=True):
            defi_protocols = [p for p in protocols if 'defi' in p.get('suitable_for', [])]
            selected_names = [p['name'] for p in sorted(defi_protocols, key=lambda x: x.get('tvl', 0), reverse=True)[:3]]
            st.rerun()
        
        if st.button("⚡ Speed Demons", use_container_width=True):
            fast_protocols = sorted(protocols, key=lambda x: x.get('tps', 0), reverse=True)
            selected_names = [p['name'] for p in fast_protocols[:3]]
            st.rerun()
    
    # Return selected protocols
    selected_protocols = [p for p in protocols if p['name'] in selected_names]
    return selected_protocols

def render_comparison_results(selected_protocols: List[Dict], comparison_data: Dict):
    """Render detailed comparison results"""
    
    if len(selected_protocols) < 2:
        return
    
    # Summary comparison table
    render_summary_table(selected_protocols)
    
    # Visual comparisons
    col1, col2 = st.columns(2)
    
    with col1:
        render_performance_comparison(selected_protocols)
    
    with col2:
        render_cost_comparison(selected_protocols)
    
    # Detailed comparison charts
    render_radar_comparison(selected_protocols)
    
    # Head-to-head analysis
    render_head_to_head(selected_protocols)
    
    # Export options
    render_export_options(selected_protocols)

def render_summary_table(protocols: List[Dict]):
    """Render summary comparison table"""
    
    st.markdown("#### 📋 Quick Comparison")
    
    # Prepare table data
    table_data = []
    for protocol in protocols:
        table_data.append({
            "Protocol": protocol['name'],
            "TPS": f"{protocol.get('tps', 0):,}",
            "Avg Fee": f"${protocol.get('avg_fee', 0):.4f}",
            "Finality": f"{protocol.get('finality_time', 0):.1f}s",
            "Security": f"{protocol.get('security_score', 0)}/100",
            "Ecosystem": f"{protocol.get('ecosystem_score', 0)}/100",
            "Type": protocol.get('type', 'Layer 1'),
            "Consensus": protocol.get('consensus', 'Unknown')
        })
    
    df = pd.DataFrame(table_data)
    
    # Style the dataframe
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Protocol": st.column_config.TextColumn("Protocol", width="medium"),
            "TPS": st.column_config.TextColumn("TPS", help="Transactions per second"),
            "Avg Fee": st.column_config.TextColumn("Avg Fee", help="Average transaction fee"),
            "Finality": st.column_config.TextColumn("Finality", help="Time to finality"),
            "Security": st.column_config.TextColumn("Security", help="Security score out of 100"),
            "Ecosystem": st.column_config.TextColumn("Ecosystem", help="Ecosystem maturity score"),
        }
    )

def render_performance_comparison(protocols: List[Dict]):
    """Render performance comparison chart"""
    
    st.markdown("#### ⚡ Performance Metrics")
    
    # Prepare data
    df = pd.DataFrame([
        {
            "Protocol": p['name'],
            "TPS": p.get('tps', 0),
            "Finality (s)": p.get('finality_time', 0)
        }
        for p in protocols
    ])
    
    # Create dual-axis chart
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add TPS bars
    fig.add_trace(
        go.Bar(
            x=df['Protocol'],
            y=df['TPS'],
            name="TPS",
            marker_color="#3B82F6",
            yaxis="y"
        )
    )
    
    # Add finality line
    fig.add_trace(
        go.Scatter(
            x=df['Protocol'],
            y=df['Finality (s)'],
            mode='lines+markers',
            name="Finality Time",
            line=dict(color="#DC2626", width=3),
            marker=dict(size=8),
            yaxis="y2"
        )
    )
    
    # Update layout
    fig.update_xaxes(title_text="Protocol")
    fig.update_yaxes(title_text="Transactions Per Second", secondary_y=False)
    fig.update_yaxes(title_text="Finality Time (seconds)", secondary_y=True)
    
    fig.update_layout(
        height=400,
        font=dict(family="Inter, sans-serif"),
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_cost_comparison(protocols: List[Dict]):
    """Render cost comparison chart"""
    
    st.markdown("#### 💰 Transaction Costs")
    
    # Prepare data
    df = pd.DataFrame([
        {
            "Protocol": p['name'],
            "Fee (USD)": p.get('avg_fee', 0),
            "Daily Cost (100 tx)": p.get('avg_fee', 0) * 100,
            "Monthly Cost (3K tx)": p.get('avg_fee', 0) * 3000
        }
        for p in protocols
    ])
    
    # Create grouped bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Single Transaction',
        x=df['Protocol'],
        y=df['Fee (USD)'],
        marker_color='#059669'
    ))
    
    fig.add_trace(go.Bar(
        name='Daily (100 tx)',
        x=df['Protocol'],
        y=df['Daily Cost (100 tx)'],
        marker_color='#D97706'
    ))
    
    fig.add_trace(go.Bar(
        name='Monthly (3K tx)',
        x=df['Protocol'],
        y=df['Monthly Cost (3K tx)'],
        marker_color='#DC2626'
    ))
    
    fig.update_layout(
        barmode='group',
        height=400,
        yaxis_title='Cost (USD)',
        font=dict(family="Inter, sans-serif"),
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_radar_comparison(protocols: List[Dict]):
    """Render radar chart comparison"""
    
    st.markdown("#### 🕸️ Multi-Dimensional Analysis")
    
    # Create radar chart
    fig = go.Figure()
    
    categories = ['TPS Score', 'Cost Score', 'Security', 'Ecosystem', 'Finality Score']
    
    for protocol in protocols:
        # Normalize scores to 0-100 scale
        tps_score = min(protocol.get('tps', 0) / 1000, 100)  # 1k TPS = 100 score
        cost_score = max(0, 100 - (protocol.get('avg_fee', 1) * 100))  # Lower fees = higher score
        security_score = protocol.get('security_score', 0)
        ecosystem_score = protocol.get('ecosystem_score', 0)
        finality_score = max(0, 100 - (protocol.get('finality_time', 60) * 2))  # Faster = higher score
        
        values = [tps_score, cost_score, security_score, ecosystem_score, finality_score]
        
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
        height=500,
        font=dict(family="Inter, sans-serif")
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_head_to_head(protocols: List[Dict]):
    """Render head-to-head comparison analysis"""
    
    st.markdown("#### 🥊 Head-to-Head Analysis")
    
    if len(protocols) != 2:
        st.info("Select exactly 2 protocols for head-to-head comparison")
        return
    
    protocol_a, protocol_b = protocols
    
    # Create comparison columns
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        render_protocol_summary(protocol_a, "Protocol A")
    
    with col2:
        render_vs_metrics(protocol_a, protocol_b)
    
    with col3:
        render_protocol_summary(protocol_b, "Protocol B")

def render_protocol_summary(protocol: Dict, label: str):
    """Render individual protocol summary for head-to-head"""
    
    st.markdown(f"**{label}: {protocol['name']}**")
    
    st.markdown(f"""
    <div class="protocol-card" style="text-align: center;">
        <h4 style="color: #1E3A8A; margin-bottom: 1rem;">
            {protocol['name']}
        </h4>
        
        <div style="margin-bottom: 0.5rem;">
            <strong>TPS:</strong> {protocol.get('tps', 0):,}
        </div>
        
        <div style="margin-bottom: 0.5rem;">
            <strong>Fee:</strong> ${protocol.get('avg_fee', 0):.4f}
        </div>
        
        <div style="margin-bottom: 0.5rem;">
            <strong>Security:</strong> {protocol.get('security_score', 0)}/100
        </div>
        
        <div style="margin-bottom: 0.5rem;">
            <strong>Ecosystem:</strong> {protocol.get('ecosystem_score', 0)}/100
        </div>
        
        <div style="margin-top: 1rem;">
            <small>{protocol.get('description', '')}</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_vs_metrics(protocol_a: Dict, protocol_b: Dict):
    """Render comparison metrics between two protocols"""
    
    st.markdown("**🔥 Winner Takes All**")
    
    comparisons = [
        ("TPS", "tps", "higher"),
        ("Fee", "avg_fee", "lower"),
        ("Security", "security_score", "higher"),
        ("Ecosystem", "ecosystem_score", "higher"),
        ("Finality", "finality_time", "lower")
    ]
    
    results_html = '<div class="comparison-results" style="text-align: center;">'
    
    for metric, field, better in comparisons:
        val_a = protocol_a.get(field, 0)
        val_b = protocol_b.get(field, 0)
        
        if better == "higher":
            winner = protocol_a['name'] if val_a > val_b else protocol_b['name'] if val_b > val_a else "Tie"
        else:
            winner = protocol_a['name'] if val_a < val_b else protocol_b['name'] if val_b < val_a else "Tie"
        
        color = "#059669" if winner != "Tie" else "#6B7280"
        
        results_html += f'''
        <div style="margin-bottom: 1rem; padding: 0.5rem; background: {color}15; border-radius: 6px;">
            <strong>{metric} Winner:</strong><br>
            <span style="color: {color}; font-weight: bold;">{winner}</span>
        </div>
        '''
    
    results_html += '</div>'
    
    st.markdown(results_html, unsafe_allow_html=True)

def render_export_options(protocols: List[Dict]):
    """Render export and sharing options"""
    
    st.markdown("---")
    st.markdown("#### 📤 Export & Share")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export as PDF", use_container_width=True):
            st.info("PDF export feature coming soon!")
    
    with col2:
        if st.button("📋 Copy Comparison", use_container_width=True):
            comparison_text = generate_comparison_text(protocols)
            st.code(comparison_text, language="markdown")
    
    with col3:
        if st.button("🔗 Share Link", use_container_width=True):
            protocol_ids = ",".join([p['id'] for p in protocols])
            share_url = f"https://your-app.com/compare?protocols={protocol_ids}"
            st.code(share_url)

def generate_comparison_text(protocols: List[Dict]) -> str:
    """Generate text summary of comparison"""
    
    text = "# Blockchain Protocol Comparison\\n\\n"
    
    for i, protocol in enumerate(protocols, 1):
        text += f"## {i}. {protocol['name']} ({protocol['symbol']})\\n"
        text += f"- **TPS:** {protocol.get('tps', 0):,}\\n"
        text += f"- **Average Fee:** ${protocol.get('avg_fee', 0):.4f}\\n"
        text += f"- **Finality:** {protocol.get('finality_time', 0):.1f} seconds\\n"
        text += f"- **Security Score:** {protocol.get('security_score', 0)}/100\\n"
        text += f"- **Ecosystem Score:** {protocol.get('ecosystem_score', 0)}/100\\n"
        text += f"- **Type:** {protocol.get('type', 'Layer 1')}\\n"
        text += f"- **Consensus:** {protocol.get('consensus', 'Unknown')}\\n\\n"
    
    return text