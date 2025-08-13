"""
Sidebar Navigation Component
"""
import streamlit as st

def render_sidebar():
    """Render the sidebar navigation menu"""
    
    with st.sidebar:
        st.markdown("### 🎯 Navigation")
        
        # Simple radio button navigation (fallback if streamlit-option-menu not available)
        selected = st.radio(
            "Choose a page:",
            ["🏠 Home", "💬 Chat", "📊 Compare", "📈 Analytics", "🔍 Advanced"],
            index=0,
            label_visibility="collapsed"
        )
        
        # Quick actions section
        st.markdown("---")
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🎮 Find Gaming Chain", use_container_width=True):
            st.session_state.selected_use_case = "gaming"
            st.session_state.current_page = "💬 Chat"
            selected = "💬 Chat"
        
        if st.button("🏦 DeFi Protocols", use_container_width=True):
            st.session_state.selected_use_case = "defi"
            st.session_state.current_page = "💬 Chat"
            selected = "💬 Chat"
        
        if st.button("🏢 Enterprise Blockchain", use_container_width=True):
            st.session_state.selected_use_case = "enterprise"
            st.session_state.current_page = "💬 Chat"
            selected = "💬 Chat"
        
        # Settings section
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        
        with st.expander("Preferences", expanded=False):
            st.slider("TPS Priority", 0.0, 1.0, 0.25, key="tps_weight")
            st.slider("Fee Priority", 0.0, 1.0, 0.25, key="fee_weight")
            st.slider("Security Priority", 0.0, 1.0, 0.25, key="security_weight")
            st.slider("Ecosystem Priority", 0.0, 1.0, 0.25, key="ecosystem_weight")
        
        # Information section
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        **Blockchain Research AI Agent** helps you find the perfect blockchain protocol for your project using AI-powered analysis and real-time data.
        
        **Features:**
        - 🤖 AI-powered recommendations
        - 📊 Real-time blockchain data
        - 🔍 Advanced filtering
        - 📈 Interactive comparisons
        - 📱 Mobile-responsive design
        """)
        
        # Update session state
        st.session_state.current_page = selected
        
        return selected