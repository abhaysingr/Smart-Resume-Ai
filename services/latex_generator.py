from config.groq_config import get_groq_client
from utils.logger import setup_logger

logger = setup_logger(__name__)

def generate_latex_resume(resume_data, template_style, job_role):
    """
    Generate LaTeX code for resume using Groq API with job role targeting
    
    Args:
        resume_data: Dictionary containing all resume information
        template_style: Selected template (ATS-Friendly, Modern, Professional, etc.)
        job_role: Target job role the user is applying for
    
    Returns:
        str: Generated LaTeX code
    """
    try:
        client = get_groq_client()
        
        # Format resume data as text
        resume_text = format_resume_data_as_text(resume_data)
        
        # Get template-specific instructions
        template_instructions = get_template_specific_instructions(template_style)
        
        # Construct the enhanced prompt with job role
        prompt = f"""You are an expert resume writer and LaTeX developer. Create a stunning, professional, ONE-PAGE resume for a {job_role} position.

**CRITICAL REQUIREMENTS:**
1. Use ONLY pdflatex-compatible packages (NO fontspec)
2. Make it visually appealing, modern, and professional
3. Use strategic whitespace and formatting
4. Highlight achievements with metrics and numbers where possible
5. Tailor ALL content specifically for {job_role} role
6. Use power verbs (Developed, Architected, Implemented, Optimized, Led, Designed)
7. Must fit on ONE PAGE with professional spacing
8. Make it ATS-friendly with proper keywords
9. Show FULL URLs for LinkedIn and GitHub (not just "LinkedIn" or "GitHub")
10. Add visual separation between sections

**Template Style: {template_style}**

{template_instructions}

**Resume Content to Transform:**
{resume_text}

**MANDATORY LaTeX Structure and Best Practices:**
```latex
\\documentclass[10pt,letterpaper]{{article}}

% Packages
\\usepackage[margin=0.5in]{{geometry}}
\\usepackage{{titlesec}}
\\usepackage{{enumitem}}
\\usepackage{{hyperref}}
\\usepackage{{xcolor}}
\\usepackage{{tabularx}}
\\usepackage{{multicol}}

% Define colors based on template
{get_color_scheme(template_style)}

% Configure hyperlinks
\\hypersetup{{
    colorlinks=true,
    linkcolor=linkcolor,
    urlcolor=linkcolor,
    pdfborder={{0 0 0}}
}}

% Remove page numbers
\\pagestyle{{empty}}

% Section formatting with colored horizontal line
\\titleformat{{\\section}}
    {{\\large\\bfseries\\color{{sectioncolor}}}}
    {{}}{{0em}}{{}}[\\color{{sectioncolor}}\\titlerule]
\\titlespacing*{{\\section}}{{0pt}}{{10pt}}{{5pt}}

% Subsection formatting (for job titles, project names)
\\titleformat{{\\subsection}}
    {{\\normalsize\\bfseries}}
    {{}}{{0em}}{{}}
\\titlespacing*{{\\subsection}}{{0pt}}{{5pt}}{{3pt}}

% Adjust spacing
\\setlength{{\\parindent}}{{0pt}}
\\setlength{{\\parskip}}{{0pt}}
\\setlist{{nosep, leftmargin=1.5em, topsep=2pt}}

\\begin{{document}}

% ========== HEADER ==========
\\begin{{center}}
    {{\\Huge\\bfseries\\color{{namecolor}} FULL NAME HERE}}
    
    \\vspace{{4pt}}
    
    {{\\small
    \\href{{mailto:EMAIL_HERE}}{{\\textbf{{EMAIL_HERE}}}} \\textbar{{}} 
    \\textbf{{PHONE_HERE}} \\textbar{{}} 
    \\textbf{{LOCATION_HERE}}
    }}
    
    \\vspace{{2pt}}
    
    {{\\small
    \\href{{FULL_LINKEDIN_URL}}{{linkedin.com/in/USERNAME}} \\textbar{{}} 
    \\href{{FULL_GITHUB_URL}}{{github.com/USERNAME}}
    }}
\\end{{center}}

\\vspace{{-8pt}}

% ========== PROFESSIONAL SUMMARY ==========
\\section*{{PROFESSIONAL SUMMARY}}
\\vspace{{-3pt}}
Write a compelling 2-3 line summary specifically highlighting passion and skills for {job_role}. Focus on key technical strengths, experience level, and what value you bring. Make it specific to {job_role} role.

\\vspace{{-3pt}}

% ========== TECHNICAL SKILLS ==========
\\section*{{TECHNICAL SKILLS}}
\\vspace{{-3pt}}
\\begin{{itemize}}[leftmargin=1em, itemsep=0.5pt]
    \\item \\textbf{{Programming Languages:}} List languages relevant to {job_role}
    \\item \\textbf{{Frameworks \\& Libraries:}} List frameworks most relevant to {job_role}
    \\item \\textbf{{Tools \\& Technologies:}} Development tools, version control, CI/CD tools
    \\item \\textbf{{Databases:}} Database technologies with specific skills
    \\item \\textbf{{Cloud \\& DevOps:}} Cloud platforms and DevOps tools if applicable
\\end{{itemize}}

\\vspace{{-3pt}}

% ========== PROFESSIONAL EXPERIENCE ==========
\\section*{{PROFESSIONAL EXPERIENCE}}
\\vspace{{-3pt}}

\\textbf{{Job Title / Internship Title}} \\hfill {{\\textit{{\\small Month YYYY -- Month YYYY}}}} \\\\
{{\\textit{{\\small Company Name, Location}}}}
\\vspace{{1pt}}
\\begin{{itemize}}[leftmargin=1.5em, itemsep=0.5pt]
    \\item Start with strong action verb + specific achievement + technology used + quantifiable result if possible
    \\item Example: Developed X feature using Y technology that improved Z by N\\%
    \\item Focus on IMPACT and RESULTS, not just duties
    \\item Maximum 3-4 bullets per role
\\end{{itemize}}

\\vspace{{-3pt}}

% ========== KEY PROJECTS ==========
\\section*{{KEY PROJECTS}}
\\vspace{{-3pt}}

\\textbf{{Project Name}} {{\\small\\textit{{| Tech1, Tech2, Tech3}}}} \\hfill {{\\textit{{\\small Month YYYY -- Month YYYY}}}} \\\\
{{\\small\\textit{{GitHub: \\href{{{{FULL_GITHUB_PROJECT_URL}}}}{{{{github.com/username/project}}}} }}}}
\\vspace{{1pt}}
\\begin{{itemize}}[leftmargin=1.5em, itemsep=0.5pt]
    \\item Developed/Built [specific feature] using [technologies] that resulted in [outcome]
    \\item Implemented [technical solution] to solve [problem], achieving [result]
    \\item Designed [system/component] with focus on [quality: scalability/performance/security]
\\end{{itemize}}

\\vspace{{-3pt}}

\\textbf{{Second Project Name}} {{\\small\\textit{{| Tech1, Tech2, Tech3}}}} \\hfill {{\\textit{{\\small Month YYYY -- Month YYYY}}}} \\\\
{{\\small\\textit{{GitHub: \\href{{{{FULL_GITHUB_PROJECT_URL}}}}{{{{github.com/username/project}}}} }}}}
\\vspace{{1pt}}
\\begin{{itemize}}[leftmargin=1.5em, itemsep=0.5pt]
    \\item Achievement-focused bullet points with specific technologies and outcomes
    \\item Highlight technical challenges solved
    \\item Show understanding of software engineering principles
\\end{{itemize}}

\\vspace{{-3pt}}

% ========== EDUCATION ==========
\\section*{{EDUCATION}}
\\vspace{{-3pt}}

\\textbf{{Degree (e.g., Bachelor of Technology in Computer Science)}} \\hfill {{\\textit{{\\small Month YYYY -- Month YYYY}}}} \\\\
{{\\small\\textit{{University Name, Location}}}} \\\\
{{\\small GPA: X.XX/4.0}}
\\begin{{itemize}}[leftmargin=1.5em, itemsep=0.5pt]
    \\item Achievements & Activities: List academic achievements, relevant coursework, or activities
\\end{{itemize}}

\\vspace{{-3pt}}

% ========== CERTIFICATIONS \\& ACHIEVEMENTS ==========
\\section*{{CERTIFICATIONS \\& ACHIEVEMENTS}}
\\vspace{{-3pt}}
\\begin{{itemize}}[leftmargin=1.5em, itemsep=0.5pt]
    \\item \\textbf{{Certification Name}} -- Issuing Organization (Month YYYY) \\\\
    {{\\small Verification: \\href{{{{FULL_VERIFICATION_URL}}}}{{{{URL_TEXT}}}}}}
    \\item \\textbf{{Achievement/Award}} -- Brief description with impact
    \\item Group related certifications together, prioritize most relevant to {job_role}
    \\item Include competitive programming ratings, hackathon wins, workshops only if space permits
\\end{{itemize}}

\\end{{document}}
```

**CONTENT ENHANCEMENT RULES:**

1. **Header Section:**
   - Name in large, bold text with color
   - Email, phone, location on first line
   - FULL LinkedIn URL (https://www.linkedin.com/in/username) and FULL GitHub URL (https://github.com/username) on second line
   - Display as: linkedin.com/in/username and github.com/username but link to full URLs

2. **Professional Summary:**
   - 2-3 lines maximum, tailored to {job_role}
   - Mention experience level (Fresher/1+ years)
   - Highlight 2-3 key strengths relevant to {job_role}
   - Show passion and career direction

3. **Technical Skills:**
   - Categorize intelligently (5-6 categories max)
   - Put most relevant skills for {job_role} first in each category
   - Remove generic/basic skills
   - Be specific (not just "Spring" but "Spring Boot, Spring Security, Spring Data JPA")

4. **Experience & Projects:**
   - Start EVERY bullet with action verbs: Developed, Architected, Implemented, Optimized, Led, Designed, Built, Created, Delivered
   - Include numbers/metrics: "Improved performance by 40%", "Reduced load time by 2 seconds", "Handled 1000+ requests/sec"
   - Format: [Action Verb] + [What you did] + [Technologies used] + [Result/Impact]
   - Maximum 3-4 bullets per item
   - Focus on technical achievements and problem-solving

5. **Education:**
   - Include full degree name (e.g., "Bachelor of Technology in Computer Science Engineering")
   - Add relevant coursework if space available
   - Include GPA if strong (>3.0/4.0 or >7.0/10.0)

6. **Certifications:**
   - List most relevant first
   - Include issuing organization and date
   - Group similar items (e.g., all Forage programs together)
   - Remove if list becomes too long (keep only top 5-7)

**FORMATTING EXCELLENCE:**
- Consistent spacing (use \\vspace{{-3pt}} between sections)
- Proper date format: Month YYYY -- Month YYYY (e.g., Jan 2024 -- Present)
- Bold for emphasis on job titles, project names, certification names
- Italic for companies, locations, dates, technologies
- Clean bullet points with proper indentation
- One page MAXIMUM

**QUALITY REQUIREMENTS:**
✓ Shows FULL LinkedIn and GitHub URLs in header
✓ All content tailored to {job_role} with relevant keywords
✓ Strong action verbs in every bullet point
✓ Quantifiable results where possible
✓ Professional visual hierarchy with colors and formatting
✓ Easy to scan with clear sections
✓ ATS-friendly structure
✓ Compiles without errors in pdflatex
✓ Fits perfectly on ONE PAGE

Generate ONLY the complete, production-ready LaTeX code with all the improvements. No explanations, no markdown blocks."""

        logger.info(f"Sending enhanced request to Groq API for {template_style} template targeting {job_role} role")
        
        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"""You are a professional resume writer with 15+ years of experience and an expert LaTeX developer. You specialize in creating compelling, ATS-optimized resumes for {job_role} positions that get interviews at top companies. 

You write achievement-focused, metric-driven content. You create visually stunning, modern resumes that compile perfectly with pdflatex. You NEVER use fontspec. You ALWAYS show FULL URLs for LinkedIn (https://www.linkedin.com/in/username) and GitHub (https://github.com/username) in the contact section.

You follow these principles:
- Start every bullet point with strong action verbs
- Include quantifiable results wherever possible
- Tailor content specifically to the target role
- Use proper LaTeX formatting with colors and spacing
- Ensure the resume fits on exactly ONE page
- Make it visually appealing yet professional
- Focus on IMPACT and RESULTS over duties"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.8,
            max_tokens=4500,
            top_p=0.95,
            stream=False
        )
        
        latex_code = chat_completion.choices[0].message.content
        logger.info(f"Enhanced LaTeX code generated successfully for {job_role} role")
        
        # Clean up the response
        latex_code = latex_code.strip()
        if latex_code.startswith("```latex"):
            latex_code = latex_code[8:]
        elif latex_code.startswith("```tex"):
            latex_code = latex_code[6:]
        elif latex_code.startswith("```"):
            latex_code = latex_code[3:]
        
        if latex_code.endswith("```"):
            latex_code = latex_code[:-3]
        
        latex_code = latex_code.strip()
        
        # Remove any fontspec if present
        if "fontspec" in latex_code.lower():
            logger.warning("fontspec detected in output, removing...")
            latex_code = latex_code.replace("\\usepackage{fontspec}", "")
            latex_code = latex_code.replace("\\setmainfont{", "% \\setmainfont{")
        
        return latex_code.strip()
        
    except Exception as e:
        logger.error(f"Error generating LaTeX with Groq: {str(e)}", exc_info=True)
        raise Exception(f"Failed to generate LaTeX resume: {str(e)}")


def get_template_specific_instructions(template_style):
    """Get specific instructions based on template style"""
    
    instructions = {
        "ATS-Friendly": """
