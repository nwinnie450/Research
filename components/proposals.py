"""
Real-Time Blockchain Proposals Component
Live improvement proposals with GitHub API integration
"""
import streamlit as st
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime

# Try to import real-time service, fallback to original if not available
try:
    from services.realtime_proposals_service import realtime_proposals
    REALTIME_AVAILABLE = True
except ImportError:
    realtime_proposals = None
    REALTIME_AVAILABLE = False

# Always import LatestProposalsFetcher for fallback functionality
try:
    from services.latest_proposals_fetcher import LatestProposalsFetcher
except ImportError:
    LatestProposalsFetcher = None

from services.blockchain_research_advisor import BlockchainResearchAdvisor

def render_proposals_interface():
    """Render real-time proposals interface with live GitHub data"""
    
    # Header with real-time indicator
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if REALTIME_AVAILABLE:
            st.markdown("### 📋 Live Blockchain Proposals")
            st.markdown("Real-time improvement proposals from GitHub repositories")
        else:
            st.markdown("### 📋 Blockchain Improvement Proposals")
            st.markdown("Explore improvement proposals (Demo Mode)")
    
    with col2:
        if REALTIME_AVAILABLE:
            if st.button("🔄 Refresh", help="Refresh live proposal data"):
                realtime_proposals.cache.clear()
                st.rerun()
            
            # Rate limit status and API key verification
            rate_info = realtime_proposals.check_rate_limit()
            remaining = rate_info.get('rate', {}).get('remaining', 0)
            limit = rate_info.get('rate', {}).get('limit', 0)
            
            # Show API status
            if limit >= 5000:
                st.success(f"🔑 API Key Active: {remaining}/{limit}")
            else:
                st.warning(f"⚠️ No API Key: {remaining}/{limit}")
            
        else:
            st.info("Demo Mode")
    
    # Initialize services
    if not REALTIME_AVAILABLE and LatestProposalsFetcher:
        proposals_fetcher = LatestProposalsFetcher()
    else:
        proposals_fetcher = None
    
    research_advisor = BlockchainResearchAdvisor()
    
    # Proposal type and status filter section
    with st.expander("⚙️ Filter Options", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Proposal Types")
            if REALTIME_AVAILABLE:
                available_types = ['EIP', 'BIP', 'TIP', 'BEP']
                default_types = ['EIP']
            else:
                available_types = ['EIP', 'BIP', 'SUP', 'TIP', 'BEP', 'LIP']
                default_types = ['TIP']
            
            proposal_types = st.multiselect(
                "Select proposal types:",
                options=available_types,
                default=default_types,
                help="Choose which types of blockchain improvement proposals to display"
            )
        
        with col2:
            st.markdown("#### Status Filter")
            status_options = {
                'All Statuses': None,
                'Production/Final': 'production',
                'Draft': 'draft',
                'Proposed': 'proposed',
                'Candidate': 'candidate', 
                'Under Review': 'review',
                'Withdrawn': 'withdrawn',
                'Superseded': 'superseded',
                'Living': 'living',
                'Stagnant': 'stagnant',
                'Open': 'open'
            }
            
            selected_status = st.selectbox(
                "Filter by status:",
                options=list(status_options.keys()),
                index=0,
                help="Filter proposals by their current status"
            )
            
            status_filter = status_options[selected_status]
    
    # Additional filters for TIPs
    if 'TIP' in proposal_types:
        with st.expander("🎯 TIPs-Specific Filters", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                show_recent_only = st.checkbox(
                    "Show recent TIPs only (last 30 days)", 
                    value=False,
                    help="Filter to show only TIPs from the last 30 days"
                )
            
            with col2:
                limit_results = st.number_input(
                    "Maximum results per type:",
                    min_value=5,
                    max_value=50,
                    value=10,
                    step=5,
                    help="Limit the number of proposals shown for each type"
                )
    else:
        show_recent_only = False
        limit_results = 10
    
    # Fetch and display button
    if st.button("🔍 Fetch Proposals", type="primary", use_container_width=True):
        if not proposal_types:
            st.warning("Please select at least one proposal type.")
        else:
            with st.spinner(f"Fetching {', '.join(proposal_types)} proposals{' with ' + selected_status.lower() + ' status' if status_filter else ''}..."):
                try:
                    if REALTIME_AVAILABLE:
                        # Use real-time GitHub API
                        all_proposals = []
                        
                        # Map proposal types to protocols
                        protocol_map = {
                            'EIP': 'ethereum',
                            'BIP': 'bitcoin', 
                            'TIP': 'tron',
                            'BEP': 'binance_smart_chain'
                        }
                        
                        for proposal_type in proposal_types:
                            if proposal_type in protocol_map:
                                protocol = protocol_map[proposal_type]
                                proposals = realtime_proposals.get_latest_proposals(
                                    protocol, 
                                    limit=limit_results,
                                    status_filter=status_filter
                                )
                                
                                # Add type information
                                for proposal in proposals:
                                    proposal['type'] = proposal_type
                                    proposal['protocol'] = protocol
                                
                                all_proposals.extend(proposals)
                        
                        # Store results in the format expected by display functions
                        # Group proposals by type for display
                        standards_data = []
                        type_groups = {}
                        
                        # Group proposals by type
                        for proposal in all_proposals:
                            ptype = proposal.get('type', 'Unknown')
                            if ptype not in type_groups:
                                type_groups[ptype] = []
                            type_groups[ptype].append(proposal)
                        
                        # Convert to expected format
                        for ptype, proposals in type_groups.items():
                            standards_data.append({
                                'standard': ptype,
                                'source': f"GitHub API - {protocol_map.get(ptype, 'Unknown')} repository",
                                'items': proposals
                            })
                        
                        st.session_state.proposals_result = {
                            'success': True,
                            'standards': standards_data,
                            'total_count': len(all_proposals),
                            'fetched_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                    else:
                        # Use original fetcher
                        if proposals_fetcher:
                            result = proposals_fetcher.fetch_latest_proposals(
                                standards=proposal_types, 
                                status_filter=status_filter
                            )
                            st.session_state.proposals_result = result
                        else:
                            st.error("Proposals service not available. Please check your installation.")
                    
                    # Store filter info
                    st.session_state.proposals_filter = {
                        'types': proposal_types,
                        'status': status_filter,
                        'selected_status_text': selected_status,
                        'recent_only': show_recent_only,
                        'limit': limit_results
                    }
                    
                    st.success(f"✅ Successfully fetched proposals!")
                    
                except Exception as e:
                    st.error(f"❌ Error fetching proposals: {str(e)}")
    
    # Search functionality
    if REALTIME_AVAILABLE:
        st.markdown("---")
        st.markdown("#### 🔍 Search Proposals")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query = st.text_input(
                "Search proposals by title or content:",
                placeholder="e.g., 'transaction fees', 'smart contracts', 'consensus'",
                help="Search across all proposal types and protocols"
            )
        
        with col2:
            if st.button("🔍 Search", disabled=not search_query):
                with st.spinner("Searching proposals..."):
                    search_results = realtime_proposals.search_proposals(search_query)
                    st.session_state.search_results = search_results
                    st.success(f"Found {len(search_results)} matching proposals")
    
    # Display search results
    if REALTIME_AVAILABLE and hasattr(st.session_state, 'search_results'):
        st.markdown("#### 🎯 Search Results")
        display_proposals_table(st.session_state.search_results, is_search=True)
        
        # Add comparison feature for search results
        if len(st.session_state.search_results) >= 2:
            render_proposal_comparison(st.session_state.search_results)
        
        st.markdown("---")
    
    # Display fetched results
    if hasattr(st.session_state, 'proposals_result') and st.session_state.proposals_result:
        render_proposals_results(st.session_state.proposals_result, st.session_state.proposals_filter)
        
        # Add analytics for fetched proposals
        if REALTIME_AVAILABLE:
            render_proposal_analytics(st.session_state.proposals_result)
    
    # Quick action buttons
    st.markdown("---")
    st.markdown("### 🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Latest TIPs", use_container_width=True):
            quick_fetch_and_display(['TIP'], None, "Latest TIPs", proposals_fetcher)
    
    with col2:
        if st.button("🔥 Active TIPs", use_container_width=True):
            quick_fetch_and_display(['TIP'], 'production', "Active TIPs", proposals_fetcher)
    
    with col3:
        if st.button("📝 Draft TIPs", use_container_width=True):
            quick_fetch_and_display(['TIP'], 'draft', "Draft TIPs", proposals_fetcher)

def render_proposals_results(result: Dict, filter_config: Dict):
    """Render the fetched proposals results"""
    
    st.markdown("---")
    st.markdown("### 📊 Results")
    
    # Show filter summary
    filter_summary = f"**Showing:** {', '.join(filter_config['types'])}"
    if filter_config['status']:
        filter_summary += f" | **Status:** {filter_config['selected_status_text']}"
    
    st.markdown(filter_summary)
    st.markdown(f"**Fetched at:** {result.get('fetched_at', 'Unknown')}")
    
    standards_data = result.get('standards', [])
    
    if not standards_data:
        st.warning("No proposals found matching the selected criteria.")
        return
    
    # Create tabs for different proposal types
    if len(standards_data) > 1:
        tab_names = [f"{std.get('standard', 'Unknown')} ({len(std.get('items', []))})" for std in standards_data]
        tabs = st.tabs(tab_names)
        
        for i, (tab, standard_data) in enumerate(zip(tabs, standards_data)):
            with tab:
                render_standard_proposals(standard_data, filter_config)
    else:
        # Single proposal type - no tabs needed
        render_standard_proposals(standards_data[0], filter_config)

def render_standard_proposals(standard_data: Dict, filter_config: Dict):
    """Render proposals for a specific standard (e.g., TIP, EIP)"""
    
    standard = standard_data.get('standard', 'Unknown')
    source = standard_data.get('source', '')
    items = standard_data.get('items', [])
    
    if not items:
        st.info(f"No {standard} proposals found with the current filters.")
        return
    
    # Apply limit if specified
    limit = filter_config.get('limit', 10)
    if len(items) > limit:
        items = items[:limit]
        st.info(f"Showing first {limit} of {len(standard_data.get('items', []))} {standard} proposals")
    
    st.markdown(f"**Source:** [{standard_data.get('source', 'Unknown')}]({source})")
    st.markdown(f"**Found:** {len(items)} proposals")
    
    # Create a table for better display
    table_data = []
    for item in items:
        table_data.append({
            'Number': f"{standard}-{item.get('number', 'N/A')}",
            'Title': item.get('title', 'No title available')[:80] + ('...' if len(item.get('title', '')) > 80 else ''),
            'Status': item.get('status', 'Unknown'),
            'Type': item.get('type', '-'),
            'Category': item.get('category', '-')
        })
    
    if table_data:
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, height=400)
        
        # Show detailed view option
        if st.checkbox(f"Show detailed {standard} information", key=f"details_{standard}"):
            render_detailed_proposals(items, standard)
    
    # Export option
    if st.button(f"📥 Export {standard} Data", key=f"export_{standard}", use_container_width=True):
        export_proposals_data(items, standard)

def render_detailed_proposals(items: List[Dict], standard: str):
    """Render detailed view of proposals with timeline and status tracking"""
    
    st.markdown(f"#### Detailed {standard} Information")
    
    for i, item in enumerate(items[:5]):  # Show first 5 in detail
        with st.expander(f"{standard}-{item.get('number', 'N/A')}: {item.get('title', 'No title')}", expanded=False):
            # Status timeline visualization
            render_proposal_timeline(item)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Basic Information:**")
                st.markdown(f"- **Number:** {item.get('number', 'N/A')}")
                
                # Enhanced status display with color coding
                status = item.get('status', 'Unknown')
                status_color = get_status_color(status)
                st.markdown(f"- **Status:** :{status_color}[{status}]")
                
                st.markdown(f"- **Type:** {item.get('type', 'Not specified')}")
                st.markdown(f"- **Category:** {item.get('category', 'Not specified')}")
                
                # Timeline information
                if item.get('created'):
                    st.markdown(f"- **Created:** {item.get('created')}")
                if item.get('last_modified'):
                    st.markdown(f"- **Last Modified:** {item.get('last_modified')}")
            
            with col2:
                st.markdown("**Links & Author:**")
                if item.get('link') or item.get('file_url'):
                    link_url = item.get('file_url') or item.get('link')
                    st.markdown(f"[📖 View Proposal]({link_url})")
                if item.get('discussions_link'):
                    st.markdown(f"[💬 Discussions]({item['discussions_link']})")
                if item.get('author'):
                    st.markdown(f"- **Author:** {item['author']}")
                
                # Status progression tracking
                render_status_progression(item, standard)
            
            if item.get('summary'):
                st.markdown("**Summary:**")
                st.markdown(item['summary'])

def render_proposal_timeline(proposal: Dict):
    """Render a visual timeline for proposal status"""
    status = proposal.get('status', '').lower()
    
    # Define status progression for different proposal types
    status_stages = {
        'draft': 1,
        'review': 2, 
        'last call': 3,
        'final': 4,
        'living': 4,
        'active': 4,
        'production': 4,
        'stagnant': 0,
        'withdrawn': 0,
        'rejected': 0
    }
    
    current_stage = status_stages.get(status, 1)
    
    # Timeline visualization
    stages = ['Draft', 'Review', 'Last Call', 'Final/Active']
    cols = st.columns(len(stages))
    
    for i, (col, stage) in enumerate(zip(cols, stages)):
        with col:
            if i + 1 <= current_stage:
                if status in ['stagnant', 'withdrawn', 'rejected']:
                    st.markdown(f"🔴 {stage}")
                else:
                    st.markdown(f"✅ {stage}")
            elif i + 1 == current_stage + 1:
                st.markdown(f"🟡 {stage}")
            else:
                st.markdown(f"⚪ {stage}")

def render_status_progression(proposal: Dict, standard: str):
    """Render status progression information"""
    status = proposal.get('status', 'Unknown')
    
    st.markdown("**Status Information:**")
    
    # Status-specific information
    if status.lower() == 'draft':
        st.info("📝 This proposal is in early draft stage")
    elif status.lower() in ['review', 'proposed']:
        st.info("🔍 This proposal is under review")
    elif status.lower() in ['final', 'active', 'production']:
        st.success("✅ This proposal is finalized")
    elif status.lower() == 'living':
        st.info("🔄 This is a living document that can be updated")
    elif status.lower() in ['stagnant', 'withdrawn', 'rejected']:
        st.warning("⚠️ This proposal is no longer active")
    
    # Show next steps based on status
    next_steps = get_next_steps(status, standard)
    if next_steps:
        st.markdown(f"**Next Steps:** {next_steps}")

def get_status_color(status: str) -> str:
    """Get color for status display"""
    status_lower = status.lower()
    
    color_map = {
        'draft': 'blue',
        'review': 'orange', 
        'proposed': 'orange',
        'last call': 'violet',
        'final': 'green',
        'active': 'green',
        'production': 'green',
        'living': 'green',
        'stagnant': 'gray',
        'withdrawn': 'red',
        'rejected': 'red'
    }
    
    return color_map.get(status_lower, 'gray')

def get_next_steps(status: str, standard: str) -> str:
    """Get next steps based on current status"""
    status_lower = status.lower()
    
    next_steps_map = {
        'draft': 'Awaiting community feedback and peer review',
        'review': 'Under evaluation by core developers',
        'proposed': 'Gathering community consensus',
        'last call': 'Final review period before decision',
        'final': 'Implementation in progress',
        'active': 'Currently implemented and active',
        'living': 'Document maintained and updated as needed',
        'stagnant': 'No recent activity - may need revival',
        'withdrawn': 'No longer being pursued',
        'rejected': 'Not accepted for implementation'
    }
    
    return next_steps_map.get(status_lower, '')

def render_proposal_comparison(proposals: List[Dict]):
    """Render proposal comparison interface"""
    
    with st.expander("🔄 Compare Proposals", expanded=False):
        st.markdown("#### Select Proposals to Compare")
        
        # Let users select proposals for comparison
        proposal_options = {}
        for proposal in proposals[:10]:  # Limit to first 10 for UI
            key = f"{proposal.get('type', 'Unknown')}-{proposal.get('number', 'N/A')}"
            title = proposal.get('title', 'No title')[:50] + ('...' if len(proposal.get('title', '')) > 50 else '')
            proposal_options[f"{key}: {title}"] = proposal
        
        col1, col2 = st.columns(2)
        
        with col1:
            proposal_1_key = st.selectbox(
                "Select First Proposal:",
                options=list(proposal_options.keys()),
                key="compare_proposal_1"
            )
        
        with col2:
            proposal_2_key = st.selectbox(
                "Select Second Proposal:",
                options=list(proposal_options.keys()),
                key="compare_proposal_2"
            )
        
        if proposal_1_key and proposal_2_key and proposal_1_key != proposal_2_key:
            proposal_1 = proposal_options[proposal_1_key]
            proposal_2 = proposal_options[proposal_2_key]
            
            st.markdown("#### 📊 Proposal Comparison")
            
            # Side-by-side comparison
            col1, col2 = st.columns(2)
            
            with col1:
                render_comparison_card(proposal_1, "First Proposal")
            
            with col2:
                render_comparison_card(proposal_2, "Second Proposal")
            
            # Comparison insights
            st.markdown("#### 🔍 Comparison Insights")
            render_comparison_insights(proposal_1, proposal_2)
        elif proposal_1_key == proposal_2_key:
            st.warning("Please select two different proposals for comparison.")

def render_comparison_card(proposal: Dict, title: str):
    """Render a comparison card for a proposal"""
    
    st.markdown(f"##### {title}")
    
    with st.container():
        # Header info
        ptype = proposal.get('type', 'Unknown')
        number = proposal.get('number', 'N/A')
        status = proposal.get('status', 'Unknown')
        status_color = get_status_color(status)
        
        st.markdown(f"**{ptype}-{number}**")
        st.markdown(f"Status: :{status_color}[{status}]")
        
        # Title and summary
        title = proposal.get('title', 'No title available')
        st.markdown(f"**Title:** {title}")
        
        # Key details
        st.markdown("**Key Details:**")
        if proposal.get('author'):
            st.markdown(f"• Author: {proposal.get('author')}")
        if proposal.get('created'):
            st.markdown(f"• Created: {proposal.get('created')}")
        if proposal.get('category'):
            st.markdown(f"• Category: {proposal.get('category')}")
        
        # Summary
        if proposal.get('summary'):
            st.markdown(f"**Summary:** {proposal.get('summary')[:200]}...")
        
        # Action buttons
        if proposal.get('file_url') or proposal.get('link'):
            link_url = proposal.get('file_url') or proposal.get('link')
            st.markdown(f"[📖 View Full Proposal]({link_url})")

def render_comparison_insights(proposal_1: Dict, proposal_2: Dict):
    """Render insights comparing two proposals"""
    
    insights = []
    
    # Status comparison
    status_1 = proposal_1.get('status', 'Unknown').lower()
    status_2 = proposal_2.get('status', 'Unknown').lower()
    
    if status_1 != status_2:
        status_comparison = compare_status_maturity(status_1, status_2)
        insights.append(f"📊 **Status Maturity:** {status_comparison}")
    
    # Type comparison
    type_1 = proposal_1.get('type', 'Unknown')
    type_2 = proposal_2.get('type', 'Unknown')
    
    if type_1 != type_2:
        insights.append(f"🔗 **Different Networks:** Comparing {type_1} (blockchain protocol) vs {type_2} (blockchain protocol)")
    else:
        insights.append(f"🔗 **Same Network:** Both proposals are for the {type_1} ecosystem")
    
    # Author comparison
    author_1 = proposal_1.get('author', 'Unknown')
    author_2 = proposal_2.get('author', 'Unknown')
    
    if author_1 == author_2 and author_1 != 'Unknown':
        insights.append(f"👤 **Same Author:** Both proposals by {author_1}")
    
    # Category comparison
    cat_1 = proposal_1.get('category', '').lower()
    cat_2 = proposal_2.get('category', '').lower()
    
    if cat_1 and cat_2 and cat_1 != cat_2:
        insights.append(f"📂 **Different Categories:** {cat_1.title()} vs {cat_2.title()}")
    
    # Timeline comparison
    try:
        created_1 = proposal_1.get('created', '')
        created_2 = proposal_2.get('created', '')
        
        if created_1 and created_2:
            if created_1 < created_2:
                insights.append(f"⏰ **Timeline:** First proposal is older (created {created_1})")
            elif created_1 > created_2:
                insights.append(f"⏰ **Timeline:** Second proposal is older (created {created_2})")
    except:
        pass
    
    # Display insights
    if insights:
        for insight in insights:
            st.markdown(insight)
    else:
        st.info("These proposals have similar characteristics.")
    
    # Recommendation
    st.markdown("#### 💡 Recommendation")
    recommendation = generate_comparison_recommendation(proposal_1, proposal_2)
    st.info(recommendation)

def compare_status_maturity(status_1: str, status_2: str) -> str:
    """Compare the maturity of two proposal statuses"""
    
    maturity_order = {
        'draft': 1,
        'review': 2,
        'proposed': 2,
        'last call': 3,
        'final': 4,
        'active': 4,
        'production': 4,
        'living': 4,
        'stagnant': 0,
        'withdrawn': 0,
        'rejected': 0
    }
    
    score_1 = maturity_order.get(status_1, 1)
    score_2 = maturity_order.get(status_2, 1)
    
    if score_1 > score_2:
        return f"First proposal ({status_1.title()}) is more mature than second ({status_2.title()})"
    elif score_2 > score_1:
        return f"Second proposal ({status_2.title()}) is more mature than first ({status_1.title()})"
    else:
        return f"Both proposals are at similar maturity levels ({status_1.title()})"

def generate_comparison_recommendation(proposal_1: Dict, proposal_2: Dict) -> str:
    """Generate a recommendation based on proposal comparison"""
    
    status_1 = proposal_1.get('status', 'unknown').lower()
    status_2 = proposal_2.get('status', 'unknown').lower()
    
    # Status-based recommendations
    if status_1 in ['final', 'active', 'production'] and status_2 not in ['final', 'active', 'production']:
        return "Consider the first proposal as it's already finalized and likely implemented."
    elif status_2 in ['final', 'active', 'production'] and status_1 not in ['final', 'active', 'production']:
        return "Consider the second proposal as it's already finalized and likely implemented."
    elif status_1 in ['stagnant', 'withdrawn', 'rejected']:
        return "The second proposal may be more relevant as the first is no longer active."
    elif status_2 in ['stagnant', 'withdrawn', 'rejected']:
        return "The first proposal may be more relevant as the second is no longer active."
    elif status_1 == 'draft' and status_2 in ['review', 'proposed']:
        return "The second proposal is further along in the review process."
    elif status_2 == 'draft' and status_1 in ['review', 'proposed']:
        return "The first proposal is further along in the review process."
    else:
        return "Both proposals appear to be at similar stages. Consider reviewing both for comprehensive understanding."

def export_proposals_data(items: List[Dict], standard: str):
    """Export proposals data as downloadable file"""
    
    if not items:
        st.warning("No data to export.")
        return
    
    try:
        df = pd.DataFrame(items)
        csv_data = df.to_csv(index=False)
        
        st.download_button(
            label=f"📥 Download {standard} data as CSV",
            data=csv_data,
            file_name=f"{standard}_proposals_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            key=f"download_{standard}"
        )
        
        st.success(f"✅ {standard} data prepared for download!")
        
    except Exception as e:
        st.error(f"❌ Error preparing export: {str(e)}")

def quick_fetch_and_display(proposal_types: List[str], status_filter: Optional[str], 
                          title: str, proposals_fetcher=None):
    """Quick fetch and display for action buttons"""
    
    with st.spinner(f"Fetching {title.lower()}..."):
        try:
            if REALTIME_AVAILABLE:
                # Use real-time service for quick actions
                all_proposals = []
                protocol_map = {
                    'TIP': 'tron',
                    'EIP': 'ethereum',
                    'BIP': 'bitcoin', 
                    'BEP': 'binance_smart_chain'
                }
                
                for proposal_type in proposal_types:
                    if proposal_type in protocol_map:
                        protocol = protocol_map[proposal_type]
                        proposals = realtime_proposals.get_latest_proposals(
                            protocol, 
                            limit=10,
                            status_filter=status_filter
                        )
                        
                        for proposal in proposals:
                            proposal['type'] = proposal_type
                            proposal['protocol'] = protocol
                        
                        all_proposals.extend(proposals)
                
                result = {
                    'success': True,
                    'data': all_proposals,
                    'total_count': len(all_proposals)
                }
            elif proposals_fetcher:
                result = proposals_fetcher.fetch_latest_proposals(
                    standards=proposal_types, 
                    status_filter=status_filter
                )
            else:
                st.error("No proposals service available")
                return
            
            # Store in session state
            st.session_state.proposals_result = result
            st.session_state.proposals_filter = {
                'types': proposal_types,
                'status': status_filter,
                'selected_status_text': title,
                'recent_only': False,
                'limit': 10
            }
            
            st.success(f"✅ {title} fetched!")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Helper function to get available statuses for each proposal type
def get_available_statuses_by_type():
    """Return available statuses for different proposal types"""
    
    return {
        'TIP': ['draft', 'proposed', 'open', 'closed', 'withdrawn'],
        'EIP': ['draft', 'review', 'last call', 'final', 'stagnant', 'withdrawn', 'living'],
        'BIP': ['draft', 'proposed', 'final', 'rejected', 'withdrawn'],
        'SUP': ['draft', 'proposed', 'open', 'closed'],
        'BEP': ['draft', 'proposed', 'final', 'deferred', 'rejected'],
        'LIP': ['draft', 'proposed', 'final', 'withdrawn']
    }

def display_proposals_table(proposals: List[Dict], is_search: bool = False):
    """Display proposals in a formatted table"""
    
    if not proposals:
        st.info("No proposals found matching your criteria.")
        return
    
    # Convert to DataFrame for better display
    df_data = []
    for proposal in proposals:
        df_data.append({
            'Type': proposal.get('type', 'Unknown'),
            'Number': proposal.get('number', 'N/A'),
            'Title': proposal.get('title', 'No title')[:50] + '...' if len(proposal.get('title', '')) > 50 else proposal.get('title', 'No title'),
            'Status': proposal.get('status', 'Unknown'),
            'Author': proposal.get('author', 'Unknown')[:20] + '...' if len(proposal.get('author', '')) > 20 else proposal.get('author', 'Unknown'),
            'Created': proposal.get('created', 'Unknown'),
            'Link': proposal.get('file_url', '#')
        })
    
    df = pd.DataFrame(df_data)
    
    # Display with clickable links
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Type": st.column_config.TextColumn("Type", width="small"),
            "Number": st.column_config.TextColumn("Number", width="small"),
            "Title": st.column_config.TextColumn("Title", width="medium"),
            "Status": st.column_config.TextColumn("Status", width="small"),
            "Author": st.column_config.TextColumn("Author", width="small"),
            "Created": st.column_config.TextColumn("Date", width="small"),
            "Link": st.column_config.LinkColumn("Link", width="small")
        }
    )
    
    # Proposal statistics
    if len(proposals) > 1:
        st.markdown("#### 📊 Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Proposals", len(proposals))
        
        with col2:
            status_counts = {}
            for proposal in proposals:
                status = proposal.get('status', 'Unknown')
                status_counts[status] = status_counts.get(status, 0) + 1
            most_common_status = max(status_counts.items(), key=lambda x: x[1]) if status_counts else ('None', 0)
            st.metric("Most Common Status", f"{most_common_status[0]} ({most_common_status[1]})")
        
        with col3:
            if REALTIME_AVAILABLE:
                type_counts = {}
                for proposal in proposals:
                    ptype = proposal.get('type', 'Unknown')
                    type_counts[ptype] = type_counts.get(ptype, 0) + 1
                most_common_type = max(type_counts.items(), key=lambda x: x[1]) if type_counts else ('None', 0)
                st.metric("Most Common Type", f"{most_common_type[0]} ({most_common_type[1]})")

