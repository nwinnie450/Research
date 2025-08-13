"""
Custom CSS Styles for Blockchain Research AI Agent
Based on design specifications from DESIGN_SPEC.md
"""
import streamlit as st
from config import COLORS

def load_custom_css():
    """Load custom CSS styles for the application"""
    
    css = f"""
    <style>
    /* Import Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Global Styles */
    .main {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}
    
    /* Header Styles */
    .main-header {{
        background: linear-gradient(90deg, {COLORS['primary_blue']} 0%, {COLORS['secondary_blue']} 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
    }}
    
    .main-header h1 {{
        margin: 0;
        font-size: 2.25rem;
        font-weight: 700;
    }}
    
    .main-header p {{
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }}
    
    /* Hero Section */
    .hero-section {{
        text-align: center;
        padding: 2rem 1rem;
        background: {COLORS['light_blue']};
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid {COLORS['secondary_blue']}20;
    }}
    
    /* Card Styles */
    .recommendation-card {{
        background: {COLORS['white']};
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }}
    
    .recommendation-card:hover {{
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transform: translateY(-2px);
        border-color: {COLORS['secondary_blue']};
    }}
    
    .protocol-card {{
        background: {COLORS['white']};
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.2s ease;
    }}
    
    .protocol-card:hover {{
        border-color: {COLORS['secondary_blue']};
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    
    /* Ranking Badges */
    .rank-badge {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.875rem;
        margin-right: 0.5rem;
    }}
    
    .rank-1 {{
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #8B4513;
    }}
    
    .rank-2 {{
        background: linear-gradient(135deg, #C0C0C0, #A0A0A0);
        color: #4A4A4A;
    }}
    
    .rank-3 {{
        background: linear-gradient(135deg, #CD7F32, #B87333);
        color: #FFFFFF;
    }}
    
    .rank-other {{
        background: {COLORS['light_gray']};
        color: {COLORS['medium_gray']};
    }}
    
    /* Chat Interface Styles */
    .chat-container {{
        background: {COLORS['white']};
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }}
    
    .chat-message {{
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        max-width: 85%;
    }}
    
    .user-message {{
        background: {COLORS['secondary_blue']};
        color: white;
        margin-left: auto;
        text-align: right;
    }}
    
    .bot-message {{
        background: {COLORS['light_gray']};
        color: {COLORS['dark_gray']};
        margin-right: auto;
    }}
    
    /* Metric Cards */
    .metric-card {{
        background: {COLORS['white']};
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        transition: all 0.2s ease;
    }}
    
    .metric-card:hover {{
        border-color: {COLORS['secondary_blue']};
        transform: translateY(-1px);
    }}
    
    .metric-value {{
        font-size: 1.75rem;
        font-weight: 700;
        color: {COLORS['primary_blue']};
        margin-bottom: 0.25rem;
    }}
    
    .metric-label {{
        font-size: 0.875rem;
        color: {COLORS['medium_gray']};
        text-transform: uppercase;
        font-weight: 500;
        letter-spacing: 0.5px;
    }}
    
    /* Status Indicators */
    .status-high {{
        color: {COLORS['success_green']};
        font-weight: 600;
    }}
    
    .status-medium {{
        color: {COLORS['warning_orange']};
        font-weight: 600;
    }}
    
    .status-low {{
        color: {COLORS['danger_red']};
        font-weight: 600;
    }}
    
    /* Comparison Table Styles */
    .comparison-table {{
        background: {COLORS['white']};
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #e5e7eb;
    }}
    
    .comparison-table th {{
        background: {COLORS['primary_blue']};
        color: white;
        padding: 0.75rem 1rem;
        font-weight: 600;
    }}
    
    .comparison-table td {{
        padding: 0.75rem 1rem;
        border-bottom: 1px solid #f3f4f6;
    }}
    
    /* Button Styles */
    .stButton > button {{
        background: {COLORS['secondary_blue']};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }}
    
    .stButton > button:hover {{
        background: {COLORS['primary_blue']};
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }}
    
    /* Success/Error/Warning Messages */
    .success-message {{
        background: {COLORS['success_green']}15;
        border: 1px solid {COLORS['success_green']};
        color: {COLORS['success_green']};
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    
    .error-message {{
        background: {COLORS['danger_red']}15;
        border: 1px solid {COLORS['danger_red']};
        color: {COLORS['danger_red']};
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    
    .warning-message {{
        background: {COLORS['warning_orange']}15;
        border: 1px solid {COLORS['warning_orange']};
        color: {COLORS['warning_orange']};
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    
    /* Loading Animation */
    .loading-spinner {{
        border: 3px solid {COLORS['light_gray']};
        border-top: 3px solid {COLORS['secondary_blue']};
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 1rem auto;
    }}
    
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    
    /* Sidebar Styles */
    .css-1d391kg {{
        background: {COLORS['light_blue']};
    }}
    
    /* Hide Streamlit Menu and Footer */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {{
        width: 6px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {COLORS['light_gray']};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {COLORS['medium_gray']};
        border-radius: 3px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {COLORS['primary_blue']};
    }}
    
    /* Responsive Design */
    @media (max-width: 768px) {{
        .main-header h1 {{
            font-size: 1.75rem;
        }}
        
        .hero-section {{
            padding: 1.5rem 1rem;
        }}
        
        .recommendation-card {{
            padding: 1rem;
        }}
        
        .metric-value {{
            font-size: 1.5rem;
        }}
    }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)