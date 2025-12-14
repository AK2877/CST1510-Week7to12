"""
Week 9
IT Operations Dashboard for managing IT tickets.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from app.data.db import connect_database
from app.data.tickets import get_all_tickets

# configure the page
st.set_page_config(
    page_title="IT Operations",
    page_icon="⚙️",
    layout="wide"
)

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("❌ You must be logged in to view this page")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

# Page Header
st.title("⚙️ IT Operations Dashboard")
st.write("Manage and analyze IT tickets with interactive visualizations")
st.write("---")

# Connect to database and get the data
conn = connect_database()

tickets_df = get_all_tickets(conn)

# Convert date columns to datetime
date_columns = ['created_date', 'resolved_date']
for col in date_columns:
    if col in tickets_df.columns:
        tickets_df[col] = pd.to_datetime(tickets_df[col], errors='coerce')

# Create 4 columns for statistics
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Total tickets
    total = len(tickets_df)
    st.metric("Total Tickets", total)

with col2:
    # Open tickets
    open_tickets = len(tickets_df[tickets_df['status'] == 'Open']) if len(tickets_df) > 0 else 0
    st.metric("Open Tickets", open_tickets)

with col3:
    # High priority tickets
    high_priority = len(tickets_df[tickets_df['priority'] == 'High']) if len(tickets_df) > 0 else 0
    st.metric("High Priority", high_priority)

with col4:
    # Average resolution time
    if len(tickets_df) > 0 and 'created_date' in tickets_df.columns and 'resolved_date' in tickets_df.columns:
        resolved_tickets = tickets_df[tickets_df['status'] == 'Resolved']
        if len(resolved_tickets) > 0:
            resolved_tickets['resolution_days'] = (resolved_tickets['resolved_date'] - resolved_tickets['created_date']).dt.days
            avg_resolution = resolved_tickets['resolution_days'].mean()
            st.metric("Avg Resolution (days)", f"{avg_resolution:.1f}")
        else:
            st.metric("Avg Resolution (days)", "N/A")
    else:
        st.metric("Avg Resolution (days)", "N/A")


# Pie & Bar chart
st.header("📈 Ticket Analysis Charts")

# Create two columns for charts
col1, col2 = st.columns(2)

with col1:
    # Chart 1: Tickets by Priority (Bar Chart)
    st.subheader("Tickets by Priority")
    
    if len(tickets_df) > 0 and 'priority' in tickets_df.columns:
        # Count tickets by priority
        priority_counts = tickets_df['priority'].value_counts().reset_index()
        priority_counts.columns = ['Priority', 'Count']
        
        # Define color sequence based on priority
        priority_colors = {
            'Critical': 'red',
            'High': 'orange',
            'Medium': 'yellow',
            'Low': 'green'
        }
        
        # Create bar chart
        fig1 = px.bar(
            priority_counts,
            x='Priority',
            y='Count',
            color='Priority',
            title="Number of Tickets by Priority Level",
            color_discrete_map=priority_colors,
            text='Count'
        )
        
        # Update layout
        fig1.update_layout(
            xaxis_title="Priority Level",
            yaxis_title="Number of Tickets",
            showlegend=False
        )
        
        # Display the chart
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("No priority data available")

with col2:
    # Chart 2: Tickets by Status (Pie Chart)
    st.subheader("Tickets by Status")
    
    if len(tickets_df) > 0 and 'status' in tickets_df.columns:
        # Count tickets by status
        status_counts = tickets_df['status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        
        # Create pie chart
        fig2 = px.pie(
            status_counts,
            values='Count',
            names='Status',
            title="Distribution of Tickets by Status",
            hole=0.3
        )
        
        # Update layout
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        
        # Display the chart
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No status data available")


# Line chart
st.header("📅 Ticket Trends Over Time")

if len(tickets_df) > 0 and 'created_date' in tickets_df.columns:
    # Create a line chart showing tickets over time
    st.subheader("Monthly Ticket Creation")
    
    # Group by month
    tickets_df['Month'] = tickets_df['created_date'].dt.to_period('M').astype(str)
    monthly_counts = tickets_df.groupby('Month').size().reset_index(name='Count')
    
    # Create line chart
    fig3 = px.line(
        monthly_counts,
        x='Month',
        y='Count',
        title="Tickets Created Per Month",
        markers=True,
        line_shape='spline'
    )
    
    # Update layout
    fig3.update_layout(
        xaxis_title="Month",
        yaxis_title="Number of Tickets Created",
        hovermode='x unified'
    )
    
    # Add a trend line
    fig3.add_trace(
        go.Scatter(
            x=monthly_counts['Month'],
            y=monthly_counts['Count'].rolling(window=3, center=True).mean(),
            mode='lines',
            name='3-Month Moving Average',
            line=dict(color='red', dash='dash')
        )
    )
    
    # Display the chart
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("No date data available for time trend analysis")

# Filtering tickets
st.header("🎯 Filter and Search Tickets")

# Create columns for filters
col1, col2, col3 = st.columns(3)

with col1:
    # Filter by priority
    if 'priority' in tickets_df.columns:
        priorities = ["All"] + sorted(tickets_df['priority'].unique().tolist())
        selected_priority = st.selectbox("Filter by Priority", priorities)
    else:
        selected_priority = "All"

with col2:
    # Filter by status
    if 'status' in tickets_df.columns:
        statuses = ["All"] + sorted(tickets_df['status'].unique().tolist())
        selected_status = st.selectbox("Filter by Status", statuses)
    else:
        selected_status = "All"

with col3:
    # Filter by category
    if 'category' in tickets_df.columns:
        categories = ["All"] + sorted(tickets_df['category'].unique().tolist())
        selected_category = st.selectbox("Filter by Category", categories)
    else:
        selected_category = "All"

# Applying the filters
filtered_df = tickets_df.copy()

if selected_priority != "All":
    filtered_df = filtered_df[filtered_df['priority'] == selected_priority]

if selected_status != "All":
    filtered_df = filtered_df[filtered_df['status'] == selected_status]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df['category'] == selected_category]

# Show the filtered results
st.write(f"**Filtered Results:** {len(filtered_df)} tickets found")

if len(filtered_df) > 0:
    st.dataframe(filtered_df, use_container_width=True)


conn.close()

# Sidebar
with st.sidebar:
    st.title("🔍 Navigation")
    st.write("---")
    
    # Back to dashboard button
    if st.button("🏠 Back to Dashboard"):
        st.switch_page("pages/1_Dashboard.py")
    
    # Logout button
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_info = None
        st.switch_page("Home.py")