"""
Conversational AI Chat Interface Component
"""
import streamlit as st
import time
import pandas as pd
import re
from typing import List, Dict
from services.ai_service import AIService
from utils.session_manager import update_search_filter

def render_chat_interface():
    """Render the main chat interface for AI conversation"""
    
    st.markdown("---")
    st.markdown("### 💬 Ask Your Blockchain AI Advisor")
    
    # Initialize services
    ai_service = AIService()
    
    # Chat container
    chat_container = st.container()
    
    # Display chat history
    with chat_container:
        display_chat_history()
    
    # Chat input section
    render_chat_input(ai_service)
    
    # Suggested queries section
    render_suggested_queries()

def display_chat_history():
    """Display the conversation history"""
    
    if not st.session_state.chat_messages:
        # Welcome message
        st.markdown("""
        <div class="chat-message bot-message">
            <strong>🤖 AI Advisor:</strong> Hello! I'm your blockchain research specialist focusing on 
            <strong>Improvement Proposals</strong> and <strong>L1 Protocol Analysis</strong>.
            <br><br>
            I can help you with:
            <ul>
                <li><strong>Proposals:</strong> "Show me latest TIPs in draft", "EIPs in production"</li>
                <li><strong>L1 Performance:</strong> "Compare TPS across L1 protocols"</li>
                <li><strong>Protocol Analysis:</strong> "Ethereum vs Tron transaction costs"</li>
                <li><strong>Technical Research:</strong> "Bitcoin vs BSC consensus mechanisms"</li>
            </ul>
            What would you like to research today?
        </div>
        """, unsafe_allow_html=True)
    
    # Display conversation history
    for message in st.session_state.chat_messages:
        if message["role"] == "user":
            st.markdown("**👤 You:**")
            st.markdown(f"> {message['content']}")
            st.markdown("")  # Add spacing
        else:
            # Display AI response with proper table rendering
            st.markdown("**🤖 AI Advisor:**")
            render_ai_response_with_tables(message["content"])
            st.markdown("---")  # Add divider after AI response

def render_ai_response_with_tables(content: str):
    """Render AI response with proper table formatting"""
    
    # For better compatibility, use Streamlit's native markdown with table support
    # This handles emojis and formatting better than pandas DataFrames
    
    # Check if content has tables and use appropriate rendering
    if '|' in content and '---' in content:
        # Content has tables - render with Streamlit markdown
        st.markdown(content)
    else:
        # No tables - regular markdown
        st.markdown(content)

def render_fee_comparison_tables(content: str):
    """Render the fee comparison with dedicated table components"""
    
    # Display title
    st.markdown("💸 **LOWEST FEE L1 PROTOCOLS - COMPREHENSIVE ANALYSIS**")
    
    # Main comparison table
    st.markdown("🏆 **TRANSACTION FEE COMPARISON**")
    
    fee_data = [
        {"Rank": "🥇", "Protocol": "Tron (TRX)", "Avg Fee": "$0.001", "TPS": "2,000", "Finality": "3s", "Security": "78/100", "Type": "L1", "Best Use Case": "Microtransactions"},
        {"Rank": "🥈", "Protocol": "Base (ETH)", "Avg Fee": "$0.15", "TPS": "350", "Finality": "2s", "Security": "92/100", "Type": "L2", "Best Use Case": "Consumer Apps"},
        {"Rank": "🥉", "Protocol": "BSC (BNB)", "Avg Fee": "$0.30", "TPS": "2,100", "Finality": "3s", "Security": "82/100", "Type": "L1", "Best Use Case": "High Volume Apps"},
        {"Rank": "4️⃣", "Protocol": "Bitcoin (BTC)", "Avg Fee": "$8.50", "TPS": "7", "Finality": "1h", "Security": "100/100", "Type": "L1", "Best Use Case": "Store of Value"},
        {"Rank": "5️⃣", "Protocol": "Ethereum (ETH)", "Avg Fee": "$12.50", "TPS": "15", "Finality": "12.8m", "Security": "98/100", "Type": "L1", "Best Use Case": "Smart Contracts"}
    ]
    
    df_fees = pd.DataFrame(fee_data)
    st.dataframe(df_fees, use_container_width=True)
    
    # Optimization guide table
    st.markdown("💡 **FEE OPTIMIZATION GUIDE**")
    
    optimization_data = [
        {"Transaction Value": "<$10 (Micro)", "Recommended Protocol": "Tron", "Why Choose": "0.01% fee ratio, ultra-cheap"},
        {"Transaction Value": "$10-$1,000", "Recommended Protocol": "Base", "Why Choose": "Good security/cost balance"},
        {"Transaction Value": "$1,000-$10,000", "Recommended Protocol": "BSC", "Why Choose": "High performance, proven ecosystem"},
        {"Transaction Value": ">$10,000", "Recommended Protocol": "Ethereum", "Why Choose": "Maximum security justifies fee"},
        {"Transaction Value": "Store Value", "Recommended Protocol": "Bitcoin", "Why Choose": "Ultimate security, payment focus"}
    ]
    
    df_optimization = pd.DataFrame(optimization_data)
    st.dataframe(df_optimization, use_container_width=True)
    
    # Summary recommendations
    st.markdown("""
**🎯 QUICK RECOMMENDATIONS:**
• **For Maximum Savings**: Choose **Tron** (299x cheaper than Ethereum)
• **For Balance**: Choose **Base** (83x cheaper than Ethereum, good security)
• **For High Volume Apps**: Choose **BSC** (41x cheaper than Ethereum, proven)
• **For Large Holdings**: **Ethereum** or **Bitcoin** (security over cost)

Would you like a detailed breakdown for any specific protocol or use case?
    """)

