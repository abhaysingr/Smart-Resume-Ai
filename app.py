import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config at the very beginning
st.set_page_config(
    page_title="Smart Resume AI",
    page_icon="🚀",
    layout="wide"
)

import uuid
import requests
from utils.logger import setup_logger
from utils.resume_analyzer import ResumeAnalyzer as OldResumeAnalyzer

from utils.resume_builder import ResumeBuilder
from config.database import (
    verify_admin, log_admin_action
)
from config.job_roles import JOB_ROLES
from dashboard.dashboard import DashboardManager
from ui_components import render_sidebar, clean_page_name

# Import Views
from views.home import render_home

from views.builder import render_builder
from views.dashboard_view import render_dashboard
from views.job_search import render_job_search
from views.feedback import render_feedback_page
from views.about import render_about
from views.cover_letter import render_cover_letter_page
from views.portfolio import render_portfolio_page
from views.signup import render_signup
from views.signin import render_signin
from views.forgot_password import render_forgot_password
from views.reset_password import render_reset_password
from views.ats_optimizer import render_ats_optimizer

logger = setup_logger(__name__)

class ResumeApp:
    def __init__(self):
        """Initialize the application"""
        if 'form_data' not in st.session_state:
            st.session_state.form_data = {
                'personal_info': {
                    'full_name': '',
                    'email': '',
                    'phone': '',
                    'location': '',
                    'linkedin': '',
                    'portfolio': ''
                },
                'summary': '',
                'experiences': [],
                'education': [],
                'projects': [],
                'skills_categories': {
                    'technical': [],
                    'soft': [],
                    'languages': [],
                    'tools': []
                },
                'certifications': []
            }
        
        # Initialize navigation state
        if 'page' not in st.session_state:
            st.session_state.page = 'home'
            
        # Initialize admin state
        if 'is_admin' not in st.session_state:
            st.session_state.is_admin = False

        # Initialize user login state
        if 'is_logged_in' not in st.session_state:
            st.session_state.is_logged_in = False
        if 'user_email' not in st.session_state:
            st.session_state.user_email = None
        
        # Initialize managers
        self.dashboard_manager = DashboardManager()
        self.old_analyzer = OldResumeAnalyzer()

        self.builder = ResumeBuilder()
        self.job_roles = JOB_ROLES
        
        # Define pages with their rendering functions
        self.pages = {
            "🏠 HOME": render_home,

            "📝 RESUME BUILDER": lambda: render_builder(self.builder),
            "🎯 ATS RESUME OPTIMIZER": render_ats_optimizer,
            "✉️ COVER LETTER GENERATOR": render_cover_letter_page,
            "🌐 PORTFOLIO VIEWER": render_portfolio_page,
            "📊 DASHBOARD": lambda: render_dashboard(self.dashboard_manager),
            "🎯 JOB SEARCH": render_job_search,
            "💬 FEEDBACK": render_feedback_page,
            "ℹ️ ABOUT": render_about,
            "🔑 SIGN IN": render_signin,
            "📝 SIGN UP": render_signup,
            "🔑 FORGOT PASSWORD": render_forgot_password,
        }
        
        # Initialize session state
        if 'user_id' not in st.session_state:
            # Generate a unique user ID for this session
            st.session_state.user_id = str(uuid.uuid4())
            logger.info(f"New session started with User ID: {st.session_state.user_id}")
            
        if 'selected_role' not in st.session_state:
            st.session_state.selected_role = None
        
        # Database is now managed by Alembic, no init needed here.
        # init_database()
        
        # Load external CSS
        with open('style/style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
        # Load Google Fonts
        st.markdown("""
            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
        """, unsafe_allow_html=True)

    def load_lottie_url(self, url: str):
        """Load Lottie animation from URL with fallback"""
        try:
            r = requests.get(url, timeout=5)  # Add timeout
            if r.status_code == 200:
                return r.json()
        except (requests.RequestException, ValueError):
            pass
        
        # Fallback: return a simple loading animation
        return {
            "v": "5.7.4",
            "fr": 60,
            "ip": 0,
            "op": 120,
            "w": 200,
            "h": 200,
            "assets": [],
            "layers": [{
                "ddd": 0,
                "ind": 1,
                "ty": 4,
                "nm": "Circle",
                "sr": 1,
                "ks": {
                    "o": {"a": 0, "k": 100},
                    "r": {
                        "a": 1,
                        "k": [{"t": 0, "s": [0]}, {"t": 120, "s": [360]}],
                        "ix": 10
                    },
                    "p": {"a": 0, "k": [100, 100, 0]},
                    "a": {"a": 0, "k": [0, 0, 0]},
                    "s": {"a": 0, "k": [100, 100, 100]}
                },
                "shapes": [{
                    "ty": "el",
                    "p": {"a": 0, "k": [0, 0]},
                    "s": {"a": 0, "k": [60, 60]},
                    "c": {"a": 0, "k": [0, 0.6, 1]}
                }]
            }]
        }

    def main(self):
        """Main application entry point"""
        
        # Handle page routing from query parameters
        query_params = st.query_params
        if "page" in query_params and query_params["page"] == "reset_password":
            render_reset_password()
            return

        # Admin login/logout in sidebar
        with st.sidebar:
            render_sidebar(
                self.pages,
                self.load_lottie_url,
                st.session_state.get('is_admin', False),
                st.session_state.get('current_admin_email'),
                verify_admin,
                log_admin_action,
                st.session_state.get('is_logged_in', False),
                st.session_state.get('user_email')
            )
        
        # Force home page on first load
        if 'initial_load' not in st.session_state:
            st.session_state.initial_load = True
            st.session_state.page = 'home'
            st.rerun()
        
        # Get current page and render it
        current_page = st.session_state.get('page', 'home')
        
        # Create a mapping of cleaned page names to original names
        page_mapping = {clean_page_name(name): name for name in self.pages.keys()}
        
        # Handle aliases and normalization
        aliases = {

            'builder': 'resume_builder',
            'insights': 'dashboard',
            'forgot_password': 'forgot_password'
        }
        
        # Normalize current_page to ensure it matches page_mapping keys
        # 1. Check aliases first (e.g. 'builder' -> 'resume_builder')
        # 2. If not in aliases, try cleaning the name (e.g. "Resume Analyzer" -> "resume_analyzer")
        current_page_lower = str(current_page).lower().strip()
        target_page = aliases.get(current_page_lower, clean_page_name(str(current_page)))
        
        # Render the appropriate page
        if target_page in page_mapping:
            self.pages[page_mapping[target_page]]()
        else:
            # Default to home page if invalid page
            render_home()
    
if __name__ == "__main__":
    app = ResumeApp()
    app.main()
