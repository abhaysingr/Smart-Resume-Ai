"""
This module simulates a Generative AI model for creating resume and cover letter content.
In a real-world application, these functions would make API calls to an LLM (e.g., Gemini, OpenAI).
For this simulation, they return realistic, hardcoded text to allow for UI and logic development.
"""

import time

def generate_summary(existing_summary, keywords=None):
    """
    Simulates rewriting a professional summary to be more impactful.
    """
    time.sleep(2) # Simulate network latency
    
    base_text = (
        "Highly motivated and results-oriented professional with a proven track record of success. "
        "Seeking to leverage my skills and experience in a challenging new role. "
    )
    
    if "Data Scientist" in keywords:
        return (
            "Results-driven Data Scientist with 5+ years of experience in machine learning, statistical analysis, "
            "and predictive modeling. Proficient in Python, R, and SQL, with a deep understanding of data "
            "structures and algorithms. Passionate about turning large datasets into actionable insights."
        )
    if "Software Engineer" in keywords:
        return (
            "Innovative Software Engineer with a passion for developing scalable and efficient applications. "
            "Experienced in full-stack development with expertise in JavaScript (React, Node.js) and Python (Django). "
            "A strong collaborator with a commitment to writing clean, maintainable code."
        )
        
    return base_text + "Adept at problem-solving and collaborating with cross-functional teams to achieve business objectives."

def generate_experience_description(company, position, bullet_points):
    """
    Generates an improved description of work experience based on a detailed
    prompt provided by the user, structuring the output into a Role Overview
    and Key Achievements.
    """
    time.sleep(2)  # Simulate network latency

    # 1. ROLE OVERVIEW
    role_overview = (
        f"Spearheaded the development and execution of key projects as a {position}, "
        f"driving engineering excellence and innovation at {company}."
    )

    # 2. KEY ACHIEVEMENTS (3 STAR Bullet Points)
    
    # Try to find a quantifiable result from the user's input
    import re
    result_metric = "[X]%"  # Default placeholder
    for point in bullet_points:
        match = re.search(r'(\d+%)', point)
        if match:
            result_metric = match.group(1)
            break
            
    # Try to find a technology or tool from the user's input
    action_tool = "a new automation script" # Default
    for point in bullet_points:
        if "python" in point.lower():
            action_tool = "a Python-based solution"
        elif "react" in point.lower():
            action_tool = "a new React component"
        elif "designed" in point.lower():
            action_tool = "a new UI/UX flow"
            
    key_achievements = [
        "- Situation/Task: Faced with the challenge of improving process efficiency and reducing manual errors in a fast-paced development environment.",
        f"- Action: Architected and deployed {action_tool} to streamline the workflow and automate repetitive tasks.",
        f"- Result: Achieved a significant {result_metric} improvement in team productivity and a reduction in critical errors, directly impacting project timelines."
    ]
    
    # Combine into a single string with plain text formatting for st.text_area
    return (
        "ROLE OVERVIEW\n"
        f"{role_overview}\n\n"
        "KEY ACHIEVEMENTS\n" +
        "\n".join(key_achievements)
    )

def generate_project_description(project_name, technologies, bullet_points):
    """
    Simulates rewriting project bullet points into a professional, STAR-based
    three-bullet overview.
    """
    time.sleep(2) # Simulate network latency

    # Default values
    problem_solved = "to streamline data processing"
    action_detail = "a full-stack solution"
    result_detail = "a 15% improvement in user engagement"

    # Simple keyword extraction from user's bullet points to make the output more dynamic
    if any("api" in p.lower() for p in bullet_points):
        action_detail = "a RESTful API"
    elif any("database" in p.lower() for p in bullet_points):
        action_detail = "a new database schema and optimized queries"
    
    if any("deployed" in p.lower() for p in bullet_points):
        problem_solved = "to automate a manual workflow"
        result_detail = "a significant reduction in deployment time"


    # 1. Situation/Task Bullet
    situation = (
        f"• Architected the '{project_name}' project, a critical initiative {problem_solved} "
        f"utilizing a tech stack of {technologies}."
    )

    # 2. Action Bullet
    action = (
        f"• Engineered {action_detail}, focusing on creating a scalable and maintainable codebase "
        "with modern development practices."
    )

    # 3. Result Bullet
    result = (
        f"• Deployed the solution, resulting in {result_detail} and receiving positive user feedback. "
        "Project link available upon request."
    )

    return f"{situation}\n{action}\n{result}"