**ATS-Friendly Template Instructions:**
- Use simple, clean formatting with NO fancy designs or graphics
- Black text only, minimal use of colors (black for everything)
- Standard fonts (Computer Modern default LaTeX font)
- Clear section headers in BOLD UPPERCASE
- No tables for main content, use simple lists
- Standard bullet points
- Maximum readability for Applicant Tracking Systems
- Focus 100% on content over design
- Keywords naturally integrated throughout
""",
        
        "Modern": """
**Modern Template Instructions:**
- Use navy blue (#2C3E50 or similar) for section headers and name
- Teal or blue-green (#16A085 or #3498DB) for links
- Clean, contemporary sans-serif appearance
- Colored horizontal lines under section headers (\\titlerule)
- Strategic use of color for visual hierarchy (name > sections > links)
- Professional yet contemporary feel
- Balanced whitespace with modern spacing
- Subtle color accents that enhance readability
""",
        
        "Professional": """
**Professional Template Instructions:**
- Traditional business formatting with conservative design
- Black and white color scheme only
- Serif font appearance (default Computer Modern is perfect)
- Classic, formal section headers in bold
- Traditional bullet points with standard markers
- Emphasis on content and achievements over design
- Timeless, executive style suitable for corporate environments
- Conservative spacing and layout
""",
        
        "Minimal": """
**Minimal Template Instructions:**
- Ultra-clean design with generous whitespace
- Thin lines (0.4pt or 0.5pt) for subtle section dividers
- Muted gray (#555555 or #4A4A4A) for secondary text like dates and locations
- Simple, elegant typography with no decorative elements
- Focus on negative space and breathing room
- Sophisticated simplicity
- Modern minimalist aesthetic
- Let content speak through clean design
""",
        
        "Creative": """
**Creative Template Instructions:**
- Bold color palette: Deep blue (#1E3A8A) for headers, vibrant accent color like orange (#F97316) or purple (#7C3AED)
- Unique section header formatting (consider using boxes or creative underlines)
- Strategic use of color blocks or background shading
- Modern, distinctive typography hierarchy
- Can include text-based icons (★ ● ■ ▸ symbols)
- Creative but still professional and readable
- Suitable for design, creative, marketing, or startup roles
- Eye-catching while maintaining professional credibility
"""
    }
    
    return instructions.get(template_style, instructions["Modern"])


def get_color_scheme(template_style):
    """Get color definitions based on template"""
    
    color_schemes = {
        "ATS-Friendly": """
% Colors - ATS Friendly (Black only for maximum compatibility)
\\definecolor{namecolor}{RGB}{0, 0, 0}
\\definecolor{sectioncolor}{RGB}{0, 0, 0}
\\definecolor{linkcolor}{RGB}{0, 0, 0}
""",
        
        "Modern": """
% Colors - Modern (Navy blue and teal)
\\definecolor{namecolor}{RGB}{44, 62, 80}
\\definecolor{sectioncolor}{RGB}{44, 62, 80}
\\definecolor{linkcolor}{RGB}{22, 160, 133}
""",
        
        "Professional": """
% Colors - Professional (All black, classic)
\\definecolor{namecolor}{RGB}{0, 0, 0}
\\definecolor{sectioncolor}{RGB}{0, 0, 0}
\\definecolor{linkcolor}{RGB}{0, 0, 139}
""",
        
        "Minimal": """
% Colors - Minimal (Subtle grays)
\\definecolor{namecolor}{RGB}{33, 33, 33}
\\definecolor{sectioncolor}{RGB}{74, 74, 74}
\\definecolor{linkcolor}{RGB}{85, 85, 85}
""",
        
        "Creative": """
% Colors - Creative (Bold and vibrant)
\\definecolor{namecolor}{RGB}{30, 58, 138}
\\definecolor{sectioncolor}{RGB}{30, 58, 138}
\\definecolor{linkcolor}{RGB}{249, 115, 22}
"""
    }
    
    return color_schemes.get(template_style, color_schemes["Modern"])


def format_resume_data_as_text(resume_data):
    """
    Format resume data as readable text for the prompt
    """
    logger.debug(f"Formatting resume data: {resume_data}")
    personal_info = resume_data.get('personal_info', {})
    
    text = f"""
**Personal Information:**
Full Name: {personal_info.get('full_name', 'Not provided')}
Email: {personal_info.get('email', 'Not provided')}
Phone: {personal_info.get('phone', 'Not provided')}
Location: {personal_info.get('location', 'Not provided')}
LinkedIn FULL URL: {personal_info.get('linkedin', 'Not provided')}
GitHub FULL URL: {personal_info.get('github', 'Not provided')}
Portfolio: {personal_info.get('portfolio', 'Not provided')}

**Professional Summary:**
{resume_data.get('summary', 'Not provided - Please write a compelling 2-3 line summary')}

**Work Experience:**
"""
    
    experiences = resume_data.get('experience', [])
    if experiences:
        for exp in experiences:
            text += f"""
Position: {exp.get('position', 'Not provided')}
Company: {exp.get('company', 'Not provided')}
Start Date: {exp.get('start_date', 'Not provided')}
End Date: {exp.get('end_date', 'Present')}
Location: {exp.get('location', 'Not provided')}
Responsibilities/Achievements:
"""
            responsibilities = exp.get('responsibilities', [])
            if responsibilities:
                for resp in responsibilities:
                    text += f"  • {resp}\n"
            else:
                text += "  • Not provided - Please write achievement-focused bullets\n"
    else:
        text += "No work experience provided\n"
    
    text += "\n**PROJECTS (with dates, technologies, GitHub links, and achievements):**\n"
    projects = resume_data.get('projects', [])
    if projects:
        for proj in projects:
            text += f"""
Project Name: {proj.get('name', 'Not provided')}
Duration: {proj.get('start_date', 'Not provided')} - {proj.get('end_date', 'Not provided')}
Technologies: {proj.get('technologies', 'Not provided')}
GitHub URL: {proj.get('github_link', 'Not provided')}
Description: {proj.get('description', 'Not provided')}
Key Achievements:
"""
            key_points = proj.get('key_points', [])
            if key_points:
                for point in key_points:
                    text += f"  • {point}\n"
            else:
                text += "  • Not provided - Please write technical achievement bullets\n"
    else:
        text += "No projects provided\n"
    
    text += "\n**Education:**\n"
    education = resume_data.get('education', [])
    if education:
        for edu in education:
            text += f"""
Degree: {edu.get('degree', 'Not provided')}
Institution: {edu.get('school', 'Not provided')}
Start Date: {edu.get('start_date', 'Not provided')}
End Date: {edu.get('end_date', 'Not provided')}
GPA: {edu.get('gpa', 'Not provided')}
Location: {edu.get('location', 'Not provided')}
Achievements:
"""
            achievements = edu.get('achievements', [])
            if achievements:
                for achievement in achievements:
                    text += f"  • {achievement}\n"
            else:
                text += "  • No achievements provided\n"
    else:
        text += "Not provided\n"
    
    text += "\n**Skills (Categorized):**\n"
    skills = resume_data.get('skills', {})
    if skills:
        for category, skill_list in skills.items():
            if skill_list:
                text += f"{category}: {', '.join(skill_list)}\n"
    else:
        text += "No skills provided\n"
    
    # ADD CERTIFICATIONS SECTION
    text += "\n**CERTIFICATIONS & ACHIEVEMENTS (with verification links):**\n"
    certifications = resume_data.get('certifications', [])
    if certifications:
        for cert in certifications:
            text += f"""
Certification: {cert.get('name', 'Not provided')}
Issuer: {cert.get('issuer', 'Not provided')}
Issue Date: {cert.get('issue_date', 'Not provided')}
Credential ID: {cert.get('credential_id', 'Not provided')}
Verification URL: {cert.get('verification_url', 'Not provided')}
"""
    else:
        text += "No certifications provided\n"
    
    return text