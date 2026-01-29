import streamlit as st
from streamlit_lottie import st_lottie
import html
import re
from utils.generative_ai import generate_summary, generate_experience_description, generate_project_description, generate_ats_summary
import time
from datetime import datetime

def clean_page_name(page_name):
    """Helper to create consistent page keys from display names by removing emojis"""
    # Remove non-word characters (except spaces), strip, lower, and replace spaces with underscaces
    text = re.sub(r'[^\w\s]', '', page_name)
    return text.strip().lower().replace(" ", "_")

def page_header(title, subtitle=None):
    """Render a consistent page header with gradient background"""
    st.markdown(
        f'''
        <div class="page-header">
            <h1 class="header-title">{title}</h1>
            {f'<p class="header-subtitle">{subtitle}</p>' if subtitle else ''}
        </div>
        ''',
        unsafe_allow_html=True
    )

def hero_section(title, subtitle=None, description=None):
    """Render a modern hero section with gradient background and animations"""
    # If description is provided but subtitle is not, use description as subtitle
    if description and not subtitle:
        subtitle = description
        description = None
    
    st.markdown(
        f'''
        <div class="page-header hero-header">
            <h1 class="header-title">{title}</h1>
            {f'<div class="header-subtitle">{subtitle}</div>' if subtitle else ''}
            {f'<p class="header-description">{description}</p>' if description else ''}
        </div>
        ''',
        unsafe_allow_html=True
    )

def feature_card(icon, title, description):
    """
    Render a feature card using native Streamlit components.
    This approach is more secure, maintainable, and responsive.
    Styling should be applied to the 'stContainer' element and the
    'feature-icon' class in the main style.css file.
    """
    with st.container(border=True):
        # The icon is still HTML, but we are only injecting a class, which is safer.
        # For maximum security, one would validate the 'icon' parameter against a
        # list of allowed FontAwesome class names.
        st.markdown(f'<i class="{html.escape(icon)} feature-icon"></i>', unsafe_allow_html=True)
        st.subheader(title)
        st.write(description)

