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
    
    /* Global Styles - Compact for Streamlit Cloud */
    .main {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        max-width: 1200px;
        margin: 0 auto;
    }}
    
    /* Make everything more compact and center-aligned */
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
    }}
    
    /* Center align main content area */
    .main .block-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }}
    
    /* Center align content sections */
    .stMarkdown, .stDataFrame, .stPlotlyChart, .stMetric {{
        width: 100%;
        text-align: center;
    }}
    
    /* Center align form elements */
    .stForm {{
        margin: 0 auto;
        text-align: center;
    }}
    
    /* Center align button groups */
    .stButton {{
        text-align: center;
        margin: 0 auto;
    }}
    
    /* Center align columns content */
    .stColumn > div {{
        text-align: center;
    }}
    
    /* Reduce default Streamlit spacing */
    .stApp {{
        margin-top: -80px;
    }}
    
    /* Compact headers and text - Center aligned */
    h1, .stMarkdown h1 {{
        font-size: 1.8rem !important;
        margin-top: 1rem !important;
        margin-bottom: 0.5rem !important;
        line-height: 1.2 !important;
        text-align: center !important;
    }}
    
    h2, .stMarkdown h2 {{
        font-size: 1.5rem !important;
        margin-top: 0.8rem !important;
        margin-bottom: 0.4rem !important;
        line-height: 1.2 !important;
        text-align: center !important;
    }}
    
    h3, .stMarkdown h3 {{
        font-size: 1.3rem !important;
        margin-top: 0.6rem !important;
        margin-bottom: 0.3rem !important;
        line-height: 1.2 !important;
        text-align: center !important;
    }}
    
    h4, .stMarkdown h4 {{
        font-size: 1.1rem !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.2rem !important;
        line-height: 1.2 !important;
        text-align: center !important;
    }}
    
    /* Compact paragraphs */
    p, .stMarkdown p {{
        font-size: 0.9rem !important;
        line-height: 1.4 !important;
        margin-bottom: 0.5rem !important;
    }}
    
    /* Compact metrics */
    .stMetric {{
        background: white;
        padding: 0.5rem !important;
        border-radius: 6px;
        border: 1px solid #e5e7eb;
        margin-bottom: 0.5rem !important;
    }}
    
    .stMetric > div {{
        gap: 0.2rem !important;
    }}
    
    .stMetric [data-testid="metric-container"] {{
        padding: 0.3rem !important;
    }}
    
    .stMetric label {{
        font-size: 0.8rem !important;
        font-weight: 500 !important;
    }}
    
    .stMetric [data-testid="metric-container"] > div {{
        font-size: 1.2rem !important;
        font-weight: 600 !important;
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
    
    /* Compact Hero Section */
    .hero-section {{
        text-align: center;
        padding: 1.2rem 1rem;
        background: {COLORS['light_blue']};
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid {COLORS['secondary_blue']}20;
    }}
    
    .hero-section h1 {{
        font-size: 1.6rem !important;
        margin-bottom: 0.5rem !important;
        line-height: 1.2 !important;
    }}
    
    .hero-section p {{
        font-size: 0.9rem !important;
        margin-bottom: 0.5rem !important;
        line-height: 1.3 !important;
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
    
    /* Compact Button Styles */
    .stButton > button {{
        background: {COLORS['secondary_blue']};
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.4rem 0.8rem !important;
        font-weight: 500;
        font-size: 0.85rem !important;
        height: auto !important;
        min-height: 32px !important;
        transition: all 0.2s ease;
        margin: 0.2rem 0 !important;
    }}
    
    .stButton > button:hover {{
        background: {COLORS['primary_blue']};
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }}
    
    /* Compact sidebar - Keep left-aligned */
    .css-1d391kg, .css-1v3fvcr {{
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }}
    
    /* Sidebar content should remain left-aligned */
    .sidebar .stMarkdown, .sidebar .stRadio, .sidebar .stButton {{
        text-align: left !important;
    }}
    
    /* Override center alignment for sidebar */
    [data-testid="stSidebar"] * {{
        text-align: left !important;
    }}
    
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {{
        text-align: left !important;
    }}
    
    /* Compact radio buttons */
    .stRadio > div {{
        gap: 0.3rem !important;
    }}
    
    .stRadio label {{
        font-size: 0.9rem !important;
        padding: 0.3rem 0 !important;
    }}
    
    /* Compact selectbox */
    .stSelectbox > div > div {{
        font-size: 0.9rem !important;
    }}
    
    /* Compact text input */
    .stTextInput > div > div > input {{
        font-size: 0.9rem !important;
        padding: 0.4rem 0.6rem !important;
    }}
    
    /* Compact columns spacing */
    .stColumn {{
        padding: 0 0.5rem !important;
    }}
    
    /* Compact dataframes - Center aligned */
    .stDataFrame {{
        font-size: 0.85rem !important;
        margin: 0 auto !important;
        text-align: center !important;
    }}
    
    .stDataFrame th {{
        font-size: 0.8rem !important;
        padding: 0.3rem 0.5rem !important;
        text-align: center !important;
    }}
    
    .stDataFrame td {{
        padding: 0.3rem 0.5rem !important;
        text-align: center !important;
    }}
    
    /* Center align Plotly charts */
    .stPlotlyChart {{
        display: flex !important;
        justify-content: center !important;
        margin: 0 auto !important;
    }}
    
    /* Center align metric groups */
    .metric-container {{
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 1rem;
        margin: 0 auto;
    }}
    
    /* Center align cards and containers */
    .element-container {{
        text-align: center;
    }}
    
    /* Compact expandable sections */
    .stExpander {{
        border-radius: 6px;
        margin-bottom: 0.5rem !important;
    }}
    
    .streamlit-expanderHeader {{
        font-size: 0.95rem !important;
        font-weight: 500 !important;
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
    
    /* Enhanced Responsive Design - Maintain center alignment */
    @media (max-width: 768px) {{
        .block-container {{
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            text-align: center !important;
        }}
        
        .main-header h1 {{
            font-size: 1.4rem !important;
            text-align: center !important;
        }}
        
        .hero-section {{
            padding: 1rem 0.8rem;
            text-align: center !important;
        }}
        
        .hero-section h1 {{
            font-size: 1.3rem !important;
            text-align: center !important;
        }}
        
        .hero-section p {{
            font-size: 0.85rem !important;
            text-align: center !important;
        }}
        
        .recommendation-card {{
            padding: 0.8rem;
            margin: 0.5rem auto;
            text-align: center !important;
        }}
        
        .metric-value {{
            font-size: 1.2rem !important;
        }}
        
        .stColumn {{
            padding: 0 0.25rem !important;
            text-align: center !important;
        }}
        
        .stColumn > div {{
            text-align: center !important;
        }}
        
        h1 {{
            font-size: 1.4rem !important;
            text-align: center !important;
        }}
        
        h2 {{
            font-size: 1.2rem !important;
            text-align: center !important;
        }}
        
        h3 {{
            font-size: 1.1rem !important;
            text-align: center !important;
        }}
        
        .stButton > button {{
            font-size: 0.8rem !important;
            padding: 0.3rem 0.6rem !important;
        }}
        
        .stButton {{
            text-align: center !important;
            margin: 0 auto !important;
        }}
        
        /* Keep sidebar left-aligned on mobile */
        [data-testid="stSidebar"] * {{
            text-align: left !important;
        }}
    }}
    
    /* Ultra-wide screens - prevent too much stretching */
    @media (min-width: 1400px) {{
        .block-container {{
            max-width: 1200px !important;
            margin: 0 auto !important;
        }}
    }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)