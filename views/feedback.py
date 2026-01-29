import streamlit as st
from feedback.feedback import FeedbackManager

def render_feedback_page():
    """Render the feedback page"""
    
    st.markdown("""
        <div class="feedback-header">
            <h1>📣 Your Voice Matters!</h1>
            <p>Help us improve Smart Resume AI with your valuable feedback</p>
        </div>
    """, unsafe_allow_html=True)

    # Initialize feedback manager
    feedback_manager = FeedbackManager()
    
    # Create tabs for form and statistics
    form_tab, stats_tab = st.tabs(["Share Feedback", "Feedback Overview"])
    
    with form_tab:
        feedback_manager.render_feedback_form()
        
    with stats_tab:
        feedback_manager.render_feedback_stats()
