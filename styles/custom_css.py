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
    
    /* GRID SYSTEM - Full viewport layout */
    :root {{
        --grid-unit: 8px;
        --grid-2x: 16px;
        --grid-3x: 24px;
        --grid-4x: 32px;
        --grid-6x: 48px;
        --grid-8x: 64px;
        --section-gap: 48px;
        --content-gap: 24px;
        --line-height-base: 1.5;
        --line-height-tight: 1.25;
    }}
    
    /* Global Styles - Full viewport */
    .main {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        width: 100vw;
        max-width: 100vw;
        margin: 0;
        padding: 0;
        line-height: var(--line-height-base);
    }}
    
    /* Content container - Full available space */
    .block-container {{
        padding: var(--grid-2x) var(--grid-3x) !important;
        max-width: 100% !important;
        margin: 0 !important;
        width: 100% !important;
        box-sizing: border-box;
    }}
    
    /* Main content - Use all available space */
    .main .block-container {{
        display: block;
        width: 100%;
        max-width: 100%;
        padding: var(--grid-2x) var(--grid-3x);
        box-sizing: border-box;
        margin: 0;
    }}
    
    /* Override Streamlit's container restrictions */
    .stApp > div:first-child {{
        width: 100% !important;
        max-width: 100% !important;
    }}
    
    [data-testid="stAppViewContainer"] {{
        width: 100% !important;
        max-width: 100% !important;
    }}
    
    /* Section spacing system */
    .section {{
        margin-bottom: var(--section-gap);
    }}
    
    .section:last-child {{
        margin-bottom: 0;
    }}
    
    /* COMPONENT ALIGNMENT SYSTEM */
    
    /* Content sections - full-width with proper spacing */
    .stMarkdown, .stDataFrame, .stPlotlyChart, .stMetric {{
        width: 100%;
        margin-bottom: var(--content-gap);
        box-sizing: border-box;
    }}
    
    /* Form elements - better proportioned */
    .stForm {{
        max-width: 800px;
        margin: var(--content-gap) auto;
        padding: var(--grid-3x);
        width: 100%;
        box-sizing: border-box;
    }}
    
    /* BUTTON SYSTEM - Perfect centering with consistent spacing */
    .button-group {{
        display: flex;
        justify-content: center;
        gap: var(--grid-3x);
        margin: var(--grid-2x) 0 var(--content-gap) 0;
        flex-wrap: wrap;
    }}
    
    .stButton {{
        margin: 0;
        flex: 0 0 auto;
    }}
    
    /* Equal width buttons in column layouts */
    .stColumns .stButton {{
        width: 100%;
        margin: var(--grid-unit) 0;
    }}
    
    /* COLUMN SYSTEM - Proper gaps and equal heights */
    .stColumn {{
        padding: 0 calc(var(--grid-2x) / 2) !important;
        box-sizing: border-box;
    }}
    
    .stColumn > div {{
        height: 100%;
        display: flex;
        flex-direction: column;
        box-sizing: border-box;
    }}
    
    /* Equal height cards */
    .stColumns {{
        gap: var(--grid-3x) !important;
        margin-bottom: var(--content-gap);
    }}
    
    .stColumns > div {{
        height: 100%;
        display: flex;
        flex-direction: column;
    }}
    
    /* Reduce default Streamlit spacing */
    .stApp {{
        margin-top: -80px;
    }}
    
    /* TYPOGRAPHY SYSTEM - Larger, more prominent text */
    
    /* Main title - bigger and bolder */
    h1, .stMarkdown h1 {{
        font-size: 2.75rem !important;
        margin: 0 0 var(--grid-3x) 0 !important;
        line-height: var(--line-height-tight) !important;
        text-align: left !important;
        font-weight: 700 !important;
        width: 100%;
        display: flex;
        align-items: center;
        gap: var(--grid-3x);
    }}
    
    /* Section headings - larger and more prominent */
    h2, .stMarkdown h2 {{
        font-size: 2.125rem !important;
        margin: var(--section-gap) 0 var(--content-gap) 0 !important;
        line-height: var(--line-height-tight) !important;
        text-align: left !important;
        font-weight: 600 !important;
        width: 100%;
        display: flex;
        align-items: center;
        gap: var(--grid-3x);
    }}
    
    h2:first-child {{
        margin-top: 0 !important;
    }}
    
    /* Subsection headings - increased size */
    h3, .stMarkdown h3 {{
        font-size: 1.625rem !important;
        margin: var(--grid-4x) 0 var(--grid-2x) 0 !important;
        line-height: var(--line-height-tight) !important;
        text-align: left !important;
        font-weight: 600 !important;
        width: 100%;
        display: flex;
        align-items: center;
        gap: var(--grid-3x);
    }}
    
    /* Card titles - larger for better readability */
    h4, .stMarkdown h4 {{
        font-size: 1.25rem !important;
        margin: var(--grid-2x) 0 var(--grid-unit) 0 !important;
        line-height: var(--line-height-tight) !important;
        text-align: left !important;
        font-weight: 500 !important;
        width: 100%;
    }}
    
    /* Paragraph text - larger for better readability */
    p, .stMarkdown p {{
        font-size: 1.125rem !important;
        line-height: var(--line-height-base) !important;
        margin: 0 0 var(--grid-2x) 0 !important;
        width: 100%;
        text-align: left;
    }}
    
    /* Icon + text alignment in headings */
    h1 .icon, h2 .icon, h3 .icon {{
        display: inline-flex;
        align-items: center;
        font-size: 0.9em;
    }}
    
    /* Enhanced metrics - larger and more prominent */
    .stMetric {{
        background: white;
        padding: var(--grid-3x) !important;
        border-radius: var(--grid-2x);
        border: 1px solid #e5e7eb;
        margin-bottom: var(--grid-2x) !important;
        min-height: 140px;
    }}
    
    .stMetric > div {{
        gap: var(--grid-unit) !important;
    }}
    
    .stMetric [data-testid="metric-container"] {{
        padding: var(--grid-2x) !important;
    }}
    
    .stMetric label {{
        font-size: 1rem !important;
        font-weight: 500 !important;
    }}
    
    .stMetric [data-testid="metric-container"] > div {{
        font-size: 1.75rem !important;
        font-weight: 600 !important;
    }}
    
    /* Metric values - even larger */
    .stMetric [data-testid="metric-container"] > div:first-child {{
        font-size: 2.25rem !important;
        font-weight: 700 !important;
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
    
    /* BUTTON SYSTEM - Larger, more prominent buttons */
    .stButton > button {{
        background: {COLORS['secondary_blue']};
        color: white;
        border: none;
        border-radius: var(--grid-2x);
        padding: var(--grid-3x) var(--grid-4x) !important;
        font-weight: 500;
        font-size: 1.125rem !important;
        height: var(--grid-8x) !important;
        min-width: 160px;
        transition: all 0.2s ease;
        margin: var(--grid-2x) 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        box-sizing: border-box;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    
    .stButton > button:hover {{
        background: {COLORS['primary_blue']};
        transform: translateY(-3px);
        box-shadow: 0 var(--grid-2x) var(--grid-3x) rgba(0,0,0,0.2);
    }}
    
    /* Button groups - equal width in rows */
    .stColumns .stButton {{
        width: 100%;
    }}
    
    .stColumns .stButton > button {{
        width: 100%;
        min-width: unset;
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
    
    /* DATA TABLE SYSTEM - Larger, more readable tables */
    .stDataFrame {{
        font-size: 1.1rem !important;
        margin: var(--grid-3x) auto !important;
        text-align: center !important;
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: auto;
        border-radius: var(--grid-2x);
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }}
    
    .stDataFrame th {{
        font-size: 1rem !important;
        padding: var(--grid-3x) var(--grid-2x) !important;
        text-align: center !important;
        font-weight: 600 !important;
        background: {COLORS['light_gray']};
        height: var(--grid-8x);
        vertical-align: middle;
    }}
    
    .stDataFrame td {{
        padding: var(--grid-3x) var(--grid-2x) !important;
        text-align: center !important;
        height: var(--grid-6x);
        vertical-align: middle;
        border-bottom: 1px solid #f3f4f6;
        font-size: 1.05rem !important;
    }}
    
    /* CHART SYSTEM - Consistent sizing and alignment */
    .stPlotlyChart {{
        width: 100% !important;
        max-width: 100% !important;
        margin: var(--grid-3x) auto !important;
        text-align: center !important;
        border-radius: var(--grid-unit);
        overflow: hidden;
    }}
    
    .stPlotlyChart > div {{
        width: 100% !important;
        margin: 0 auto !important;
        border-radius: var(--grid-unit);
    }}
    
    /* CARD GRID SYSTEM - 3-4 column uniform layout */
    .protocol-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: var(--grid-3x);
        margin-bottom: var(--content-gap);
        width: 100%;
    }}
    
    .metric-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: var(--grid-3x);
        margin-bottom: var(--content-gap);
        width: 100%;
    }}
    
    /* Larger, more prominent cards */
    .protocol-card, .metric-card {{
        min-height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: var(--grid-4x);
        border-radius: var(--grid-3x);
        border: 1px solid #e5e7eb;
        background: white;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }}
    
    .protocol-card:hover, .metric-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 var(--grid-2x) var(--grid-4x) rgba(0,0,0,0.15);
        border-color: {COLORS['secondary_blue']};
    }}
    
    /* Card content sizing */
    .protocol-card h3, .metric-card h3 {{
        font-size: 1.375rem !important;
        margin-bottom: var(--grid-2x) !important;
    }}
    
    .protocol-card p, .metric-card p {{
        font-size: 1.1rem !important;
        line-height: 1.5 !important;
    }}
    
    .protocol-card .metric-value, .metric-card .metric-value {{
        font-size: 2rem !important;
        font-weight: 700 !important;
    }}
    
    /* Element containers - no extra spacing */
    .element-container {{
        margin: 0;
        width: 100%;
    }}
    
    /* Streamlit metrics - uniform sizing */
    .stMetric {{
        min-height: 120px;
        padding: var(--grid-3x) !important;
        margin: 0 !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: var(--grid-2x);
        transition: all 0.2s ease;
    }}
    
    .stMetric:hover {{
        transform: translateY(-2px);
        box-shadow: 0 var(--grid-unit) var(--grid-3x) rgba(0,0,0,0.1);
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
    
    /* RESPONSIVE DESIGN - Maintains grid system across screen sizes */
    
    /* Mobile - Stack cards, reduce spacing */
    @media (max-width: 768px) {{
        :root {{
            --section-gap: 32px;
            --content-gap: 16px;
        }}
        
        .block-container {{
            padding: var(--grid-2x) !important;
            width: 100% !important;
            max-width: 100% !important;
        }}
        
        .main .block-container {{
            padding: var(--grid-2x);
            width: 100%;
            max-width: 100%;
        }}
        
        /* Single column grids on mobile */
        .protocol-grid, .metric-grid {{
            grid-template-columns: 1fr;
            gap: var(--grid-2x);
        }}
        
        /* Smaller cards on mobile */
        .protocol-card, .metric-card {{
            min-height: 140px;
            padding: var(--grid-2x);
        }}
        
        /* Adjust typography for mobile */
        h1, .stMarkdown h1 {{
            font-size: 1.75rem !important;
            text-align: center !important;
            justify-content: center;
        }}
        
        h2, .stMarkdown h2 {{
            font-size: 1.375rem !important;
            text-align: center !important;
            justify-content: center;
        }}
        
        h3, .stMarkdown h3 {{
            font-size: 1.125rem !important;
            text-align: center !important;
            justify-content: center;
        }}
        
        p, .stMarkdown p {{
            text-align: center !important;
        }}
        
        /* Button adjustments */
        .button-group {{
            flex-direction: column;
            align-items: center;
            gap: var(--grid-2x);
        }}
        
        .stButton > button {{
            font-size: 0.85rem !important;
            padding: var(--grid-2x) var(--grid-3x) !important;
            min-width: 200px;
        }}
    }}
    
    /* Tablet - 2 column grids */
    @media (min-width: 769px) and (max-width: 1024px) {{
        .block-container {{
            width: 100% !important;
            max-width: 100% !important;
        }}
        
        .protocol-grid {{
            grid-template-columns: repeat(2, 1fr);
        }}
        
        .metric-grid {{
            grid-template-columns: repeat(3, 1fr);
        }}
    }}
    
    /* Desktop - 3+ column grids */
    @media (min-width: 1025px) {{
        .block-container {{
            width: 100% !important;
            max-width: 100% !important;
            padding: var(--grid-3x) var(--grid-4x) !important;
        }}
        
        .protocol-grid {{
            grid-template-columns: repeat(4, 1fr);
        }}
        
        .metric-grid {{
            grid-template-columns: repeat(5, 1fr);
        }}
    }}
    
    /* Large screens - Maximum columns */
    @media (min-width: 1400px) {{
        .block-container {{
            padding: var(--grid-4x) var(--grid-6x) !important;
        }}
        
        .protocol-grid {{
            grid-template-columns: repeat(5, 1fr);
        }}
        
        .metric-grid {{
            grid-template-columns: repeat(6, 1fr);
        }}
    }}
    
    /* Ultra-wide screens */
    @media (min-width: 1800px) {{
        .protocol-grid {{
            grid-template-columns: repeat(6, 1fr);
        }}
        
        .metric-grid {{
            grid-template-columns: repeat(8, 1fr);
        }}
    }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)