import streamlit as st
from ui_components import page_header
from utils.generative_ai import generate_cover_letter
import time

def render_cover_letter_page():
    """
    Renders the page for generating a cover letter.
    """
    page_header("Cover Letter Generator", "Create a tailored cover letter in seconds.")

    st.markdown("This tool will help you generate a professional cover letter tailored to a specific job. Simply provide the job description and some details, and let the AI do the rest.")

    # Get user's resume data from session state (populated by builder)
    resume_data = st.session_state.get('form_data', {})

    if not resume_data.get('personal_info', {}).get('full_name'):
        st.warning("Your personal information is missing. Please fill out the Resume Builder first to generate a more personalized cover letter.")

    with st.form("cover_letter_form"):
        company_name = st.text_input("Company Name", placeholder="e.g., Google")
        job_description = st.text_area("Job Description", placeholder="Paste the full job description here...", height=250)
        
        submitted = st.form_submit_button("Generate Cover Letter")

    if submitted:
        if not company_name or not job_description:
            st.error("Please provide both the company name and the job description.")
        else:
            with st.spinner("Writing a draft for you..."):
                try:
                    generated_letter = generate_cover_letter(resume_data, job_description, company_name)
                    
                    st.subheader("Your Generated Cover Letter")
                    st.markdown("---")
                    
                    # Display the letter with a copy button
                    st.text_area("Cover Letter", generated_letter, height=500)
                    st.download_button(
                        label="Download as .txt",
                        data=generated_letter,
                        file_name=f"cover_letter_{company_name}.txt",
                        mime="text/plain"
                    )

                except Exception as e:
                    st.error(f"An error occurred: {e}")