def render_proposal_analytics(result: Dict):
    """Render comprehensive analytics for proposals"""
    
    with st.expander("📊 Proposal Analytics & Trends", expanded=False):
        st.markdown("### 📈 Proposal Analytics Dashboard")
        
        # Extract all proposals from standards
        all_proposals = []
        standards = result.get('standards', [])
        
        for standard in standards:
            items = standard.get('items', [])
            for item in items:
                item['standard_type'] = standard.get('standard', 'Unknown')
                all_proposals.append(item)
        
        if not all_proposals:
            st.info("No proposals available for analytics")
            return
        
        # Overview metrics
        render_analytics_overview(all_proposals)
        
        # Status distribution
        render_status_analytics(all_proposals)
        
        # Author analytics
        render_author_analytics(all_proposals)
        
        # Timeline analytics
        render_timeline_analytics(all_proposals)
        
        # Network comparison
        render_network_analytics(all_proposals)

def render_analytics_overview(proposals: List[Dict]):
    """Render overview analytics metrics"""
    
    st.markdown("#### 🔍 Overview Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Proposals", len(proposals))
    
    with col2:
        # Active proposals (final, active, production, living)
        active_count = sum(1 for p in proposals if p.get('status', '').lower() in ['final', 'active', 'production', 'living'])
        st.metric("Active Proposals", active_count)
    
    with col3:
        # Draft proposals
        draft_count = sum(1 for p in proposals if p.get('status', '').lower() == 'draft')
        st.metric("Draft Proposals", draft_count)
    
    with col4:
        # Unique authors
        authors = set(p.get('author', 'Unknown') for p in proposals if p.get('author') and p.get('author') != 'Unknown')
        st.metric("Unique Authors", len(authors))