def circular_progress_card(title, score, status, color):
    """
    Renders a card with a circular progress bar.
    Uses unsafe_allow_html=True for the complex circular graphic,
    but strictly sanitizes all dynamic inputs to mitigate XSS risk.
    """
    # Sanitize all dynamic inputs
    s_title = html.escape(title)
    s_score = html.escape(str(score))
    s_status = html.escape(status)
    s_color = html.escape(color) # Ensure color is a valid and safe CSS color value

    st.markdown(f"""
    <div class="feature-card">
        <h2>{s_title}</h2>
        <div class="ats-score-container">
            <div class="ats-score-circle" style="background: conic-gradient({s_color} 0% {s_score}%, var(--bg-dark) {s_score}% 100%);">
                <div class="ats-score-inner-circle" style="color: {s_color};">{s_score}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def skills_match_card(keyword_match):
    """
    Renders the Skills Match card using native Streamlit components.
    """
    with st.container(border=True):
        st.subheader("Skills Match")
        st.metric(label="Keyword Match", value=f"{int(keyword_match.get('score', 0))}%")
        if keyword_match.get('missing_skills'):
            st.markdown("#### Missing Skills:")
            for skill in keyword_match['missing_skills']:
                st.markdown(f"- {html.escape(skill)}")

def format_section_card(format_score, section_score):
    """
    Renders the Format & Section Analysis card using native Streamlit components.
    """
    with st.container(border=True):
        st.subheader("Format & Section Analysis")
        st.metric("Format Score", f"{int(format_score)}%")
        st.metric("Section Score", f"{int(section_score)}%")

def suggestions_card(suggestions):
    """
    Renders the Resume Improvement Suggestions card using native Streamlit components.
    """
    with st.container(border=True):
        st.subheader("📋 Resume Improvement Suggestions")
        if suggestions:
            for suggestion in suggestions:
                # Use st.markdown for the icon and text, ensuring sanitization
                # For FontAwesome icons, we still need unsafe_allow_html=True, but content is sanitized
                icon_class = html.escape(suggestion.get('icon', 'fa-check-circle'))
                suggestion_text = html.escape(suggestion.get('text'))
                st.markdown(f"<div class='suggestion-item'><i class='fas {icon_class}'></i> {suggestion_text}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='suggestion-item'><i class='fas fa-star'></i> Your resume looks great! No immediate suggestions.</div>", unsafe_allow_html=True)

def course_recommendations_card(selected_role):
    """
    Renders the Recommended Courses card using native Streamlit components.
    """
    from config.courses import COURSES_BY_CATEGORY, get_courses_for_role, get_category_for_role

    with st.container(border=True):
        st.subheader("📚 Recommended Courses")
        
        courses = get_courses_for_role(selected_role)
        if not courses:
            category = get_category_for_role(selected_role)
            courses = COURSES_BY_CATEGORY.get(category, {}).get(selected_role, [])
        
        if courses:
            cols_courses = st.columns(2)
            for i, course in enumerate(courses[:6]):
                with cols_courses[i % 2]:
                    # Inner course card - still uses unsafe_allow_html for link to external content
                    # but content is sanitized.
                    course_title = html.escape(course[0])
                    course_url = html.escape(course[1])
                    st.markdown(f"""
                    <div class="course-card">
                        <h4>{course_title}</h4>
                        <a href='{course_url}' target='_blank' class="course-link">View Course</a>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No course recommendations available for this role yet.")

def helpful_videos_card():
    """
    Renders the Helpful Videos card using native Streamlit components.
    """
    from config.courses import RESUME_VIDEOS, INTERVIEW_VIDEOS

    with st.container(border=True):
        st.subheader("📺 Helpful Videos")
        
        tab1, tab2 = st.tabs(["Resume Tips", "Interview Tips"])
        
        with tab1:
            for category, videos in RESUME_VIDEOS.items():
                st.markdown(f"**{html.escape(category)}**") # Use markdown for bold category
                cols_videos = st.columns(2)
                for i, video in enumerate(videos):
                    with cols_videos[i % 2]:
                        st.video(video[1])
        
        with tab2:
            for category, videos in INTERVIEW_VIDEOS.items():
                st.markdown(f"**{html.escape(category)}**") # Use markdown for bold category
                cols_videos = st.columns(2)
                for i, video in enumerate(videos):
                    with cols_videos[i % 2]:
                        st.video(video[1])

def profile_section(content, image_path=None, social_links=None):
    """Render a modern about section with profile image and social links"""
    st.markdown("""
        <div class="glass-card about-section">
            <div class="profile-section">
    """, unsafe_allow_html=True)
    
    # Profile Image
    if image_path:
        st.image(image_path, use_column_width=False, width=200)
    
    # Image Upload
    uploaded_file = st.file_uploader("Upload profile picture", type=['png', 'jpg', 'jpeg'])
    if uploaded_file is not None:
        st.image(uploaded_file, use_column_width=False, width=200)
    
    # Social Links
    if social_links:
        st.markdown('<div class="social-links">', unsafe_allow_html=True)
        for platform, url in social_links.items():
            st.markdown(f'<a href="{url}" target="_blank" class="social-link"><i class="fab fa-{platform.lower()}"></i></a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # About Content
    st.markdown(f"""
            </div>
            <div class="about-content">{content}</div>
        </div>
    """, unsafe_allow_html=True)

def metric_card(label, value, delta=None, icon_emoji=None):
    """
    Render a metric card using native Streamlit's st.metric component.
    This provides a secure, maintainable, and responsive way to display metrics.
    Icon is replaced with an emoji in the label for native component compatibility.
    """
    display_label = f"{icon_emoji} {label}" if icon_emoji else label
    st.metric(label=display_label, value=value, delta=delta)

def template_card(title, description, image_url=None):
    """Render a modern template card with glassmorphism effect"""
    image_html = f'<img src="{image_url}" class="template-image" />' if image_url else ''
    
    st.markdown(f"""
        <div class="glass-card template-card">
            {image_html}
            <h3>{title}</h3>
            <p>{description}</p>
            <div class="card-overlay"></div>
        </div>
    """, unsafe_allow_html=True)

def feedback_card(name, feedback, rating):
    """Render a modern feedback card with rating stars"""
    stars = "⭐" * int(rating)
    
    st.markdown(f"""
        <div class="card feedback-card">
            <div class="feedback-header">
                <div class="feedback-name">{name}</div>
                <div class="feedback-rating">{stars}</div>
            </div>
            <p class="feedback-text">{feedback}</p>
        </div>
    """, unsafe_allow_html=True)

def loading_spinner(message="Loading..."):
    """Show a modern loading spinner with message"""
    st.markdown(f"""
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <p class="loading-message">{message}</p>
        </div>
    """, unsafe_allow_html=True)

def progress_bar(value, max_value, label=None):
    """Render a modern animated progress bar"""
    percentage = (value / max_value) * 100
    label_html = f'<div class="progress-label">{label}</div>' if label else ''
    
    st.markdown(f"""
        <div class="progress-container">
            {label_html}
            <div class="progress-bar">
                <div class="progress-fill" style="width: {percentage}%"></div>
            </div>
            <div class="progress-value">{percentage:.1f}%</div>
        </div>
    """, unsafe_allow_html=True)

def tooltip(content, tooltip_text):
    """Render content with a modern tooltip"""
    st.markdown(f"""
        <div class="tooltip" data-tooltip="{tooltip_text}">
            {content}
        </div>
    """, unsafe_allow_html=True)

def data_table(data, headers):
    """Render a modern data table with hover effects"""
    header_row = "".join([f"<th>{header}</th>" for header in headers])
    rows = ""
    for row in data:
        cells = "".join([f"<td>{cell}</td>" for cell in row])
        rows += f"<tr>{cells}</tr>"
    
    st.markdown(f"""
        <div class="table-container">
            <table class="modern-table">
                <thead>
                    <tr>{header_row}</tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
    """, unsafe_allow_html=True)

def grid_layout(*elements):
    """Create a responsive grid layout"""
    st.markdown("""
        <div class="grid">
            {}
        </div>
    """.format("".join(elements)), unsafe_allow_html=True)

def alert(message, type="info"):
    """Display a modern alert message"""
    alert_types = {
        "info": ("ℹ️", "var(--accent-color)"),
        "success": ("✅", "var(--success-color)"),
        "warning": ("⚠️", "var(--warning-color)"),
        "error": ("❌", "var(--error-color)")
    }
    icon, color = alert_types.get(type, alert_types["info"])
    
    st.markdown(f"""
        <div class="alert alert-{type}">
            <span class="alert-icon">{icon}</span>
            <span class="alert-message">{message}</span>
        </div>
    """, unsafe_allow_html=True)

def about_section(title, description, team_members=None):
    st.markdown(f"""
        <div class="about-section">
            <h2>{title}</h2>
            <p class="about-description">{description}</p>
            {generate_team_section(team_members) if team_members else ''}
        </div>
    """, unsafe_allow_html=True)

def generate_team_section(team_members):
    if not team_members:
        return ""
    
    team_html = '<div class="team-section">'
    for member in team_members:
        team_html += f"""
            <div class="team-member">
                <img src="{member['image']}" alt="{member['name']}">
                <h3>{member['name']}</h3>
                <p>{member['role']}</p>
            </div>
        """
    team_html += '</div>'
    return team_html

def render_feedback(feedback_data):
    """Render feedback with modern styling"""
    if not feedback_data:
        return
    
    feedback_html = """
    <div class="feedback-section">
        <h3 class="feedback-header">Resume Analysis Feedback</h3>
        <div class="feedback-content">
    """
    
    for category, items in feedback_data.items():
        if items:  # Only show categories with feedback
            for item in items:
                feedback_html += f"""
                <div class="feedback-item">
                    <div class="feedback-category">{html.escape(category)}</div>
                    <div class="feedback-description">{html.escape(item)}</div>
                </div>
                """
    
    feedback_html += """
        </div>
    </div>
    """
    
    st.markdown(feedback_html, unsafe_allow_html=True)

def render_feedback_form():
    st.markdown("""
        <div class="feedback-header">
            <h1>Your Voice Matters! 🗣️</h1>
            <p>Help us improve Smart Resume AI with your valuable feedback and suggestions.</p>
        </div>
        <div class="feedback-form-container">
    """, unsafe_allow_html=True)

    # Form content will be added here by the feedback manager
    st.markdown("</div>", unsafe_allow_html=True)

def render_feedback_overview():
    st.markdown("""
        <div class="feedback-section">
            <h2 class="feedback-overview-title">Feedback Overview 📊</h2>
        </div>
    """, unsafe_allow_html=True)

def render_analytics_section(resume_uploaded=False, metrics=None):
    """Render the analytics section of the dashboard"""
    if not metrics:
        metrics = {
            'views': 0,
            'downloads': 0,
            'score': 'N/A'
        }
    
    # Views Card
    st.markdown("""
        <div class="analytics-card">
            <div class="analytics-icon">
                <i class='fas fa-eye'></i>
            </div>
            <h2 class="analytics-title">Resume Views</h2>
            <p class="analytics-value">{}</p>
        </div>
    """.format(metrics['views']), unsafe_allow_html=True)
    
    # Downloads Card
    st.markdown("""
        <div class="analytics-card">
            <div class="analytics-icon">
                <i class='fas fa-download'></i>
            </div>
            <h2 class="analytics-title">Downloads</h2>
            <p class="analytics-value">{}</p>
        </div>
    """.format(metrics['downloads']), unsafe_allow_html=True)
    
    # Profile Score Card
    st.markdown("""
        <div class="analytics-card">
            <div class="analytics-icon">
                <i class='fas fa-chart-line'></i>
            </div>
            <h2 class="analytics-title">Profile Score</h2>
            <p class="analytics-value">{}</p>
        </div>
    """.format(metrics['score']), unsafe_allow_html=True)

def render_activity_section(resume_uploaded=False):
    """Render the recent activity section"""
    st.markdown("""
        <div class="activity-section">
            <h2 class="activity-title">
                <i class='fas fa-history activity-icon'></i> Recent Activity
            </h2>
    """, unsafe_allow_html=True)
    
    if resume_uploaded:
        st.markdown("""
            <div class="activity-content">
                <p class="activity-item">• Resume uploaded and analyzed</p>
                <p class="activity-item">• Generated optimization suggestions</p>
                <p class="activity-item">• Updated profile score</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="activity-empty-state">
                <i class='fas fa-upload activity-empty-icon'></i>
                <p class="activity-empty-message">Upload your resume to see activity</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_suggestions_section(resume_uploaded=False):
    """Render the suggestions section"""
    st.markdown("""
        <div class="suggestions-section">
            <h2 class="suggestions-title">
                <i class='fas fa-lightbulb suggestions-icon'></i> Suggestions
            </h2>
    """, unsafe_allow_html=True)
    
    if resume_uploaded:
        st.markdown("""
            <div class="suggestions-content">
                <p class="suggestions-item">• Add more quantifiable achievements</p>
                <p class="suggestions-item">• Include relevant keywords</p>
                <p class="suggestions-item">• Optimize formatting</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="suggestions-empty-state">
                <i class='fas fa-file-alt suggestions-empty-icon'></i>
                <p class="suggestions-empty-message">Upload your resume to get suggestions</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_personal_info_form(personal_info):
    st.subheader("Personal Information")
    col1, col2 = st.columns(2)
    with col1:
        personal_info['full_name'] = st.text_input("Full Name", value=personal_info.get('full_name', ''))
        personal_info['email'] = st.text_input("Email", value=personal_info.get('email', ''), key="email_input")
        st.write("**Phone Number**")
        phone_col1, phone_col2 = st.columns([0.2, 0.2])
        
        # Country codes with country names
        country_options = {
            "🇮🇳 India (+91)": "+91",
            "🇺🇸 USA (+1)": "+1",
            "🇬🇧 UK (+44)": "+44",
            "🇦🇺 Australia (+61)": "+61",
            "🇯🇵 Japan (+81)": "+81",
            "🇨🇳 China (+86)": "+86",
            "🇩🇪 Germany (+49)": "+49",
            "🇫🇷 France (+33)": "+33",
            "🇮🇹 Italy (+39)": "+39",
            "🇪🇸 Spain (+34)": "+34",
            "🇷🇺 Russia (+7)": "+7",
            "🇨🇦 Canada (+1)": "+1",
        }
        
        with phone_col1:
            existing_phone = personal_info.get('phone', '')
            default_country_code = "+91" 
            phone_number_only = existing_phone

            if existing_phone:
                for code in country_options.values():
                    if existing_phone.startswith(code):
                        default_country_code = code
                        phone_number_only = existing_phone[len(code):].strip()
                        break
            
            default_display = "🇮🇳 India (+91)"
            for display, code in country_options.items():
                if code == default_country_code:
                    default_display = display
                    break
            
            selected_country = st.selectbox(
                "Country",
                options=list(country_options.keys()),
                index=list(country_options.keys()).index(default_display) if default_display in country_options.keys() else 0,
                key="country_code_select",
                label_visibility="collapsed"
            )
            
            country_code = country_options[selected_country]
            
        with phone_col2:
            phone_number = st.text_input(
                "Number",
                value=phone_number_only,
                placeholder="Enter phone number",
                key="phone_number_input",
                label_visibility="collapsed"
            )
        
        personal_info['phone'] = f"{country_code} {phone_number}".strip() if phone_number else ""
    with col2:
        personal_info['location'] = st.text_input("Location", value=personal_info.get('location', ''))
        personal_info['linkedin'] = st.text_input("LinkedIn URL", value=personal_info.get('linkedin', ''))
        personal_info['github'] = st.text_input("GitHub URL", value=personal_info.get('github', ''))
    return personal_info

def render_summary_form():
    st.subheader("Professional Summary")

    summary_text = st.text_area("Professional Summary", 
                                value=st.session_state.form_data.get('summary', ''), 
                                height=150,
                                help="Write a brief summary about your professional background.",
                                key="summary_text_area")
    
    st.session_state.form_data['summary'] = summary_text
    return summary_text

def render_experience_form(experiences):
    """Render the work experience form section with enhanced date picker"""
    st.header("💼 Work Experience")
    
    if 'experience_count' not in st.session_state:
        st.session_state.experience_count = len(experiences) if experiences else 1
    
    if st.button("➕ Add Experience", key="add_experience"):
        st.session_state.experience_count += 1
    
    updated_experiences = []
    
    # Month options
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    current_year = datetime.now().year
    years = list(range(current_year - 30, current_year + 2))  # Last 30 years to next year
    
    for i in range(st.session_state.experience_count):
        with st.expander(f"Experience {i+1}", expanded=(i == 0)):
            # Get existing data if available
            existing_exp = experiences[i] if i < len(experiences) else {}
            
            col1, col2 = st.columns(2)
            
            with col1:
                position = st.text_input(
                    "Position/Job Title*",
                    value=existing_exp.get('position', ''),
                    key=f"exp_position_{i}",
                    placeholder="e.g., Software Engineer"
                )
                
                company = st.text_input(
                    "Company Name*",
                    value=existing_exp.get('company', ''),
                    key=f"exp_company_{i}",
                    placeholder="e.g., Google"
                )
                
                location = st.text_input(
                    "Location",
                    value=existing_exp.get('location', ''),
                    key=f"exp_location_{i}",
                    placeholder="e.g., San Francisco, CA"
                )
            
            with col2:
                work_mode = st.selectbox(
                    "Work Mode",
                    options=["On-site", "Remote", "Hybrid"],
                    index=["On-site", "Remote", "Hybrid"].index(existing_exp.get('work_mode', 'On-site')) if existing_exp.get('work_mode') in ["On-site", "Remote", "Hybrid"] else 0,
                    key=f"exp_work_mode_{i}"
                )
                
                
                with col2:
                    st.write("**Start Date**")
                    start_month = st.selectbox(
                        "Month",
                        options=months,
                        index=months.index(existing_exp.get('start_month', 'Jan')) if existing_exp.get('start_month') in months else 0,
                        key=f"exp_start_month_{i}"
                    )
                with col2:
                    start_year = st.selectbox(
                        "Year",
                        options=years,
                        index=years.index(existing_exp.get('start_year', current_year)) if existing_exp.get('start_year') in years else len(years)-1,
                        key=f"exp_start_year_{i}"
                    )
                
            
                with col2:
                    st.write("**End Date**")
                    end_month = st.selectbox(
                        "Month",
                        options=months,
                        index=months.index(existing_exp.get('end_month', 'Dec')) if existing_exp.get('end_month') in months else 11,
                        key=f"exp_end_month_{i}",
                        disabled=existing_exp.get('is_present', False)
                    )
                with col2:
                    end_year = st.selectbox(
                        "Year",
                        options=years,
                        index=years.index(existing_exp.get('end_year', current_year)) if existing_exp.get('end_year') in years else len(years)-1,
                        key=f"exp_end_year_{i}",
                        disabled=existing_exp.get('is_present', False)
                    )
                with col2:
                    st.write("")  # Spacing
                    is_present = st.checkbox(
                        "Present",
                        value=existing_exp.get('is_present', False),
                        key=f"exp_present_{i}"
                    )
            
            # Responsibilities section
            st.write("**Key Responsibilities & Achievements:**")
            st.caption("Use bullet points starting with strong action verbs (Developed, Led, Implemented, etc.)")
            
            # Get existing responsibilities
            existing_responsibilities = existing_exp.get('responsibilities', [''])
            if not existing_responsibilities:
                existing_responsibilities = ['']
            
            # Dynamic responsibility points
            if f'responsibility_count_{i}' not in st.session_state:
                st.session_state[f'responsibility_count_{i}'] = max(len(existing_responsibilities), 3)
            
            responsibilities = []
            for j in range(st.session_state[f'responsibility_count_{i}']):
                resp = st.text_input(
                    f"Point {j+1}",
                    value=existing_responsibilities[j] if j < len(existing_responsibilities) else '',
                    key=f"exp_resp_{i}_{j}",
                    placeholder=f"e.g., Developed Python-based REST APIs, reducing data processing time by 25%"
                )
                if resp.strip():
                    responsibilities.append(resp.strip())
            
            # Add more points button
            if st.button(f"➕ Add More Points", key=f"add_resp_{i}"):
                st.session_state[f'responsibility_count_{i}'] += 1
                st.rerun()
            
            if position and company:
                exp_data = {
                    'position': position,
                    'company': company,
                    'location': location,
                    'work_mode': work_mode,  # ADDED BACK
                    'start_month': start_month,
                    'start_year': start_year,
                    'end_month': end_month if not is_present else '',
                    'end_year': end_year if not is_present else '',
                    'is_present': is_present,
                    'start_date': f"{start_month} {start_year}",
                    'end_date': "Present" if is_present else f"{end_month} {end_year}",
                    'responsibilities': responsibilities
                }
                updated_experiences.append(exp_data)
            
            if st.button(f"🗑️ Remove Experience {i+1}", key=f"remove_exp_{i}"):
                st.session_state.experience_count -= 1
                if f'responsibility_count_{i}' in st.session_state:
                    del st.session_state[f'responsibility_count_{i}']
                st.rerun()
    
    return updated_experiences

def render_projects_form(projects_data):
    """Render the projects form section with enhanced date picker"""
    st.header("💼 Projects")
    
    if 'project_count' not in st.session_state:
        st.session_state.project_count = len(projects_data) if projects_data else 1
    
    if st.button("➕ Add Project", key="add_project"):
        st.session_state.project_count += 1
    
    projects = []
    
    # Month options
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    current_year = datetime.now().year
    years = list(range(current_year - 10, current_year + 2))  # Last 10 years to next year
    
    for i in range(st.session_state.project_count):
        with st.expander(f"Project {i+1}", expanded=(i == 0)):
            # Get existing data if available
            existing_project = projects_data[i] if i < len(projects_data) else {}
            
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input(
                    "Project Name*",
                    value=existing_project.get('name', ''),
                    key=f"project_name_{i}",
                    placeholder="e.g., E-commerce Platform"
                )
                
                technologies = st.text_input(
                    "Technologies Used*",
                    value=existing_project.get('technologies', ''),
                    key=f"project_tech_{i}",
                    placeholder="e.g., React, Node.js, MongoDB"
                )
            
            with col2:
                st.write("**Start Date**")
                with col2:
                    start_month = st.selectbox(
                        "Month",
                        options=months,
                        index=months.index(existing_project.get('start_month', 'Jan')) if existing_project.get('start_month') in months else 0,
                        key=f"proj_start_month_{i}"
                    )
                with col2:
                    start_year = st.selectbox(
                        "Year",
                        options=years,
                        index=years.index(existing_project.get('start_year', current_year)) if existing_project.get('start_year') in years else len(years)-1,
                        key=f"proj_start_year_{i}"
                    )
                
                
                with col2:
                    st.write("**End Date**")
                    end_month = st.selectbox(
                        "Month",
                        options=months,
                        index=months.index(existing_project.get('end_month', 'Dec')) if existing_project.get('end_month') in months else 11,
                        key=f"proj_end_month_{i}",
                        disabled=existing_project.get('is_ongoing', False)
                    )
                with col2:
                    end_year = st.selectbox(
                        "Year",
                        options=years,
                        index=years.index(existing_project.get('end_year', current_year)) if existing_project.get('end_year') in years else len(years)-1,
                        key=f"proj_end_year_{i}",
                        disabled=existing_project.get('is_ongoing', False)
                    )
                with col2:
                    st.write("")  # Spacing
                    is_ongoing = st.checkbox(
                        "Ongoing",
                        value=existing_project.get('is_ongoing', False),
                        key=f"proj_ongoing_{i}"
                    )
            
            # GitHub Link
            github_link = st.text_input(
                "Project GitHub URL",
                value=existing_project.get('github_link', ''),
                key=f"project_github_{i}",
                placeholder="https://github.com/username/project-name"
            )
            
            description = st.text_area(
                "Project Description",
                value=existing_project.get('description', ''),
                key=f"project_desc_{i}",
                placeholder="Brief overview of the project",
                height=80
            )
            
            st.write("**Key Achievements/Features:**")
            st.caption("Highlight technical implementation, challenges solved, and impact")
            
            # Get existing key points
            existing_points = existing_project.get('key_points', [''])
            if not existing_points:
                existing_points = ['']
            
            # Dynamic key points
            if f'project_point_count_{i}' not in st.session_state:
                st.session_state[f'project_point_count_{i}'] = max(len(existing_points), 3)
            
            key_points = []
            for j in range(st.session_state[f'project_point_count_{i}']):
                point = st.text_input(
                    f"Point {j+1}",
                    value=existing_points[j] if j < len(existing_points) else '',
                    key=f"project_point_{i}_{j}",
                    placeholder=f"e.g., Implemented user authentication using JWT, supporting 10,000+ users"
                )
                if point.strip():
                    key_points.append(point.strip())
            
            # Add more points button
            if st.button(f"➕ Add More Points", key=f"add_proj_point_{i}"):
                st.session_state[f'project_point_count_{i}'] += 1
                st.rerun()
            
            if name and technologies:
                project_data = {
                    'name': name,
                    'technologies': technologies,
                    'start_month': start_month,
                    'start_year': start_year,
                    'end_month': end_month if not is_ongoing else '',
                    'end_year': end_year if not is_ongoing else '',
                    'is_ongoing': is_ongoing,
                    'start_date': f"{start_month} {start_year}",
                    'end_date': "Present" if is_ongoing else f"{end_month} {end_year}",
                    'github_link': github_link,
                    'description': description,
                    'key_points': key_points
                }
                projects.append(project_data)
            
            if st.button(f"🗑️ Remove Project {i+1}", key=f"remove_project_{i}"):
                st.session_state.project_count -= 1
                if f'project_point_count_{i}' in st.session_state:
                    del st.session_state[f'project_point_count_{i}']
                st.rerun()
    
    return projects

def render_education_form(education):
    st.subheader("Education")
    if st.button("Add Education"):
        education.append({
            'school': '',
            'degree': '',
            'field': '',
            'graduation_date': '',
            'gpa': '',
            'achievements': []
        })
        st.session_state.form_data['education'] = education
        st.rerun()

    for idx, edu in enumerate(education):
        with st.expander(f"Education {idx + 1}", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                edu['school'] = st.text_input("School/University", key=f"school_{idx}", value=edu.get('school', ''))
                edu['degree'] = st.text_input("Degree", key=f"degree_{idx}", value=edu.get('degree', ''))
            with col2:
                edu['field'] = st.text_input("Field of Study", key=f"field_{idx}", value=edu.get('field', ''))
                edu['graduation_date'] = st.text_input("Graduation Date", key=f"grad_date_{idx}", 
                                                     value=edu.get('graduation_date', ''))
            
            edu['gpa'] = st.text_input("GPA (optional)", key=f"gpa_{idx}", value=edu.get('gpa', ''))
            
            st.markdown("##### Achievements & Activities")
            edu_achv_text = st.text_area("Enter achievements (one per line)", 
                                       key=f"edu_achv_{idx}",
                                       value='\n'.join(edu.get('achievements', [])),
                                       height=100,
                                       help="List academic achievements, relevant coursework, or activities")
            edu['achievements'] = [a.strip() for a in edu_achv_text.split('\n') if a.strip()]
            
            if st.button("Remove Education", key=f"remove_edu_{idx}"):
                education.pop(idx)
                st.session_state.form_data['education'] = education
                st.rerun()
    return education

def render_skills_form(skills_categories):
    """Render skills form without certifications"""
    st.subheader("Skills")
    
    # Updated skill categories (removed certifications)
    skill_categories_config = {
        'programming_languages': 'Programming Languages',
        'frameworks_libraries': 'Frameworks & Libraries',
        'developer_tools': 'Developer Tools',
        'databases': 'Databases',
        'cloud_devops': 'Cloud & DevOps'
    }
    
    # Initialize skills_categories if it's not already in a dictionary format
    if not isinstance(skills_categories, dict):
        skills_categories = {key: [] for key in skill_categories_config.keys()}

    # Create two columns for the layout
    col1, col2 = st.columns(2)
    
    # Split the categories between the two columns
    categories_list = list(skill_categories_config.items())
    mid_point = (len(categories_list) + 1) // 2
    
    with col1:
        for key, label in categories_list[:mid_point]:
            skills_text = st.text_area(label, 
                                     value='\n'.join(skills_categories.get(key, [])),
                                     height=120,
                                     key=f"skills_{key}")
            skills_categories[key] = [s.strip() for s in skills_text.split('\n') if s.strip()]
            
    with col2:
        for key, label in categories_list[mid_point:]:
            skills_text = st.text_area(label, 
                                     value='\n'.join(skills_categories.get(key, [])),
                                     height=120,
                                     key=f"skills_{key}")
            skills_categories[key] = [s.strip() for s in skills_text.split('\n') if s.strip()]
            
    return skills_categories

def render_certifications_form(certifications_data):
    """Render the new Certifications & Achievements section"""
    st.header("🏆 Certifications & Achievements")
    st.caption("Add certifications with verification links for ATS optimization")
    
    if 'certification_count' not in st.session_state:
        st.session_state.certification_count = len(certifications_data) if certifications_data else 1
    
    if st.button("➕ Add Certification/Achievement", key="add_cert"):
        st.session_state.certification_count += 1
    
    certifications = []
    
    # Month options for issue date
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    current_year = datetime.now().year
    years = list(range(current_year - 10, current_year + 2))
    
    for i in range(st.session_state.certification_count):
        with st.expander(f"Certification/Achievement {i+1}", expanded=(i == 0)):
            # Get existing data if available
            existing_cert = certifications_data[i] if i < len(certifications_data) else {}
            
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input(
                    "Certification/Achievement Name*",
                    value=existing_cert.get('name', ''),
                    key=f"cert_name_{i}",
                    placeholder="e.g., AWS Certified Solutions Architect – Associate"
                )
                
                issuer = st.text_input(
                    "Issuing Organization",
                    value=existing_cert.get('issuer', ''),
                    key=f"cert_issuer_{i}",
                    placeholder="e.g., Amazon Web Services"
                )
            
            with col2:
                st.write("**Issue Date**")
                col_month, col_year = st.columns(2)
                with col_month:
                    issue_month = st.selectbox(
                        "Month",
                        options=months,
                        index=months.index(existing_cert.get('issue_month', 'Jan')) if existing_cert.get('issue_month') in months else 0,
                        key=f"cert_month_{i}"
                    )
                with col_year:
                    issue_year = st.selectbox(
                        "Year",
                        options=years,
                        index=years.index(existing_cert.get('issue_year', current_year)) if existing_cert.get('issue_year') in years else len(years)-1,
                        key=f"cert_year_{i}"
                    )
                
                credential_id = st.text_input(
                    "Credential ID (optional)",
                    value=existing_cert.get('credential_id', ''),
                    key=f"cert_cred_{i}",
                    placeholder="e.g., ABC123XYZ"
                )
            
            verification_url = st.text_input(
                "Verification URL (optional)",
                value=existing_cert.get('verification_url', ''),
                key=f"cert_url_{i}",
                placeholder="https://www.credly.com/badges/..."
            )
            
            if name:
                cert_data = {
                    'name': name,
                    'issuer': issuer,
                    'issue_month': issue_month,
                    'issue_year': issue_year,
                    'issue_date': f"{issue_month} {issue_year}",
                    'credential_id': credential_id,
                    'verification_url': verification_url
                }
                certifications.append(cert_data)
            
            if st.button(f"🗑️ Remove Certification {i+1}", key=f"remove_cert_{i}"):
                st.session_state.certification_count -= 1
                st.rerun()
    
    return certifications

def render_sidebar(pages, load_lottie_url, is_admin, current_admin_email, verify_admin, log_admin_action, is_logged_in, user_email):
    with st.sidebar:
        # Custom CSS for sidebar styling is now in style/style.css

        st_lottie(load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_xyadoh9h.json"), height=180, key="sidebar_animation")
        st.markdown('<div class="sidebar-header">Smart Resume AI</div>', unsafe_allow_html=True)
        st.markdown("---")
        
        # Navigation buttons
        st.markdown("### 🧭 Menu")
        
        # Filter pages based on authentication status
        if is_logged_in or is_admin:
            pages_to_show = {k: v for k, v in pages.items() if k not in ["🔑 SIGN IN", "📝 SIGN UP"]}
        else:
            pages_to_show = {k: v for k, v in pages.items() if k not in ["📊 DASHBOARD"]}


        for page_name in pages_to_show.keys():
            if st.button(page_name, width='stretch', key=f"nav_btn_{page_name}"):
                st.session_state.page = clean_page_name(page_name)
                st.rerun()

        # Add some space before login/logout
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Admin Login/Logout section at bottom
        if is_admin:
            st.success(f"👤 {current_admin_email}")
            if st.button("🚪 Logout", key="logout_button", type="primary"):
                try:
                    log_admin_action(current_admin_email, "logout")
                    st.session_state.is_admin = False
                    st.session_state.current_admin_email = None
                    st.success("Logged out")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        # User Login/Logout section
        elif is_logged_in:
            st.success(f"👤 {user_email}")
            if st.button("🚪 Sign Out", key="signout_button", type="primary"):
                st.session_state.is_logged_in = False
                st.session_state.user_email = None
                st.success("Signed out successfully!")
                st.rerun()

        else:
            with st.expander("🔐 Admin Access"):
                admin_email_input = st.text_input("Email", key="admin_email_input")
                admin_password = st.text_input("Password", type="password", key="admin_password_input")
                if st.button("Login", key="login_button", type="primary"):
                        try:
                            if verify_admin(admin_email_input, admin_password):
                                st.session_state.is_admin = True
                                st.session_state.current_admin_email = admin_email_input
                                log_admin_action(admin_email_input, "login")
                                st.success("Welcome back!")
                                st.rerun()
                            else:
                                st.error("Invalid credentials")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                            
        st.markdown('<div class="sidebar-footer">© 2026 Smart Resume AI<br>v1.0.0</div>', unsafe_allow_html=True)