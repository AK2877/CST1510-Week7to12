"""
Week 9
Settings Dashboard to change the settings
"""

import streamlit as st
from app.auth import hash_password, validate_password
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user

# Configure the page
st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide"
)

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("❌ You must be logged in to view this page")
    
    # Button to go to login page
    if st.button("Go to Login Page"):
        st.switch_page("Home.py")
    st.stop()

# Page Header
st.title("⚙️ Settings")
st.markdown("---")

# User's information
if st.session_state.user_info:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Profile Information")
        st.info(f"**Username:** {st.session_state.user_info['username']}")
        st.info(f"**Role:** {st.session_state.user_info.get('role', 'user')}")
        st.info(f"**User ID:** {st.session_state.user_info['id']}")
    
    with col2:
        st.subheader("Account Actions")

# Change password
with st.expander("Change Password", expanded=True):
    with st.form("change_password"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        if st.form_submit_button("Update Password"):
            if not current_password or not new_password or not confirm_password:
                st.error("Please fill in all fields")
            elif new_password != confirm_password:
                st.error("New passwords do not match")
            else:
                # Validate password strength
                is_valid, message = validate_password(new_password)
                if not is_valid:
                    st.error(message)
                else:
                    # Verify current password
                    conn = connect_database()
                    user = get_user_by_username(st.session_state.user_info['username'])
                    conn.close()
                    
                    if user:
                        from app.auth.auth_utils import verify_password
                        if verify_password(current_password, user[2]):
                            # Update password
                            new_hash = hash_password(new_password)
                            conn = connect_database()
                            cursor = conn.cursor()
                            cursor.execute(
                                "UPDATE users SET password_hash = ? WHERE id = ?",
                                (new_hash, st.session_state.user_info['id'])
                            )
                            conn.commit()
                            conn.close()
                            st.success("✅ Password updated successfully!")
                        else:
                            st.error("Current password is incorrect")
                    else:
                        st.error("User not found")

# Profile settings
with st.expander("Profile Settings"):
    col1, col2 = st.columns(2)
    
    with col1:
        theme = st.selectbox(
            "Theme",
            ["Light", "Dark", "System"]
        )
        
        timezone = st.selectbox(
            "Timezone",
            ["UTC", "GMT", "EST", "PST", "CET", "IST"]
        )
    
    with col2:
        notifications = st.checkbox("Email Notifications", value=True)
        auto_refresh = st.checkbox("Auto-refresh Dashboard", value=False)
        refresh_interval = st.slider(
            "Refresh Interval (minutes)",
            min_value=1,
            max_value=60,
            value=5,
            disabled=not auto_refresh
        )
    
    if st.button("Save Profile Settings"):
        st.success("Profile settings saved!")


# System information
with st.expander("System Information"):
    import platform
    import streamlit as st
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Platform Information**")
        st.code(f"OS: {platform.system()} {platform.release()}")
        st.code(f"Python: {platform.python_version()}")
        st.code(f"Streamlit: {st.__version__}")
    
    with col2:
        st.write("**Application Information**")
        st.code("Multi-Domain Intelligence Platform")
        st.code("Version: 1.0.0")
        st.code(f"User: {st.session_state.user_info['username']}")

# Deletion options
with st.expander("Deletion options", expanded=False):
    st.warning("These actions are irreversible!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Delete Account", type="secondary"):
            st.error("Account deletion requires confirmation")
    
    with col2:
        if st.button("Reset All Data", type="secondary"):
            st.error("This will delete all your data!")
    
    with col3:
        if st.button("Log Out All Sessions", type="secondary"):
            st.session_state.logged_in = False
            st.session_state.user_info = None
            st.success("Logged out from all sessions!")
            st.switch_page("Home.py")

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