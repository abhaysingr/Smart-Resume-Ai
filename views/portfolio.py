import streamlit as st
from ui_components import page_header

def render_portfolio_page():
    """
    Renders a beautiful, modern web portfolio based on the user's project data.
    """

    # Get data from session state
    personal_info = st.session_state.form_data.get('personal_info', {})
    projects = st.session_state.form_data.get('projects', [])
    skills = st.session_state.form_data.get('skills', [])
    
    # --- Custom CSS for Enhanced Styling ---
    st.markdown("""
    <style>
        /* Hero Section */
        .hero-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 60px 20px;
            border-radius: 20px;
            margin-bottom: 40px;
            text-align: center;
            color: white;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            animation: fadeInDown 0.8s ease-out;
        }
        
        .hero-title {
            font-size: 3.5em;
            font-weight: 800;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .hero-subtitle {
            font-size: 1.3em;
            opacity: 0.95;
            margin-bottom: 30px;
        }
        
        /* Contact Links */
        .contact-container {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin: 30px 0;
            flex-wrap: wrap;
        }
        
        .contact-link {
            background: white;
            color: #667eea;
            padding: 12px 25px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        
        .contact-link:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 25px rgba(0,0,0,0.2);
            background: #f8f9fa;
        }
        
        /* Skills Section */
        .skills-container {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin: 20px 0;
            justify-content: center;
        }
        
        .skill-badge {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: 600;
            font-size: 0.95em;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            transition: all 0.3s ease;
            animation: fadeIn 0.5s ease-out;
        }
        
        .skill-badge:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
        }
        
        /* Project Cards */
        .project-card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 25px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            transition: all 0.4s ease;
            border: 1px solid #e8e8e8;
            position: relative;
            overflow: hidden;
            animation: fadeInUp 0.6s ease-out;
        }
        
        .project-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        }
        
        .project-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        }
        
        .project-title {
            font-size: 1.8em;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .project-tech {
            background: #f7fafc;
            padding: 8px 15px;
            border-radius: 8px;
            margin: 15px 0;
            border-left: 4px solid #667eea;
            font-size: 0.95em;
            color: #4a5568;
        }
        
        .project-description {
            color: #4a5568;
            line-height: 1.7;
            margin: 15px 0;
            font-size: 1.05em;
        }
        
        .project-link-btn {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 30px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            margin-top: 15px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .project-link-btn:hover {
            transform: translateX(5px);
            box-shadow: 0 6px 25px rgba(102, 126, 234, 0.5);
            color: white;
            text-decoration: none;
        }
        
        /* Section Headers */
        .section-header {
            text-align: center;
            margin: 50px 0 30px 0;
            position: relative;
        }
        
        .section-title {
            font-size: 2.5em;
            font-weight: 800;
            color: #2d3748;
            margin-bottom: 10px;
        }
        
        .section-underline {
            width: 80px;
            height: 4px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            margin: 10px auto;
            border-radius: 2px;
        }
        
        /* Animations */
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            background: #f7fafc;
            border-radius: 15px;
            margin: 40px 0;
        }
        
        .empty-state-icon {
            font-size: 4em;
            margin-bottom: 20px;
        }
        
        .empty-state-text {
            font-size: 1.2em;
            color: #718096;
            line-height: 1.6;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .hero-title {
                font-size: 2.5em;
            }
            .contact-container {
                flex-direction: column;
                gap: 15px;
            }
            .project-card {
                padding: 20px;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # --- Hero Section ---
    full_name = personal_info.get('full_name', 'My Portfolio')
    bio = personal_info.get('bio', 'Welcome to my portfolio! Explore my projects and skills.')
    
    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-title">{full_name}</div>
        <div class="hero-subtitle">{bio}</div>
    </div>
    """, unsafe_allow_html=True)

    # --- Contact Links Section ---
    contact_links = []
    if personal_info.get('email'):
        contact_links.append(f'<a href="mailto:{personal_info["email"]}" class="contact-link">📧 Email</a>')
    if personal_info.get('linkedin'):
        contact_links.append(f'<a href="{personal_info["linkedin"]}" target="_blank" class="contact-link">💼 LinkedIn</a>')
    if personal_info.get('github'):
        contact_links.append(f'<a href="{personal_info["github"]}" target="_blank" class="contact-link">💻 GitHub</a>')
    if personal_info.get('portfolio'):
        contact_links.append(f'<a href="{personal_info["portfolio"]}" target="_blank" class="contact-link">🌐 Website</a>')
    
    if contact_links:
        st.markdown(f"""
        <div class="contact-container">
            {''.join(contact_links)}
        </div>
        """, unsafe_allow_html=True)

    # --- Skills Section ---
    if skills:
        st.markdown("""
        <div class="section-header">
            <div class="section-title">Skills & Technologies</div>
            <div class="section-underline"></div>
        </div>
        """, unsafe_allow_html=True)
        
        skills_html = ''.join([f'<div class="skill-badge">{skill}</div>' for skill in skills])
        st.markdown(f'<div class="skills-container">{skills_html}</div>', unsafe_allow_html=True)

    # --- Projects Section ---
    st.markdown("""
    <div class="section-header">
        <div class="section-title">Featured Projects</div>
        <div class="section-underline"></div>
    </div>
    """, unsafe_allow_html=True)

    if not projects:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">🚀</div>
            <div class="empty-state-text">
                <strong>No projects yet!</strong><br>
                Head over to the Resume Builder to add your amazing projects,<br>
                and they'll appear here in all their glory.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Display projects in a beautiful grid
    for i, proj in enumerate(projects):
        project_name = proj.get('name', 'Unnamed Project')
        project_tech = proj.get('technologies', 'N/A')
        project_desc = proj.get('description', 'No description available.')
        project_link = proj.get('link', '#')
        
        st.markdown(f"""
        <div class="project-card">
            <div class="project-title">
                🎯 {project_name}
            </div>
            <div class="project-tech">
                <strong>🛠️ Technologies:</strong> {project_tech}
            </div>
            <div class="project-description">
                {project_desc}
            </div>
            <a href="{project_link}" target="_blank" class="project-link-btn">
                View Project →
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # Add spacing between projects
        if i < len(projects) - 1:
            st.markdown("<br>", unsafe_allow_html=True)

    # --- Footer ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 30px; color: #718096; border-top: 2px solid #e2e8f0; margin-top: 50px;">
        <p style="font-size: 1.1em;">✨ Built with passion and code ✨</p>
        <p style="font-size: 0.9em; margin-top: 10px;">© 2026 {name}. All rights reserved.</p>
    </div>
    """.replace("{name}", full_name), unsafe_allow_html=True)