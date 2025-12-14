"""
Week 9
Main Dashboard page for the Multi-Domain Intelligence Platform.
This page appears after successful login.
"""

import streamlit as st

# configure the page
st.set_page_config(
    page_title="Dashboard - Intelligence Platform",
    page_icon="🏠",
    layout="wide"
)

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("❌ You must be logged in to view this page")
    
    # Button to go to login page
    if st.button("Go to Login Page"):
        st.switch_page("Home.py")
    
    # Stop the execution here, don't show the rest of the page
    st.stop()

# Get user info from session state
user_info = st.session_state.user_info

# Page guard
if user_info is None:
    st.error("User information not found")
    if st.button("Go to Login"):
        st.switch_page("Home.py")
    st.stop()


# Page Header
st.title("🏠 Dashboard")
st.write(f"Welcome, **{user_info['username']}**!")
st.write("---")

# Dashboard's description
st.markdown("""
### Multi-Domain Intelligence Platform Dashboard
            
Navigate to different domains using the sidebar menu or the cards below.
Each domain provides specialized analytics and management tools for:
""")

# Create cards for each domain
col1, col2, col3 = st.columns(3)

with col1:
    # Cybersecurity dashboard card
    st.subheader("🔒 Cybersecurity")
    st.write("Monitor security incidents and threats")
    st.write("• View all incidents")
    st.write("• Track incident severity")
    st.write("• Analyze incident status")
    
    # Button to go to cybersecurity page
    if st.button("Go to Cybersecurity", key="cyber_btn"):
        st.switch_page("pages/2_Cybersecurity.py")

with col2:
    # Data Science dashboard card
    st.subheader("📈 Data Science")
    st.write("Manage datasets and analytics")
    st.write("• View dataset metadata")
    st.write("• Analyze data statistics")
    st.write("• Track dataset usage")
    
    # Button to go to data science page
    if st.button("Go to Data Science", key="ds_btn"):
        st.switch_page("pages/3_DataScience.py")

with col3:
    # IT Operations dashboard card
    st.subheader("⚙️ IT Operations")
    st.write("Manage IT tickets and operations")
    st.write("• View all tickets")
    st.write("• Track ticket status")
    st.write("• Analyze ticket information")
    
    # Button to go to IT operations page
    if st.button("Go to IT Operations", key="it_btn"):
        st.switch_page("pages/4_ITOperations.py")

st.write("---")

# Sidebar navigation
with st.sidebar:
    st.title("🔍 Navigation")
    st.write("---")
    
    if st.button("🔒 Cybersecurity"):
        st.switch_page("pages/2_Cybersecurity.py")
    
    if st.button("📊 Data Science"):
        st.switch_page("pages/3_DataScience.py")
    
    if st.button("⚙️ IT Operations"):
        st.switch_page("pages/4_ITOperations.py")
    
    if st.button("Settings"):
        st.switch_page("pages/5_Settings.py")
    
    st.write("---")
    
    # Logout button
    if st.button("🚪 Logout", type="secondary"):
        # Clear the session state
        st.session_state.logged_in = False
        st.session_state.user_info = None
        st.success("Logged out successfully!")
        st.switch_page("Home.py")

st.caption(f"Logged in as: {st.session_state.user_info['username']} | Role: {st.session_state.user_info.get('role', 'user')}")