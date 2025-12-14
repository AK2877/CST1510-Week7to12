"""
Week 9
Data Science Dashboard for managing and analyzing datasets.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app.data.db import connect_database
from app.data.datasets import get_all_datasets

# configure the page
st.set_page_config(
    page_title="Data Science",
    page_icon="📊",
    layout="wide"
)

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("❌ You must be logged in to view this page")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()

# Page Header
st.title("📊 Data Science Dashboard")
st.write("Manage and analyze datasets with interactive visualizations")
st.write("---")

# Connect to database and get the data
conn = connect_database()

datasets_df = get_all_datasets(conn)

# Create 4 columns for statistics
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_datasets = len(datasets_df)
    st.metric("Total Datasets", total_datasets)

with col2:
    total_records = datasets_df['record_count'].sum() if not datasets_df.empty else 0
    st.metric("Total Records", f"{total_records:,}")

with col3:
    total_size = datasets_df['file_size_mb'].sum() if not datasets_df.empty else 0
    st.metric("Total Size", f"{total_size:.1f} MB")

with col4:
    unique_categories = datasets_df['category'].nunique() if not datasets_df.empty else 0
    st.metric("Categories", unique_categories)


# Pie & Bar chart
st.header("📊 Dataset Distribution Analysis")

# Create two columns for charts
col1, col2 = st.columns(2)

with col1:
    # Chart 1: Datasets by Category (Pie Chart)
    st.subheader("Datasets by Category")
    
    if len(datasets_df) > 0 and 'category' in datasets_df.columns:
        # Count datasets by category
        category_counts = datasets_df['category'].value_counts().reset_index()
        category_counts.columns = ['Category', 'Count']
        
        # Create pie chart
        fig1 = px.pie(
            category_counts,
            values='Count',
            names='Category',
            title="Distribution of Datasets by Category",
            hole=0.3
        )
        
        # Update layout
        fig1.update_traces(textposition='inside', textinfo='percent+label')
        
        # Display the chart
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("No category data available")

with col2:
    # Chart 2: Total Records by Category (Bar Chart)
    st.subheader("Total Records by Category")
    
    if len(datasets_df) > 0 and 'category' in datasets_df.columns and 'record_count' in datasets_df.columns:
        # Sum records by category
        records_by_category = datasets_df.groupby('category')['record_count'].sum().reset_index()
        records_by_category.columns = ['Category', 'Total Records']
        
        # Create bar chart
        fig2 = px.bar(
            records_by_category,
            x='Category',
            y='Total Records',
            color='Category',
            title="Total Number of Records by Category",
            text='Total Records'
        )
        
        # Format y-axis with commas
        fig2.update_layout(
            yaxis=dict(tickformat=",d"),
            xaxis_title="Category",
            yaxis_title="Total Records",
            showlegend=False
        )
        
        # Display the chart
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No record count data available")


# Scatter Plot
st.header("🔍 Dataset Size Analysis")

if len(datasets_df) > 0 and 'record_count' in datasets_df.columns and 'file_size_mb' in datasets_df.columns:
    # Create a scatter plot
    st.subheader("Record Count vs File Size")
    
    fig3 = px.scatter(
        datasets_df,
        x='record_count',
        y='file_size_mb',
        size='record_count',
        color='category',
        hover_data=['dataset_name', 'source'],
        title="Relationship Between Record Count and File Size",
        labels={
            'record_count': 'Number of Records',
            'file_size_mb': 'File Size (MB)',
            'category': 'Dataset Category'
        }
    )
    
    # Update layout
    fig3.update_layout(
        xaxis_title="Number of Records",
        yaxis_title="File Size (MB)",
        hovermode='closest'
    )
    
    # Display the chart
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("No data available for scatter plot")


# Histogram
st.header("📏 File Size Distribution")

if len(datasets_df) > 0 and 'file_size_mb' in datasets_df.columns:
    # Create a histogram of file sizes
    st.subheader("Distribution of Dataset File Sizes")
    
    fig4 = px.histogram(
        datasets_df,
        x='file_size_mb',
        nbins=20,
        title="Frequency Distribution of Dataset File Sizes",
        labels={'file_size_mb': 'File Size (MB)'},
        color_discrete_sequence=['#636EFA']
    )
    
    # Add mean line
    mean_size = datasets_df['file_size_mb'].mean()
    fig4.add_vline(x=mean_size, line_dash="dash", line_color="red", 
                   annotation_text=f"Mean: {mean_size:.1f} MB")
    
    # Update layout
    fig4.update_layout(
        xaxis_title="File Size (MB)",
        yaxis_title="Number of Datasets",
        bargap=0.1
    )
    
    # Display the chart
    st.plotly_chart(fig4, use_container_width=True)
else:
    st.info("No file size data available")


# Filtering datasets
st.header("🎯 Filter and Search Datasets")

# Create columns for filters
col1, col2 = st.columns(2)

with col1:
    # Filter by category
    if 'category' in datasets_df.columns:
        categories = ["All"] + sorted(datasets_df['category'].unique().tolist())
        selected_category = st.selectbox("Filter by Category", categories)
    else:
        selected_category = "All"

with col2:
    # Filter by source
    if 'source' in datasets_df.columns:
        sources = ["All"] + sorted(datasets_df['source'].unique().tolist())
        selected_source = st.selectbox("Filter by Source", sources)
    else:
        selected_source = "All"

# File size range filter
if 'file_size_mb' in datasets_df.columns:
    min_size = float(datasets_df['file_size_mb'].min())
    max_size = float(datasets_df['file_size_mb'].max())
    size_range = st.slider(
        "Filter by File Size (MB)",
        min_value=min_size,
        max_value=max_size,
        value=(min_size, max_size)
    )

# Applying the filters
filtered_df = datasets_df.copy()

if selected_category != "All":
    filtered_df = filtered_df[filtered_df['category'] == selected_category]

if selected_source != "All":
    filtered_df = filtered_df[filtered_df['source'] == selected_source]

if 'file_size_mb' in datasets_df.columns:
    filtered_df = filtered_df[
        (filtered_df['file_size_mb'] >= size_range[0]) &
        (filtered_df['file_size_mb'] <= size_range[1])
    ]

# Show the filtered results
st.write(f"**Filtered Results:** {len(filtered_df)} datasets found")

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