"""
Header Component for Blockchain Research AI Agent
"""
import streamlit as st
from config import APP_TITLE, APP_DESCRIPTION, VERSION

def render_header():
    """Render the main application header"""
    
    st.markdown(f"""
    <div class="main-header">
        <h1>🔗 {APP_TITLE}</h1>
        <p>{APP_DESCRIPTION} • v{VERSION}</p>
    </div>
    """, unsafe_allow_html=True)