def generate_ats_summary(raw_input):
    """
    Simulates generating an ATS-optimized summary based on raw input,
    following a specific A/B/C structure.
    """
    time.sleep(2)  # Simulate network latency

    # This is a hardcoded example of what the AI might return based on a hypothetical user input.
    # It dynamically incorporates parts of the user's input to seem more realistic.
    
    # A. CURRENT TITLE/STATUS + EXPERIENCE LEVEL
    # In a real scenario, the AI would parse this from the input. We'll simulate that.
    title = "Experienced Professional" # Default
    if "data scientist" in raw_input.lower():
        title = "Data Scientist"
    elif "software engineer" in raw_input.lower():
        title = "Software Engineer"
    elif "product manager" in raw_input.lower():
        title = "Product Manager"

    part_a = f"Results-driven and detail-oriented {title} with a strong foundation in analytical problem-solving."

    # B. KEY ACHIEVEMENTS (Quantified)
    # The AI would extract numbers or specific accomplishments. We'll simulate finding one.
    part_b = "Proven ability to contribute to team projects and deliver high-quality results under tight deadlines." # Default
    import re
    quantified_achievements = re.findall(r'\d+%', raw_input) # Find percentages
    if quantified_achievements:
        part_b = f"Demonstrated success in achieving key objectives, including improving metrics by {quantified_achievements[0]}."
    elif "gpa" in raw_input.lower():
        part_b = "Record of academic excellence, reflected in a strong GPA and positive feedback from educators."


    # C. TOP SKILLS & QUALIFICATIONS
    # The AI would identify key skills from the input.
    part_c = "Skilled in various modern technologies and programming languages relevant to the field." # Default
    skills = []
    if "python" in raw_input.lower():
        skills.append("Python")
    if "react" in raw_input.lower():
        skills.append("React")
    if "sql" in raw_input.lower():
        skills.append("SQL")
    if "machine learning" in raw_input.lower():
        skills.append("Machine Learning")
    
    if skills:
        part_c = f"Proficient in {', '.join(skills)} and quick to adapt to new technology stacks."

    return f"{part_a} {part_b} {part_c}"


def generate_cover_letter(resume_data, job_description, company_name):
    """
    Simulates generating a full, tailored cover letter.
    """
    time.sleep(3) # Simulate network latency

    user_name = resume_data.get('personal_info', {}).get('full_name', 'Your Name')
    
    return f"""
Dear Hiring Manager,

I am writing to express my enthusiastic interest in the position advertised on [Platform where you saw the ad], which I discovered through my deep respect for {company_name}'s innovative work in the industry. With my background in [Your Field, e.g., software engineering] and a proven ability to [mention a key skill from your resume], I am confident that I possess the skills and experience necessary to excel in this role.

The enclosed resume details my experience, including my recent role at [Previous Company], where I was responsible for [mention a key responsibility]. One of my proudest achievements was [mention an achievement], which demonstrates my commitment to delivering results. This experience has equipped me with a unique perspective on how to tackle the challenges outlined in your job description.

I am particularly drawn to {company_name}'s commitment to [mention a company value or project you admire]. My goal is to contribute to a team that is pushing the boundaries of what is possible, and I believe my skills are a perfect match for your needs.

Thank you for considering my application. I have attached my resume for your review and welcome the opportunity to discuss how I can be a valuable asset to your team.

Sincerely,
{user_name}
"""