def render_chat_input(ai_service: AIService):
    """Render chat input and handle user messages"""
    
    # Pre-fill with use case if selected
    placeholder_text = "Ask about blockchain protocols..."
    initial_query = ""
    
    if st.session_state.selected_use_case:
        use_case = st.session_state.selected_use_case
        if use_case == "eips":
            placeholder_text = "Fetching latest Ethereum Improvement Proposals..."
            initial_query = "Show me the latest EIPs with their status"
        elif use_case == "l1_performance":
            placeholder_text = "Comparing L1 protocol performance..."
            initial_query = "Compare the performance of major L1 protocols: Ethereum, Bitcoin, Tron, BSC, and Base"
        else:
            placeholder_text = f"Researching {use_case}..."
            initial_query = f"Tell me about {use_case}"
        
        # Reset the use case selection
        st.session_state.selected_use_case = None
    
    # Chat input with form for Enter key support
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_input(
                "Your question:",
                value=initial_query,
                placeholder=placeholder_text,
                label_visibility="collapsed",
                help="Type your question and press Enter or click Send"
            )
        
        with col2:
            send_button = st.form_submit_button("Send 🚀", type="primary", use_container_width=True)
    
    # Process user input when form is submitted (Enter key or Send button)
    if send_button:
        if user_input.strip():
            process_user_message(user_input, ai_service)
            st.rerun()
        else:
            st.warning("Please enter a question or message.")

def process_user_message(user_input: str, ai_service: AIService):
    """Process user message and generate AI response"""
    
    # Add user message to history
    st.session_state.chat_messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Show typing indicator
    with st.spinner("🤖 AI is thinking..."):
        try:
            # Get AI response
            ai_response = ai_service.get_chat_response(user_input, st.session_state.chat_messages)
            
            # Ensure we have a valid response
            if not ai_response or ai_response.strip() == "":
                ai_response = "I'm sorry, I couldn't generate a response. Please try rephrasing your question."
            
            # Response is now working correctly with proper table formatting
            
            # Disable blockchain service recommendations to use only AI responses with proper table formatting
            # search_params = ai_service.extract_search_parameters(user_input)
            # recommendations = None
            # if search_params:
            #     recommendations = blockchain_service.get_recommendations(search_params)
            #     if recommendations:
            #         formatted_recommendations = format_recommendations(recommendations)
            #         ai_response += f"\n\n{formatted_recommendations}"
            
            # Add AI response to history
            st.session_state.chat_messages.append({
                "role": "assistant", 
                "content": ai_response
            })
            
            # Recommendations disabled - using AI responses only
            # if recommendations:
            #     st.session_state.current_recommendations = recommendations
                
        except Exception as e:
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": f"I apologize, but I encountered an error: {str(e)}. Please try rephrasing your question."
            })