def render_status_analytics(proposals: List[Dict]):
    """Render status distribution analytics"""
    
    st.markdown("#### 📊 Status Distribution")
    
    # Count proposals by status
    status_counts = {}
    for proposal in proposals:
        status = proposal.get('status', 'Unknown')
        status_counts[status] = status_counts.get(status, 0) + 1
    
    if status_counts:
        # Create a simple bar chart representation
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Display status counts
            for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / len(proposals)) * 100
                st.write(f"**{status}:** {count} ({percentage:.1f}%)")
        
        with col2:
            # Status health score
            health_score = calculate_status_health(status_counts, len(proposals))
            st.metric("Health Score", f"{health_score:.1f}/10")
            
            if health_score >= 8:
                st.success("Excellent proposal ecosystem health")
            elif health_score >= 6:
                st.info("Good proposal ecosystem health")
            elif health_score >= 4:
                st.warning("Moderate proposal ecosystem health")
            else:
                st.error("Needs improvement in proposal ecosystem")

def render_author_analytics(proposals: List[Dict]):
    """Render author contribution analytics"""
    
    st.markdown("#### 👥 Author Contributions")
    
    # Count proposals by author
    author_counts = {}
    for proposal in proposals:
        author = proposal.get('author', 'Unknown')
        if author and author != 'Unknown':
            author_counts[author] = author_counts.get(author, 0) + 1
    
    if author_counts:
        # Top contributors
        top_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Top Contributors:**")
            for i, (author, count) in enumerate(top_authors, 1):
                st.write(f"{i}. **{author}**: {count} proposals")
        
        with col2:
            # Contribution diversity
            single_contrib = sum(1 for count in author_counts.values() if count == 1)
            multi_contrib = len(author_counts) - single_contrib
            
            st.write(f"**Single Contributors:** {single_contrib}")
            st.write(f"**Multi Contributors:** {multi_contrib}")
            
            diversity_score = (single_contrib / len(author_counts)) * 100 if author_counts else 0
            st.write(f"**Diversity Score:** {diversity_score:.1f}%")

