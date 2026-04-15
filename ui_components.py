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
    
    if st.button("➕ Add Experience", key="add_experience"):
        experiences.append({
            'position': '', 'company': '', 'location': '', 'work_mode': 'On-site',
            'start_month': 'Jan', 'start_year': datetime.now().year,
            'end_month': 'Dec', 'end_year': datetime.now().year,
            'is_present': False, 'responsibilities': ['']
        })
        st.rerun()

    # Month options
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    current_year = datetime.now().year
    years = list(range(current_year - 30, current_year + 2))  # Last 30 years to next year
    
    for i, exp in enumerate(experiences):
        with st.expander(f"Experience {i+1}", expanded=(i == len(experiences) - 1)):
            col1, col2 = st.columns(2)
            
            with col1:
                exp['position'] = st.text_input(
                    "Position/Job Title*",
                    value=exp.get('position', ''),
                    key=f"exp_position_{i}",
                    placeholder="e.g., Software Engineer"
                )
                
                exp['company'] = st.text_input(
                    "Company Name*",
                    value=exp.get('company', ''),
                    key=f"exp_company_{i}",
                    placeholder="e.g., Google"
                )
                
                exp['location'] = st.text_input(
                    "Location",
                    value=exp.get('location', ''),
                    key=f"exp_location_{i}",
                    placeholder="e.g., San Francisco, CA"
                )
            
            with col2:
                exp['work_mode'] = st.selectbox(
                    "Work Mode",
                    options=["On-site", "Remote", "Hybrid"],
                    index=["On-site", "Remote", "Hybrid"].index(exp.get('work_mode', 'On-site')) if exp.get('work_mode') in ["On-site", "Remote", "Hybrid"] else 0,
                    key=f"exp_work_mode_{i}"
                )
                
                st.write("**Start Date**")
                start_month_col, start_year_col = st.columns(2)
                with start_month_col:
                    exp['start_month'] = st.selectbox("Month", months, index=months.index(exp.get('start_month', 'Jan')), key=f"exp_start_month_{i}")
                with start_year_col:
                    exp['start_year'] = st.selectbox("Year", years, index=years.index(exp.get('start_year', current_year)), key=f"exp_start_year_{i}")

                st.write("**End Date**")
                end_month_col, end_year_col = st.columns(2)
                with end_month_col:
                    exp['end_month'] = st.selectbox("Month", months, index=months.index(exp.get('end_month', 'Dec')), key=f"exp_end_month_{i}", disabled=exp.get('is_present', False))
                with end_year_col:
                    exp['end_year'] = st.selectbox("Year", years, index=years.index(exp.get('end_year', current_year)), key=f"exp_end_year_{i}", disabled=exp.get('is_present', False))
                
                exp['is_present'] = st.checkbox("Present", value=exp.get('is_present', False), key=f"exp_present_{i}")

            st.write("**Key Responsibilities & Achievements:**")
            st.caption("Use bullet points starting with strong action verbs (Developed, Led, Implemented, etc.)")
            
            if f'responsibility_count_{i}' not in st.session_state:
                st.session_state[f'responsibility_count_{i}'] = max(len(exp.get('responsibilities', [''])), 1)

            # Ensure responsibilities list has enough empty strings
            while len(exp.get('responsibilities', [])) < st.session_state[f'responsibility_count_{i}']:
                exp.setdefault('responsibilities', []).append('')

            temp_resps = []
            for j in range(st.session_state[f'responsibility_count_{i}']):
                resp_text = st.text_input(f"Point {j+1}", value=exp['responsibilities'][j], key=f"exp_resp_{i}_{j}")
                if resp_text.strip():
                    temp_resps.append(resp_text.strip())
            exp['responsibilities'] = temp_resps
            
            if st.button(f"➕ Add More Points", key=f"add_resp_{i}"):
                st.session_state[f'responsibility_count_{i}'] += 1
                st.rerun()

            if st.button(f"🗑️ Remove Experience {i+1}", key=f"remove_exp_{i}"):
                experiences.pop(i)
                st.rerun()
            
            # Update derived fields
            exp['start_date'] = f"{exp['start_month']} {exp['start_year']}"
            exp['end_date'] = "Present" if exp['is_present'] else f"{exp['end_month']} {exp['end_year']}"

    return experiences

