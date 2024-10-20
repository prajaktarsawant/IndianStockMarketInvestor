import streamlit as st

# Hardcoded credentials
user_data = {
    "Prajakta": {"email": "prajsawant141@gmail.com", "password": "Prajakta@123"},
    "Prasad": {"email": "prasadsawant11121999@gmail.com", "password": "Prasad@123"},
}

def login():
    st.title("Login Page")
    username = st.text_input("Enter Username")
    email = st.text_input("Enter Email")
    password = st.text_input("Enter Password", type="password")
    
    if st.button("Login"):
        if username in user_data and user_data[username]["email"] == email and user_data[username]["password"] == password:
            st.success("Login Successful!")
            return True
        else:
            st.error("Invalid Credentials")
            return False
    return False
