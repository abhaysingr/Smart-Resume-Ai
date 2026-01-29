import streamlit as st
import time
import PyPDF2
from docx import Document
from groq import Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Page config
st.set_page_config(
    page_title="Smart Resume AI - ATS Optimizer",
    page_icon="📄",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .score-card {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .score-before {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
    }
    .score-after {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF"""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(docx_file):
    """Extract text from DOCX"""
    doc = Document(docx_file)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

def analyze_and_optimize_resume(resume_text, job_description):
    """Use Groq to analyze ATS score and optimize resume"""
    
    prompt = f"""You are an expert ATS (Applicant Tracking System) analyzer and resume optimizer.

JOB DESCRIPTION:
{job_description}

CURRENT RESUME:
{resume_text}

Please provide a detailed analysis in the following format:

**📊 CURRENT ATS SCORE ANALYSIS**

Resume Evaluated: [Extract candidate name] - [Extract target role from job description]

✅ STRENGTHS (ATS-Friendly):
- [List 4-5 specific strengths with keywords found]

❌ GAPS AFFECTING ATS SCORE:
- [List 4-5 specific missing keywords and gaps]

🎯 Current ATS Score: [Score]/100

---

**🚀 OPTIMIZED ATS RESUME**

[Provide a complete, professionally formatted resume with:
- All sections (Contact, Summary, Skills, Experience, Projects, Education)
- Job-description-aligned keywords naturally integrated
- ATS-friendly structure
- Keep all factual information accurate]

---

**📈 IMPROVED ATS SCORE**

✅ Optimized ATS Score: [New Score]/100

Why it increased:
- [List 4 key improvements made]

Be detailed and professional. Format the resume sections clearly."""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Best free model
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert ATS analyzer and resume writer. Provide detailed, actionable analysis."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        st.error(f"Error with Groq API: {str(e)}")
        return None

def render_ats_optimizer():
    # Main App
    if 'analysis_done' not in st.session_state:
        st.session_state.analysis_done = False
        st.session_state.result = None

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Smart Resume AI</h1>
        <p>ATS Score Analysis + Resume Optimization Powered by AI</p>
    </div>
    """, unsafe_allow_html=True)

    # Input Section (only show if analysis not done)
    if not st.session_state.analysis_done:
        st.markdown("### 📝 Step 1: Provide Job Details")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📋 Job Description")
            job_description = st.text_area(
                "Paste the complete job description here",
                height=300,
                placeholder="Job Title: Software Engineer\nLocation: Remote\nExperience: Fresher / 0–1 Year\n\nResponsibilities:\n- Develop, test, and maintain software applications\n- Write clean and efficient code\n..."
            )
        
        with col2:
            st.markdown("#### 📄 Your Resume")
            uploaded_file = st.file_uploader(
                "Upload your resume (PDF or DOCX)",
                type=['pdf', 'docx'],
                help="Upload your current resume for ATS analysis"
            )
            
            if uploaded_file:
                st.success(f"✅ {uploaded_file.name} uploaded successfully!")
        
        # Submit button
        st.markdown("---")
        col_center = st.columns([1, 2, 1])
        with col_center[1]:
            if st.button("🎯 Analyze & Optimize Resume", type="primary", use_container_width=True):
                if job_description and uploaded_file:
                    # Show progress
                    with st.spinner("🔍 Analyzing your resume against ATS requirements..."):
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Extract resume text
                        status_text.text("📄 Extracting resume content...")
                        progress_bar.progress(20)
                        time.sleep(0.5)
                        
                        if uploaded_file.name.endswith('.pdf'):
                            resume_text = extract_text_from_pdf(uploaded_file)
                        else:
                            resume_text = extract_text_from_docx(uploaded_file)
                        
                        # Analyze with AI
                        status_text.text("🤖 Running ATS analysis and optimization...")
                        progress_bar.progress(50)
                        
                        result = analyze_and_optimize_resume(resume_text, job_description)
                        
                        progress_bar.progress(100)
                        status_text.text("✅ Analysis complete!")
                        time.sleep(0.5)
                        
                        # Store in session state
                        st.session_state.analysis_done = True
                        st.session_state.result = result
                        st.rerun()
                        
                else:
                    if not job_description:
                        st.error("❌ Please enter the job description")
                    if not uploaded_file:
                        st.error("❌ Please upload your resume")

    # Results Section (show after analysis)
    else:
        st.markdown("### 🎉 Your ATS Analysis & Optimized Resume")
        
        # Display the full result
        st.markdown(st.session_state.result)
        
        # Action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("📋 Copy Optimized Resume", use_container_width=True):
                st.toast("✅ Content ready to copy! Select and copy from above.")
        
        with col2:
            # Create downloadable text file
            result_bytes = st.session_state.result.encode('utf-8')
            st.download_button(
                label="💾 Download as TXT",
                data=result_bytes,
                file_name="optimized_resume_analysis.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col3:
            if st.button("🔄 Analyze Another Resume", use_container_width=True):
                st.session_state.analysis_done = False
                st.session_state.result = None
                st.rerun()

    # Sidebar
    with st.sidebar:
        st.markdown("### ℹ️ How It Works")
        st.markdown("""
        1. **Paste** the job description
        2. **Upload** your resume (PDF/DOCX)
        3. **Click** Analyze & Optimize
        4. **Get** instant ATS score + optimized resume
        
        ---
        
        ### ✨ What You'll Get
        - 📊 Current ATS score analysis
        - ✅ Strengths identified
        - ❌ Gaps highlighted
        - 🚀 Fully optimized resume
        - 📈 Improved ATS score
        
        ---
        
        ### 🔒 Privacy
        Your data is processed securely and not stored.
        """)
        
        st.markdown("---")
        st.caption("Powered by OpenAI GPT-4")