def render_timeline_analytics(proposals: List[Dict]):
    """Render timeline and trend analytics"""
    
    st.markdown("#### ⏰ Timeline Trends")
    
    # Extract years from creation dates
    years = {}
    recent_proposals = 0
    
    for proposal in proposals:
        created = proposal.get('created', '')
        if created:
            try:
                # Try to extract year from various date formats
                import re
                year_match = re.search(r'(\d{4})', str(created))
                if year_match:
                    year = int(year_match.group(1))
                    if 2020 <= year <= 2025:  # Reasonable range
                        years[year] = years.get(year, 0) + 1
                        if year >= 2024:  # Recent proposals
                            recent_proposals += 1
            except:
                continue
    
    col1, col2 = st.columns(2)
    
    with col1:
        if years:
            st.markdown("**Proposals by Year:**")
            for year in sorted(years.keys(), reverse=True)[:5]:
                st.write(f"**{year}:** {years[year]} proposals")
        else:
            st.info("No timeline data available")
    
    with col2:
        st.metric("Recent Proposals (2024+)", recent_proposals)
        
        # Activity trend
        if len(years) >= 2:
            sorted_years = sorted(years.keys())
            if len(sorted_years) >= 2:
                recent_year = sorted_years[-1]
                previous_year = sorted_years[-2]
                
                trend = years[recent_year] - years[previous_year]
                trend_text = "📈 Increasing" if trend > 0 else "📉 Decreasing" if trend < 0 else "➡️ Stable"
                st.write(f"**Activity Trend:** {trend_text}")

