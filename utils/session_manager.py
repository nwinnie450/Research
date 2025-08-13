"""
Session State Management for Streamlit Application
"""
import streamlit as st
from typing import Dict, Any

def init_session_state():
    """Initialize Streamlit session state variables"""
    
    # Navigation state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "🏠 Home"
    
    # Chat state
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # User preferences
    if 'selected_use_case' not in st.session_state:
        st.session_state.selected_use_case = None
    
    if 'user_preferences' not in st.session_state:
        st.session_state.user_preferences = {
            'tps_weight': 0.25,
            'fee_weight': 0.25, 
            'security_weight': 0.25,
            'ecosystem_weight': 0.25
        }
    
    # Search and filter state
    if 'search_filters' not in st.session_state:
        st.session_state.search_filters = {
            'min_tps': 1000,
            'max_fee': 1.0,
            'consensus_types': [],
            'use_case': None,
            'min_market_cap': 100000000
        }
    
    # Results and recommendations
    if 'current_recommendations' not in st.session_state:
        st.session_state.current_recommendations = []
    
    if 'comparison_protocols' not in st.session_state:
        st.session_state.comparison_protocols = []
    
    # API and data state
    if 'api_cache' not in st.session_state:
        st.session_state.api_cache = {}
    
    if 'last_api_call' not in st.session_state:
        st.session_state.last_api_call = None
    
    # UI state
    if 'sidebar_expanded' not in st.session_state:
        st.session_state.sidebar_expanded = True
    
    if 'show_advanced_options' not in st.session_state:
        st.session_state.show_advanced_options = False

def reset_session_state():
    """Reset specific session state variables"""
    st.session_state.chat_messages = []
    st.session_state.current_recommendations = []
    st.session_state.comparison_protocols = []

def update_user_preference(key: str, value: Any):
    """Update a user preference in session state"""
    if 'user_preferences' not in st.session_state:
        st.session_state.user_preferences = {}
    st.session_state.user_preferences[key] = value

def get_user_preference(key: str, default: Any = None):
    """Get a user preference from session state"""
    return st.session_state.user_preferences.get(key, default)

def update_search_filter(key: str, value: Any):
    """Update a search filter in session state"""
    if 'search_filters' not in st.session_state:
        st.session_state.search_filters = {}
    st.session_state.search_filters[key] = value

def get_search_filter(key: str, default: Any = None):
    """Get a search filter from session state"""
    return st.session_state.search_filters.get(key, default)