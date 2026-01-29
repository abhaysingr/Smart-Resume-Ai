import pytest
from services.latex_generator import generate_latex_resume
import os

@pytest.fixture
def resume_data():
    """Provides a sample resume data dictionary for tests."""
    return {
        'personal_info': {
            'full_name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '123-456-7890',
            'location': 'New York, NY',
            'linkedin': 'https://linkedin.com/in/johndoe',
            'github': 'https://github.com/johndoe'
        },
        'summary': 'A passionate software developer.',
        'skills': {
            'Programming Languages': ['Python', 'JavaScript'],
            'Frameworks': ['Flask', 'React']
        },
        'experience': [
            {
                'position': 'Software Engineer',
                'company': 'Tech Corp',
                'start_date': 'Jan 2022',
                'end_date': 'Present',
                'location': 'San Francisco, CA',
                'responsibilities': ['Developed web applications.', 'Collaborated with team members.']
            }
        ],
        'projects': [
            {
                'name': 'Cool Project',
                'technologies': 'Python, Flask',
                'start_date': 'Jun 2021',
                'end_date': 'Dec 2021',
                'key_points': ['Did something cool.', 'Used by many people.']
            }
        ],
        'education': [
            {
                'degree': 'B.S. in Computer Science',
                'institution': 'State University',
                'start_date': 'Sep 2018',
                'end_date': 'May 2022',
                'location': 'State College, PA',
                'gpa': '3.8'
            }
        ],
        'certifications': [
            {
                'name': 'Certified Python Developer',
                'issuer': 'Python Institute',
                'issue_date': '2021'
            }
        ]
    }

def test_generate_latex_resume_modern_template(resume_data):
    """
    Tests that generate_latex_resume generates a non-empty string for the modern template.
    """
    latex_code = generate_latex_resume(resume_data, "Modern")
    assert latex_code
    assert "John Doe" in latex_code
    assert "Tech Corp" in latex_code
    assert "Cool Project" in latex_code
    assert "State University" in latex_code
    assert "Certified Python Developer" in latex_code
    assert "modern_template.tex" in open("services/latex_generator.py").read()

def test_generate_latex_resume_with_missing_info(resume_data):
    """
    Tests that generate_latex_resume handles missing data gracefully.
    """
    # Remove some data from the resume
    del resume_data['summary']
    del resume_data['certifications']

    latex_code = generate_latex_resume(resume_data, "Modern")
    assert latex_code
    assert "PROFESSIONAL SUMMARY" not in latex_code
    assert "CERTIFICATIONS & ACHIEVEMENTS" not in latex_code
