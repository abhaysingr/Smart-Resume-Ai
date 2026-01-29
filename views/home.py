import streamlit as st
from ui_components import hero_section, feature_card

def render_home():
    # Hero Section
    hero_section(
        "Smart Resume AI",
        "Transform your career with AI-powered resume analysis and building. Get personalized insights and create professional resumes that stand out."
    )
    
    # Features Section
    col1, col2, col3 = st.columns(3)
    with col1:
        feature_card(
            "fas fa-robot",
            "AI-Powered Analysis",
            "Get instant feedback on your resume with advanced AI analysis that identifies strengths and areas for improvement."
        )
        if st.button("Go to ATS Optimizer", key="analyzer_btn", use_container_width=True):
            st.session_state.page = "🎯 ATS RESUME OPTIMIZER"
            st.rerun()

    with col2:
        feature_card(
            "fas fa-magic",
            "Smart Resume Builder",
            "Create professional resumes with our intelligent builder that suggests optimal content and formatting."
        )
        if st.button("Go to Builder", key="builder_btn", use_container_width=True):
            st.session_state.page = "📝 RESUME BUILDER"
            st.rerun()

    with col3:
        feature_card(
            "fas fa-chart-line",
            "Transform your journey with Career Insights",
            "Gain actionable insights and customized career strategies to drive long-term success."
        )
        if st.button("Go to Insights", key="insights_btn", use_container_width=True):
            st.session_state.page = "Dashboard"
            st.rerun()
    

    
    # Call-to-Action with Streamlit navigation
    col4 = st.columns([30])
    with col4[0]:
        if st.button("Get Started", key="get_started_btn", 
                    help="Click to start analyzing your resume",
                    use_container_width=True):
            st.session_state.page = "🎯 ATS RESUME OPTIMIZER"
            st.rerun()
