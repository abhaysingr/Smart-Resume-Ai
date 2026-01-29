import streamlit as st
from config.database import get_user_email_by_token, update_user_password, delete_reset_token

def render_reset_password():
    """Render the reset password page."""
    st.title("Reset Password")
    
    token = st.query_params.get("token")
    
    if not token:
        st.error("Invalid or missing reset token.")
        return
        
    email = get_user_email_by_token(token)
    
    if not email:
        st.error("Invalid or expired reset token. Please request a new one.")
        return
        
    with st.form("reset_password_form"):
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        submitted = st.form_submit_button("Reset Password")
        
        if submitted:
            if new_password == confirm_password:
                if update_user_password(email, new_password):
                    delete_reset_token(token)
                    st.success("Your password has been updated successfully! You can now sign in with your new password.")
                else:
                    st.error("Failed to update password. Please try again.")
            else:
                st.error("Passwords do not match.")
