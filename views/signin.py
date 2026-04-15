import streamlit as st
from config.database import verify_user

def render_signin():
    """Render the signin page."""
    st.title("Sign In")
    
    with st.form("signin_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        submitted = st.form_submit_button("Sign In")
        
        if submitted:
            if verify_user(email, password):
                st.session_state['is_logged_in'] = True
                st.session_state['user_email'] = email
                
                # Write persistent cookie
                if 'cookie_controller' in st.session_state:
                    st.session_state.cookie_controller.set('auth_token', email)
                    
                # Setup auto-recovery from JSON profile
                from utils.profile_manager import load_profile
                profile = load_profile(email)
                if profile:
                    st.session_state.form_data = profile
                
                st.success("Logged in successfully!")
                # Redirect to dashboard
                st.session_state.page = 'dashboard'
                st.rerun()
            else:
                st.error("Invalid email or password.")

    if st.button("Forgot Password?"):
        st.session_state.page = 'forgot_password'
        st.rerun()

