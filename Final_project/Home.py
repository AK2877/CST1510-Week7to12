"""
Week 9
Home page for the Multi-Domain Intelligence Platform.
This is the main entry point with login and registration functionality.
"""

import streamlit as st
from app.auth import authenticate_user, register_user, validate_username, validate_password


# Configure the page
st.set_page_config(
    page_title="Multi-Domain Intelligence Platform",
    page_icon="🔐",
    layout="centered"
)

# Initializing login status if not already set
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Initializing user information if not already set
if 'user_info' not in st.session_state:
    st.session_state.user_info = None

# Page Header
st.title("🔐 Multi-Domain Intelligence Platform")
st.write("Welcome! Please login or register to access the dashboards.")
st.write("---")

# If user is already logged in, show a message and redirect option
if st.session_state.logged_in and st.session_state.user_info:
    st.success(f"You are already logged in as **{st.session_state.user_info['username']}**")
    
    # Button to go to dashboard
    if st.button("Go to Dashboard"):
        st.switch_page("pages/1_Dashboard.py")
    
    # Stop the program execution here so login/register forms don't show
    st.stop()


# Creating two tabs: one for login & one for registration
tab_login, tab_register = st.tabs(["Login", "Register"])


# Login Tab
with tab_login:
    st.header("Login to Your Account")
    
    # Create a form for login inputs
    with st.form("login_form"):
        # Input fields for username and password
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        # Submit button
        submit_login = st.form_submit_button("Login")
        
        # login when form is submitted
        if submit_login:
            # Check if both fields are filled
            if not username or not password:
                st.error("Please fill in both username and password")
            else:
                # Try to authenticate the user
                success, user_info = authenticate_user(username, password)
                
                if success:
                    # If login successful, update session state
                    st.session_state.logged_in = True
                    st.session_state.user_info = user_info
                    st.success(f"Welcome back, {username}!")
                    
                    # Show success message, then redirect
                    st.write("Redirecting to dashboard...")
                    st.switch_page("pages/1_Dashboard.py")
                else:
                    # Show error if login failed
                    st.error("Invalid username or password")


# Register Tab
with tab_register:
    st.header("Create New Account")
    
    # Create a form for registration
    with st.form("register_form"):
        # Input fields
        new_username = st.text_input("Choose a username")
        new_password = st.text_input("Choose a password", type="password")
        confirm_password = st.text_input("Confirm password", type="password")
        
        # Submit button
        submit_register = st.form_submit_button("Register")
        
        # register when form is submitted
        if submit_register:
            # Check if all fields are filled
            if not new_username or not new_password:
                st.error("Please fill in all fields")
            
            # Check if passwords match
            elif new_password != confirm_password:
                st.error("Passwords do not match")
            
            else:
                # Validate username format
                username_valid, username_msg = validate_username(new_username)
                if not username_valid:
                    st.error(username_msg)
                
                else:
                    # Validate password strength
                    password_valid, password_msg = validate_password(new_password)
                    if not password_valid:
                        st.error(password_msg)
                    
                    else:
                        # Try to register the user
                        success, message = register_user(new_username, new_password)
                        
                        if success:
                            st.success(message)
                            st.info("You can now login with your new account")
                        else:
                            st.error(message)