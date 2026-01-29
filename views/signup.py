import streamlit as st
import re
from config.database import add_user

def render_signup():
    """Render the signup page."""
    st.title("Sign Up")

    EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
    
    with st.form("signup_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        submitted = st.form_submit_button("Sign Up")
        
        if submitted:
            if not email or not password or not confirm_password:
                st.error("All fields are required.")
            elif not EMAIL_REGEX.match(email):
                st.error("Invalid email format. Please enter a valid email address.")
            elif len(password) < 8:
                st.error("Password is too short. It must be at least 8 characters long.")
            elif password == confirm_password:
                if add_user(email, password):
                    st.success("You have successfully signed up! Please go to the Sign In page to log in.")
                else:
                    st.error("Email already exists. Please try a different email.")
            else:
                st.error("Passwords do not match.")
