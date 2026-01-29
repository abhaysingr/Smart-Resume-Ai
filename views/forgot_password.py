import streamlit as st
import secrets
from config.database import store_reset_token

def render_forgot_password():
    """Render the forgot password page."""
    st.title("Forgot Password")
    
    with st.form("forgot_password_form"):
        email = st.text_input("Enter your email address")
        submitted = st.form_submit_button("Get Reset Link")
        
        if submitted:
            token = secrets.token_urlsafe(16)
            if store_reset_token(email, token):
                reset_link = f"http://localhost:8501/?page=reset_password&token={token}"
                st.success("A password reset link has been generated. In a real application, this would be emailed to you.")
                st.info(f"Click the link to reset your password: {reset_link}")
            else:
                st.error("Could not process request. Please try again.")