def render_network_analytics(proposals: List[Dict]):
    """Render network/blockchain comparison analytics"""
    
    st.markdown("#### 🌐 Network Analysis")
    
    # Count by network type
    network_counts = {}
    network_status = {}
    
    for proposal in proposals:
        network = proposal.get('standard_type', 'Unknown')
        status = proposal.get('status', 'Unknown').lower()
        
        network_counts[network] = network_counts.get(network, 0) + 1
        
        if network not in network_status:
            network_status[network] = {'active': 0, 'draft': 0, 'total': 0}
        
        network_status[network]['total'] += 1
        if status in ['final', 'active', 'production', 'living']:
            network_status[network]['active'] += 1
        elif status == 'draft':
            network_status[network]['draft'] += 1
    
    # Display network comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Network Activity:**")
        for network in sorted(network_counts.keys()):
            count = network_counts[network]
            percentage = (count / len(proposals)) * 100
            st.write(f"**{network}:** {count} ({percentage:.1f}%)")
    
    with col2:
        st.markdown("**Network Health:**")
        for network in sorted(network_status.keys()):
            stats = network_status[network]
            if stats['total'] > 0:
                active_rate = (stats['active'] / stats['total']) * 100
                health_icon = "🟢" if active_rate > 50 else "🟡" if active_rate > 25 else "🔴"
                st.write(f"{health_icon} **{network}:** {active_rate:.1f}% active")

def calculate_status_health(status_counts: Dict[str, int], total: int) -> float:
    """Calculate ecosystem health score based on status distribution"""
    
    # Weight different statuses
    status_weights = {
        'final': 2.0,
        'active': 2.0,
        'production': 2.0,
        'living': 2.0,
        'review': 1.5,
        'proposed': 1.5,
        'last call': 1.8,
        'draft': 1.0,
        'stagnant': 0.2,
        'withdrawn': 0.1,
        'rejected': 0.1
    }
    
    weighted_score = 0
    for status, count in status_counts.items():
        weight = status_weights.get(status.lower(), 0.5)
        weighted_score += (count / total) * weight * 10
    
    return min(weighted_score, 10.0)  # Cap at 10