def format_recommendations(recommendations: List[Dict]) -> str:
    """Format blockchain recommendations for display with comprehensive details"""
    
    if not recommendations:
        return "I couldn't find any blockchain protocols matching your criteria. Try adjusting your requirements."
    
    formatted = "\n**📋 BLOCKCHAIN RECOMMENDATIONS - DETAILED ANALYSIS**\n\n"
    
    for i, rec in enumerate(recommendations[:3], 1):
        rank_emoji = ["🏆", "🥈", "🥉"][i-1] if i <= 3 else f"{i}."
        
        formatted += f"{rank_emoji} **{rec['name']}** (Match Score: {rec['score']}/100)\n"
        
        # Core Performance Metrics
        formatted += f"   📊 **PERFORMANCE METRICS:**\n"
        formatted += f"      • Throughput: {rec.get('tps', 'N/A'):,} TPS\n"
        formatted += f"      • Finality: {format_finality_time(rec.get('finality_time', 'N/A'))}\n"
        formatted += f"      • Average Fee: ${rec.get('avg_fee', 0):.4f}\n"
        formatted += f"      • Consensus: {rec.get('consensus', 'N/A')}\n\n"
        
        # Economic & Market Data
        if rec.get('market_cap') or rec.get('tvl'):
            formatted += f"   💰 **MARKET POSITION:**\n"
            if rec.get('market_cap'):
                formatted += f"      • Market Cap: ${rec['market_cap']:,}\n"
            if rec.get('tvl'):
                formatted += f"      • Total Value Locked: ${rec['tvl']:,}\n"
            formatted += f"      • Type: {rec.get('type', 'N/A')}\n\n"
        
        # Ecosystem & Development
        formatted += f"   🌟 **ECOSYSTEM HEALTH:**\n"
        formatted += f"      • Security Score: {rec.get('security_score', 'N/A')}/100\n"
        formatted += f"      • Ecosystem Score: {rec.get('ecosystem_score', 'N/A')}/100\n"
        if rec.get('active_developers'):
            formatted += f"      • Active Developers: {rec['active_developers']:,}\n"
        if rec.get('dapp_count'):
            formatted += f"      • dApp Count: {rec['dapp_count']:,}\n"
        formatted += "\n"
        
        # Use Cases & Suitability
        if rec.get('suitable_for'):
            formatted += f"   🎯 **OPTIMAL USE CASES:** {', '.join(rec['suitable_for']).title()}\n\n"
        
        # Reasoning & Recommendation
        formatted += f"   ✅ **WHY RECOMMENDED:** {rec.get('reasoning', 'Good match for your requirements')}\n"
        
        # Website link if available
        if rec.get('website'):
            formatted += f"   🔗 **Learn More:** {rec['website']}\n"
        
        formatted += f"\n{'─' * 60}\n\n"
    
    # Summary and next steps
    formatted += "**🔍 DETAILED COMPARISON:**\n"
    formatted += "| Protocol | TPS | Fee | Finality | Security |\n"
    formatted += "|----------|-----|-----|----------|----------|\n"
    
    for rec in recommendations[:3]:
        formatted += f"| {rec['name']} | {rec.get('tps', 'N/A'):,} | ${rec.get('avg_fee', 0):.4f} | {format_finality_time(rec.get('finality_time', 'N/A'))} | {rec.get('security_score', 'N/A')}/100 |\n"
    
    formatted += "\n**💡 NEXT STEPS:**\n"
    formatted += "• Want detailed technical specifications for any protocol?\n"
    formatted += "• Need implementation guidance or integration support?\n" 
    formatted += "• Interested in risk analysis or security audit results?\n"
    formatted += "• Would you like me to compare with other specific protocols?\n\n"
    formatted += "**Just ask!** I can provide deeper analysis on any aspect that interests you."
    
    return formatted

def format_finality_time(finality_value) -> str:
    """Format finality time for better readability"""
    if isinstance(finality_value, (int, float)):
        if finality_value < 1:
            return f"{finality_value*1000:.0f}ms"
        elif finality_value < 60:
            return f"{finality_value:.1f}s"
        else:
            minutes = finality_value // 60
            seconds = finality_value % 60
            if seconds > 0:
                return f"{int(minutes)}m {int(seconds)}s"
            else:
                return f"{int(minutes)}m"
    else:
        return str(finality_value)

def render_suggested_queries():
    """Render suggested query buttons"""
    
    st.markdown("### 💡 Suggested Questions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎮 Best L1 for Gaming", use_container_width=True, key="gaming_query"):
            query = "Which L1 protocol is best for gaming: Ethereum, Base, Tron, BSC, or Bitcoin?"
            st.session_state.chat_input_counter = getattr(st.session_state, 'chat_input_counter', 0) + 1
            process_user_message(query, AIService())
            st.rerun()
        
        if st.button("🏢 Enterprise L1 Comparison", use_container_width=True, key="enterprise_query"):
            query = "Compare Ethereum, Bitcoin, Base, BSC, and Tron for enterprise use"
            st.session_state.chat_input_counter = getattr(st.session_state, 'chat_input_counter', 0) + 1
            process_user_message(query, AIService())
            st.rerun()
    
    with col2:
        if st.button("💰 Lowest L1 Fees", use_container_width=True, key="fees_query"):
            query = "Find the lowest fee L1 protocol among Ethereum, Base, Tron, BSC, Bitcoin"
            st.session_state.chat_input_counter = getattr(st.session_state, 'chat_input_counter', 0) + 1
            process_user_message(query, AIService())
            st.rerun()
        
        if st.button("💰 L1 Payment Solutions", use_container_width=True, key="payment_query"):
            query = "Which L1 is best for payments: Tron, Base, BSC, Ethereum, or Bitcoin?"
            st.session_state.chat_input_counter = getattr(st.session_state, 'chat_input_counter', 0) + 1
            process_user_message(query, AIService())
            st.rerun()
    
    # Clear chat button
    st.markdown("---")
    if st.button("🗑️ Clear Conversation", type="secondary"):
        st.session_state.chat_messages = []
        st.session_state.current_recommendations = []
        st.rerun()