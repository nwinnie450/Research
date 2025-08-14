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
            
            # Rate limit status
            rate_info = realtime_proposals.check_rate_limit()
            remaining = rate_info.get('rate', {}).get('remaining', 0)
            st.caption(f"API: {remaining} calls left")
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
                        
                        # Store results
                        st.session_state.proposals_result = {
                            'success': True,
                            'data': all_proposals,
                            'total_count': len(all_proposals)
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
        st.markdown("---")
    
    # Display fetched results
    if hasattr(st.session_state, 'proposals_result') and st.session_state.proposals_result:
        render_proposals_results(st.session_state.proposals_result, st.session_state.proposals_filter)
    
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
    """Render detailed view of proposals"""
    
    st.markdown(f"#### Detailed {standard} Information")
    
    for i, item in enumerate(items[:5]):  # Show first 5 in detail
        with st.expander(f"{standard}-{item.get('number', 'N/A')}: {item.get('title', 'No title')}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Basic Information:**")
                st.markdown(f"- **Number:** {item.get('number', 'N/A')}")
                st.markdown(f"- **Status:** {item.get('status', 'Unknown')}")
                st.markdown(f"- **Type:** {item.get('type', 'Not specified')}")
                st.markdown(f"- **Category:** {item.get('category', 'Not specified')}")
            
            with col2:
                st.markdown("**Links:**")
                if item.get('link'):
                    st.markdown(f"[📖 View Proposal]({item['link']})")
                if item.get('discussions_link'):
                    st.markdown(f"[💬 Discussions]({item['discussions_link']})")
                if item.get('author'):
                    st.markdown(f"- **Author:** {item['author']}")
            
            if item.get('summary'):
                st.markdown("**Summary:**")
                st.markdown(item['summary'])

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