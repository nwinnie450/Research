"""
Blockchain Proposals Component
Provides TIPs status filtering and other improvement proposals management
"""
import streamlit as st
import pandas as pd
from typing import Dict, List, Optional
from services.latest_proposals_fetcher import LatestProposalsFetcher
from services.blockchain_research_advisor import BlockchainResearchAdvisor

def render_proposals_interface():
    """Render the proposals management interface with TIPs status filtering"""
    
    st.markdown("---")
    st.markdown("### 📋 Blockchain Improvement Proposals")
    st.markdown("Explore and filter the latest TIPs, EIPs, BIPs, and other blockchain improvement proposals")
    
    # Initialize services
    proposals_fetcher = LatestProposalsFetcher()
    research_advisor = BlockchainResearchAdvisor()
    
    # Proposal type and status filter section
    with st.expander("⚙️ Filter Options", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Proposal Types")
            proposal_types = st.multiselect(
                "Select proposal types:",
                options=['EIP', 'BIP', 'SUP', 'TIP', 'BEP', 'LIP'],
                default=['TIP'],
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
                    # Fetch proposals using the backend service
                    result = proposals_fetcher.fetch_latest_proposals(
                        standards=proposal_types, 
                        status_filter=status_filter
                    )
                    
                    # Store results in session state
                    st.session_state.proposals_result = result
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
    
    # Display results if available
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
                          title: str, proposals_fetcher: LatestProposalsFetcher):
    """Quick fetch and display for action buttons"""
    
    with st.spinner(f"Fetching {title.lower()}..."):
        try:
            result = proposals_fetcher.fetch_latest_proposals(
                standards=proposal_types, 
                status_filter=status_filter
            )
            
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