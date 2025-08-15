#!/usr/bin/env python3
"""
Proposals component using scraped data (no API calls)
"""
import streamlit as st
import pandas as pd
from services.scraped_data_service import scraped_data_service
import time

def render_scraped_proposals():
    """Render proposals interface using scraped data"""
    
    st.header("🔗 Blockchain Improvement Proposals (Web Scraped)")
    
    # Protocol selection
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        protocol_options = {
            'tron': 'TRON (TIPs)',
            'ethereum': 'Ethereum (EIPs)',
            'bitcoin': 'Bitcoin (BIPs)',
            'binance_smart_chain': 'BNB Chain (BEPs)'
        }
        selected_protocol = st.selectbox("Select Protocol:", 
                                       options=list(protocol_options.keys()),
                                       format_func=lambda x: protocol_options[x],
                                       key="scraped_protocol")
    
    with col2:
        # Status filter
        status_options = {
            'all': 'All Statuses',
            'draft': 'Draft',
            'active': 'Active/Review', 
            'final': 'Final',
            'withdrawn': 'Withdrawn'
        }
        status_filter = st.selectbox("Filter by Status:", 
                                   options=list(status_options.keys()),
                                   format_func=lambda x: status_options[x],
                                   key="scraped_status")
    
    with col3:
        # Sort option
        sort_option = st.selectbox("Sort by:", 
                                 options=["Latest by Date", "Latest by Number"],
                                 key="scraped_sort")
        sort_by = 'number' if sort_option == "Latest by Number" else 'date'
    
    with col4:
        # Results limit
        limit = st.selectbox("Show:", 
                           options=[10, 20, 50, 100],
                           index=1,
                           key="scraped_limit")
    
    # Fetch proposals using scraped data
    try:
        st.info(f"📊 Loading {protocol_options[selected_protocol]} data...")
        
        proposals = scraped_data_service.get_latest_proposals(
            protocol=selected_protocol,
            limit=limit,
            status_filter=status_filter if status_filter != 'all' else None,
            sort_by=sort_by
        )
        
        if proposals:
            # Get data info
            data_info = scraped_data_service.load_protocol_data(selected_protocol)
            
            # Display results info
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📋 Results", len(proposals))
            
            with col2:
                status_text = status_options[status_filter]
                st.metric("🎯 Status", status_text)
            
            with col3:
                if data_info.get('generated_at_iso'):
                    st.metric("🕒 Data Updated", data_info['generated_at_iso'].split()[0])
            
            # Create DataFrame
            df_data = []
            for proposal in proposals:
                # Create clickable proposal number
                proposal_url = proposal.get('url', proposal.get('file_url', '#'))
                
                df_data.append({
                    'Number_Display': proposal.get('id', f"#{proposal.get('number', 'N/A')}"),
                    'Proposal': proposal_url,  # This will be the link
                    'Title': proposal.get('title', 'No title'),
                    'Status': proposal.get('status', 'Unknown'),
                    'Author': proposal.get('author', 'Unknown'),
                    'Created': proposal.get('created', 'Unknown'),
                    'Type': proposal.get('type', ''),
                })
            
            df = pd.DataFrame(df_data)
            
            # Display results
            st.subheader(f"📊 Results")
            st.write(f"Showing: {protocol_options[selected_protocol]} | Status: {status_options[status_filter]}")
            
            # Show data freshness
            if data_info.get('generated_at_iso'):
                st.caption(f"Fetched at: {data_info['generated_at_iso']}")
            
            # Configure DataFrame display
            column_config = {
                "Proposal": st.column_config.LinkColumn(
                    "Proposal",
                    width="medium",
                    help="Click to view the full proposal on GitHub",
                    display_text="Number_Display"
                ),
                "Title": st.column_config.TextColumn("Title", width="large"),
                "Status": st.column_config.TextColumn("Status", width="small"),
                "Author": st.column_config.TextColumn("Author", width="medium"), 
                "Created": st.column_config.TextColumn("Created", width="small"),
                "Type": st.column_config.TextColumn("Type", width="small"),
            }
            
            # Hide the helper column
            df_display = df.drop('Number_Display', axis=1)
            
            st.dataframe(
                df_display,
                column_config=column_config,
                hide_index=True,
                use_container_width=True
            )
            
            # Show success message for draft filtering
            if status_filter == 'draft' and len(proposals) > 0:
                st.success("✅ Successfully found draft proposals!")
                
                # Highlight TIP-156 specifically if found
                tip_156_found = any(p.get('number') == 156 for p in proposals)
                if tip_156_found and selected_protocol == 'tron':
                    st.info("🎯 TIP-156 (Vote instructions in TVM) found in draft results!")
            
        else:
            st.warning("No proposals found matching the selected criteria.")
            
            # Show debugging info for draft filter
            if status_filter == 'draft':
                st.info("💡 Try selecting 'All Statuses' to see available proposals.")
        
        # Show protocol statistics
        with st.expander("📈 Protocol Statistics", expanded=False):
            stats = scraped_data_service.get_proposal_stats()
            
            if selected_protocol in stats:
                protocol_stats = stats[selected_protocol]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Overview:**")
                    st.write(f"- Total proposals: {protocol_stats.get('total', 0)}")
                    st.write(f"- Data updated: {protocol_stats.get('generated_at_iso', 'Unknown')}")
                
                with col2:
                    st.write("**Status breakdown:**")
                    status_counts = protocol_stats.get('status_breakdown', {})
                    for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
                        st.write(f"- {status.capitalize()}: {count}")
    
    except Exception as e:
        st.error(f"Error loading proposals: {str(e)}")
        st.info("💡 Make sure to run the scraping scripts first to generate data files.")

if __name__ == "__main__":
    render_scraped_proposals()