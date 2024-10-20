import streamlit as st
from login import login
from dashboard import dashboard

# Use session state to manage login status
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Check login status
if st.session_state['logged_in']:
    # If logged in, show the dashboard
    dashboard()
else:
    # If not logged in, show the login page
    if login():
        st.session_state['logged_in'] = True
        # Update the query parameter to simulate page navigation
        st.query_params['logged_in'] = "true"  # Change to st.query_params
        st.rerun()  # Change to st.rerun()