def render_projects_form(projects_data):
    """Render the projects form section with enhanced date picker"""
    st.header("💼 Projects")
    
    if st.button("➕ Add Project", key="add_project"):
        projects_data.append({
            'name': '', 'technologies': '', 'start_month': 'Jan', 'start_year': datetime.now().year,
            'end_month': 'Dec', 'end_year': datetime.now().year, 'is_ongoing': False,
            'github_link': '', 'description': '', 'key_points': ['']
        })
        st.rerun()

    # Month options
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    current_year = datetime.now().year
    years = list(range(current_year - 10, current_year + 2))  # Last 10 years to next year
    
    for i, proj in enumerate(projects_data):
        with st.expander(f"Project {i+1}", expanded=(i == len(projects_data) - 1)):
            col1, col2 = st.columns(2)
            
            with col1:
                proj['name'] = st.text_input("Project Name*", value=proj.get('name', ''), key=f"project_name_{i}")
                proj['technologies'] = st.text_input("Technologies Used*", value=proj.get('technologies', ''), key=f"project_tech_{i}")

            with col2:
                st.write("**Start Date**")
                start_month_col, start_year_col = st.columns(2)
                with start_month_col:
                    proj['start_month'] = st.selectbox("Month", months, index=months.index(proj.get('start_month', 'Jan')), key=f"proj_start_month_{i}")
                with start_year_col:
                    proj['start_year'] = st.selectbox("Year", years, index=years.index(proj.get('start_year', current_year)), key=f"proj_start_year_{i}")
                
                st.write("**End Date**")
                end_month_col, end_year_col = st.columns(2)
                with end_month_col:
                    proj['end_month'] = st.selectbox("Month", months, index=months.index(proj.get('end_month', 'Dec')), key=f"proj_end_month_{i}", disabled=proj.get('is_ongoing', False))
                with end_year_col:
                    proj['end_year'] = st.selectbox("Year", years, index=years.index(proj.get('end_year', current_year)), key=f"proj_end_year_{i}", disabled=proj.get('is_ongoing', False))

                proj['is_ongoing'] = st.checkbox("Ongoing", value=proj.get('is_ongoing', False), key=f"proj_ongoing_{i}")

            proj['github_link'] = st.text_input("Project GitHub URL", value=proj.get('github_link', ''), key=f"project_github_{i}")
            proj['description'] = st.text_area("Project Description", value=proj.get('description', ''), key=f"project_desc_{i}", height=80)
            
            st.write("**Key Achievements/Features:**")
            if f'project_point_count_{i}' not in st.session_state:
                st.session_state[f'project_point_count_{i}'] = max(len(proj.get('key_points', [''])), 1)
            
            while len(proj.get('key_points', [])) < st.session_state[f'project_point_count_{i}']:
                proj.setdefault('key_points', []).append('')

            temp_points = []
            for j in range(st.session_state[f'project_point_count_{i}']):
                point = st.text_input(f"Point {j+1}", value=proj['key_points'][j], key=f"project_point_{i}_{j}")
                if point.strip():
                    temp_points.append(point.strip())
            proj['key_points'] = temp_points
            
            if st.button(f"➕ Add More Points", key=f"add_proj_point_{i}"):
                st.session_state[f'project_point_count_{i}'] += 1
                st.rerun()

            if st.button(f"🗑️ Remove Project {i+1}", key=f"remove_project_{i}"):
                projects_data.pop(i)
                st.rerun()

            # Update derived fields
            proj['start_date'] = f"{proj['start_month']} {proj['start_year']}"
            proj['end_date'] = "Present" if proj['is_ongoing'] else f"{proj['end_month']} {proj['end_year']}"

    return projects_data

def render_education_form(education):
    st.subheader("Education")
    
    current_year = datetime.now().year
    years = list(range(current_year - 50, current_year + 5)) # A wider range for education years

    if st.button("Add Education"):
        education.append({
            'school': '',
            'degree': '',
            'field': '',
            'start_year': '',
            'end_year': '',
            'is_present': False,
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
                edu['field'] = st.text_input("Field of Study", key=f"field_{idx}", value=edu.get('field', ''))
            with col2:
                st.write("**Start Year**")
                edu['start_year'] = st.selectbox(
                    "Year",
                    options=years,
                    index=years.index(edu.get('start_year', current_year)) if edu.get('start_year') in years else len(years)-1,
                    key=f"edu_start_year_{idx}",
                    label_visibility="collapsed"
                )
                
                st.write("**End Year**")
                edu['end_year'] = st.selectbox(
                    "Year",
                    options=years,
                    index=years.index(edu.get('end_year', current_year)) if edu.get('end_year') in years else len(years)-1,
                    key=f"edu_end_year_{idx}",
                    disabled=edu.get('is_present', False),
                    label_visibility="collapsed"
                )
                
                edu['is_present'] = st.checkbox(
                    "Currently pursuing",
                    value=edu.get('is_present', False),
                    key=f"edu_is_present_{idx}"
                )
            
            edu['gpa'] = st.text_input("GPA/Percentage (optional)", key=f"gpa_{idx}", value=edu.get('gpa', ''))
            
            st.markdown("##### Achievements & Activities (optional)")
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
                
                # Delete persistent cookie
                if 'cookie_controller' in st.session_state:
                    st.session_state.cookie_controller.remove('auth_token')
                
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
