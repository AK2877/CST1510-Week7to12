"""
Week 9
Cybersecurity Dashboard for monitoring security incidents.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app.data.db import connect_database
from app.data.incidents import get_all_incidents

# onfigure the page
st.set_page_config(
    page_title="Cybersecurity",
    page_icon="🔒",
    layout="wide"
)

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("❌ You must be logged in to view this page")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

# Page Header
st.title("🔒 Cybersecurity Dashboard")
st.write("Monitor and manage security incidents")
st.write("---")

# Connect to database and get the data
conn = connect_database()
incidents_df = get_all_incidents(conn)

# Convert date column to datetime for better analysis
if 'date' in incidents_df.columns:
    incidents_df['date'] = pd.to_datetime(incidents_df['date'], errors='coerce')


st.header("📊 Incident Statistics")

# Create 4 columns for statistics
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Total incidents
    total = len(incidents_df)
    st.metric("Total Incidents", total)

with col2:
    # High severity incidents
    high_severity = len(incidents_df[incidents_df['severity'] == 'High'])
    st.metric("High Severity", high_severity)

with col3:
    # Open incidents
    open_incidents = len(incidents_df[incidents_df['status'] == 'Open'])
    st.metric("Open Incidents", open_incidents)

with col4:
    # Resolved incidents
    resolved = len(incidents_df[incidents_df['status'] == 'Resolved'])
    st.metric("Resolved", resolved)


# Show the incidents table
st.header("📋 All Incidents")

# Check if we have data
if len(incidents_df) > 0:
    # Show the dataframe
    st.dataframe(incidents_df, use_container_width=True)
    
    st.write(f"Showing {len(incidents_df)} incidents from the database")
else:
    st.info("No incidents found in the database")


# Bar & Pie Chart
st.header("📈 Incident Analysis Charts")

# Create two columns for charts
col1, col2 = st.columns(2)

with col1:
    # Chart 1: Incidents by Severity (Bar Chart)
    st.subheader("Incidents by Severity")
    
    if len(incidents_df) > 0:
        # Count incidents by severity
        severity_counts = incidents_df['severity'].value_counts().reset_index()
        severity_counts.columns = ['Severity', 'Count']
        
        # Create bar chart
        fig1 = px.bar(
            severity_counts,
            x='Severity',
            y='Count',
            color='Severity',
            title="Number of Incidents by Severity Level",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        
        # Update layout for better appearance
        fig1.update_layout(
            xaxis_title="Severity Level",
            yaxis_title="Number of Incidents",
            showlegend=False
        )
        
        # Display the chart
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("No data available for chart")

with col2:
    # Chart 2: Incidents by Status (Pie Chart)
    st.subheader("Incidents by Status")
    
    if len(incidents_df) > 0:
        # Count incidents by status
        status_counts = incidents_df['status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        
        # Create pie chart
        fig2 = px.pie(
            status_counts,
            values='Count',
            names='Status',
            title="Distribution of Incidents by Status",
            hole=0.3  # Makes it a donut chart
        )
        
        # Update layout
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        
        # Display the chart
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No data available for chart")


# Line Chart
st.header("📅 Incident Trends Over Time")

if len(incidents_df) > 0 and 'date' in incidents_df.columns:
    # Create a line chart showing incidents over time
    st.subheader("Monthly Incident Trends")
    
    # Group by month
    incidents_df['Month'] = incidents_df['date'].dt.to_period('M').astype(str)
    monthly_counts = incidents_df.groupby('Month').size().reset_index(name='Count')
    
    # Create line chart
    fig3 = px.line(
        monthly_counts,
        x='Month',
        y='Count',
        title="Incidents Reported Per Month",
        markers=True,  # Add markers to each point
        line_shape='spline'  # Smooth line
    )
    
    # Update layout
    fig3.update_layout(
        xaxis_title="Month",
        yaxis_title="Number of Incidents",
        hovermode='x unified'  # Show all data on hover
    )
    
    # Display the chart
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("No date data available for time trend analysis")


# Filtering incidents
st.header("🔍 Filter Incidents")

# Create columns for filters
col1, col2, col3 = st.columns(3)

with col1:
    # Filter by severity
    severities = ["All"] + sorted(incidents_df['severity'].unique().tolist())
    selected_severity = st.selectbox("Filter by Severity", severities)

with col2:
    # Filter by status
    statuses = ["All"] + sorted(incidents_df['status'].unique().tolist())
    selected_status = st.selectbox("Filter by Status", statuses)

with col3:
    # Filter by incident type
    types = ["All"] + sorted(incidents_df['incident_type'].unique().tolist())
    selected_type = st.selectbox("Filter by Type", types)

# Applying the filters
filtered_df = incidents_df.copy()

if selected_severity != "All":
    filtered_df = filtered_df[filtered_df['severity'] == selected_severity]

if selected_status != "All":
    filtered_df = filtered_df[filtered_df['status'] == selected_status]

if selected_type != "All":
    filtered_df = filtered_df[filtered_df['incident_type'] == selected_type]

# Show the filtered results
st.write(f"**Filtered Results:** {len(filtered_df)} incidents found")

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
    
    st.write("---")
    
    # Logout button
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_info = None
        st.switch_page("Home.py")