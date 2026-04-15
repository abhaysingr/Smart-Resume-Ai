import streamlit as st
import traceback
from config.database import save_resume_data
from ui_components import (
    render_personal_info_form, render_summary_form,
    render_experience_form, render_projects_form, 
    render_education_form, render_skills_form,
    render_certifications_form  # ADD THIS IMPORT
)
from utils.logger import setup_logger
from services.latex_generator import generate_latex_resume

logger = setup_logger(__name__)

def render_builder(builder):
    st.title("Resume Builder 📝")
    st.write("Create your professional resume")
    
    # Job Role Input Section
    st.subheader("🎯 Target Job Role")
    job_role = st.text_input(
        "What job role are you applying for?",
        placeholder="e.g., Software Engineer, Data Scientist, Frontend Developer, etc.",
        help="This helps tailor your resume to the specific role"
    )
    
    # Template selection
    st.subheader("🎨 Resume Template")
    template_options = ["ATS-Friendly", "Modern", "Professional", "Minimal", "Creative"]
    selected_template = st.selectbox("Select Resume Template", template_options)
    st.success(f"🎨 Currently using: {selected_template} Template")

    # Personal Information
    st.session_state.form_data['personal_info'] = render_personal_info_form(st.session_state.form_data['personal_info'])

    # Professional Summary
    st.session_state.form_data['summary'] = render_summary_form()

    # Skills Section
    st.session_state.form_data['skills_categories'] = render_skills_form(st.session_state.form_data['skills_categories'])
    
    # Experience Section
    st.session_state.form_data['experiences'] = render_experience_form(st.session_state.form_data['experiences'])
    
    # Projects Section
    st.session_state.form_data['projects'] = render_projects_form(st.session_state.form_data['projects'])
    
    # Education Section
    st.session_state.form_data['education'] = render_education_form(st.session_state.form_data['education'])
    
    
    # Certifications Section (NEW - ADD THIS)
    if 'certifications' not in st.session_state.form_data:
        st.session_state.form_data['certifications'] = []
    st.session_state.form_data['certifications'] = render_certifications_form(st.session_state.form_data['certifications'])
    
    # Update form data in session state
    st.session_state.form_data.update({
        'summary': st.session_state.form_data['summary']
    })
    
    # Generate Resume button
    if st.button("Generate Resume 📄", type="primary"):
        logger.info("Validating form data...")
        logger.debug(f"Session state form data: {st.session_state.form_data}")
        
        # Get the current values from form
        current_name = st.session_state.form_data['personal_info']['full_name'].strip()
        current_email = st.session_state.email_input if 'email_input' in st.session_state else ''
        
        logger.info(f"Generating resume for: {current_name}")
        
        # Validate required fields
        if not current_name:
            st.error("⚠️ Please enter your full name.")
            return
        
        if not current_email:
            st.error("⚠️ Please enter your email address.")
            return
        
        if not job_role or not job_role.strip():
            st.error("⚠️ Please enter the job role you are applying for.")
            return
            
        # Update email in form data one final time
        st.session_state.form_data['personal_info']['email'] = current_email
        
        # Show progress
        with st.spinner(f'🤖 Generating {selected_template} resume for {job_role} role with AI...'):
            try:
                logger.info("Preparing resume data...")
                # Prepare resume data with current form values
                resume_data = {
                    "personal_info": st.session_state.form_data['personal_info'],
                    "summary": st.session_state.form_data.get('summary', '').strip(),
                    "experience": st.session_state.form_data.get('experiences', []),
                    "education": st.session_state.form_data.get('education', []),
                    "projects": st.session_state.form_data.get('projects', []),
                    "skills": st.session_state.form_data.get('skills_categories', {}),
                    "certifications": st.session_state.form_data.get('certifications', []),  # ADD THIS
                    "template": selected_template,
                    "job_role": job_role.strip(),
                    "experience_type": "professional"
                }
                
                logger.debug(f"Resume data prepared: {resume_data}")
                
                try:
                    # Generate LaTeX code using Groq API
                    st.info(f"🎨 Generating {selected_template} resume tailored for {job_role} role...")
                    latex_code = generate_latex_resume(resume_data, selected_template, job_role.strip())
                    
                    logger.info("LaTeX code received from Groq")
                    
                    # Store LaTeX code in session state for preview/download
                    st.session_state['generated_latex'] = latex_code
                    st.session_state['job_role'] = job_role.strip()
                    
                    # Save to database
                    try:
                        resume_id = save_resume_data(resume_data)
                        logger.info("Resume data saved to database")
                        
                        if resume_id:
                            with st.spinner("📊 Analyzing ATS compatibility..."):
                                from services.latex_generator import generate_ats_score
                                from config.database import save_analysis_data
                                analysis_dict = generate_ats_score(resume_data, job_role.strip())
                                if analysis_dict:
                                    save_analysis_data(resume_id, analysis_dict)
                                    logger.info("ATS Analysis saved to database")
                                    
                    except Exception as db_error:
                        logger.warning(f"Failed to save to database: {str(db_error)}")
                    
                    # Success message
                    st.success(f"✅ Resume generated successfully for {job_role} role with Groq AI!")
                    
                    # Display LaTeX code in an expander
                    with st.expander("📝 View Generated LaTeX Code"):
                        st.code(latex_code, language='latex')
                    
                    # Download button for LaTeX file
                    st.download_button(
                        label="Download LaTeX Code (.tex) 📥",
                        data=latex_code,
                        file_name=f"{current_name.replace(' ', '_')}_{job_role.replace(' ', '_')}_resume.tex",
                        mime="text/plain"
                    )
                    
                    st.info("💡 Tip: You can compile this LaTeX code using Overleaf or a local LaTeX compiler to generate a PDF.")
                    
                except Exception as groq_error:
                    logger.error(f"Error calling Groq API: {str(groq_error)}", exc_info=True)
                    st.error(f"❌ Error generating resume with Groq: {str(groq_error)}")
                    st.info("Please check your GROQ_API_KEY in the .env file")
                        
            except Exception as e:
                logger.error(f"Error preparing resume data: {str(e)}", exc_info=True)
                st.error(f"❌ Error preparing resume data: {str(e)}")