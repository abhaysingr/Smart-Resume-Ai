"""
This module contains helper functions for parsing and extracting data from resume files.
It uses basic text processing and regular expressions. This is the 'old' analyzer,
kept for its data extraction capabilities.
"""
import re

# Keyword definitions moved to module level for use by _extract_section
DOCUMENT_TYPES = {
    'resume': [
        'experience', 'education', 'skills', 'work', 'project', 'objective',
        'summary', 'employment', 'qualification', 'achievements'
    ],
    'marksheet': [
        'grade', 'marks', 'score', 'semester', 'cgpa', 'sgpa', 'examination',
        'result', 'academic year', 'percentage'
    ],
    'certificate': [
        'certificate', 'certification', 'awarded', 'completed', 'achievement',
        'training', 'course completion', 'qualified'
    ],
    'id_card': [
        'id card', 'identity', 'student id', 'employee id', 'valid until',
        'date of issue', 'identification'
    ]
}

class ResumeAnalyzer:
    """
    This class encapsulates the original rule-based parsing and extraction logic.
    It is used to extract structured data from resume text before passing it to the ML models.
    """
    
    def extract_text_from_pdf(self, file):
        try:
            import PyPDF2
            import io
            
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
            
    def extract_text_from_docx(self, docx_file):
        """Extract text from a DOCX file"""
        try:
            from docx import Document
            doc = Document(docx_file)
            full_text = []
            for paragraph in doc.paragraphs:
                full_text.append(paragraph.text)
            return '\n'.join(full_text)
        except Exception as e:
            raise Exception(f"Error extracting text from DOCX file: {str(e)}")

    def extract_personal_info(self, text):
        """Extract personal information from resume text"""
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        phone_pattern = r'(\+\d{1,3}[-.]?)?\s*\(?\d{3}\)?[-.]?\s*\d{3}[-.]?\s*\d{4}'
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        github_pattern = r'github\.com/[\w-]+'
        
        email = re.search(email_pattern, text)
        phone = re.search(phone_pattern, text)
        linkedin = re.search(linkedin_pattern, text)
        github = re.search(github_pattern, text)
        
        name = text.split('\n')[0].strip()
        
        return {
            'name': name if len(name) > 0 else 'Unknown',
            'email': email.group(0) if email else '',
            'phone': phone.group(0) if phone else '',
            'linkedin': linkedin.group(0) if linkedin else '',
            'github': github.group(0) if github else '',
            'portfolio': ''
        }

    def _extract_section(self, text, section_keywords):
        """A generic function to extract a section from resume text."""
        section_content = []
        lines = text.split('\n')
        in_section = False
        current_entry = []

        all_other_keywords = [k for k_list in DOCUMENT_TYPES.values() for k in k_list if k not in section_keywords]

        for line in lines:
            line = line.strip()
            line_lower = line.lower()

            if any(keyword.lower() in line_lower for keyword in section_keywords):
                if not any(keyword.lower() == line_lower for keyword in section_keywords):
                    current_entry.append(line)
                in_section = True
                continue
            
            if in_section:
                if line and any(other_keyword.lower() in line_lower for other_keyword in all_other_keywords):
                    in_section = False
                    if current_entry:
                        section_content.append(' '.join(current_entry))
                        current_entry = []
                    continue
                
                if line:
                    current_entry.append(line)
                elif current_entry:
                    section_content.append(' '.join(current_entry))
                    current_entry = []
        
        if current_entry:
            section_content.append(' '.join(current_entry))
        
        return section_content

    def extract_education(self, text):
        """Extract education information from resume text"""
        education_keywords = [
            'education', 'academic', 'qualification', 'degree', 'university', 'college',
            'school', 'institute', 'certification', 'diploma', 'bachelor', 'master',
            'phd', 'b.tech', 'm.tech', 'b.e', 'm.e', 'b.sc', 'm.sc','bca', 'mca', 'b.com',
            'm.com', 'b.cs-it', 'imca', 'bba', 'mba', 'honors', 'scholarship'
        ]
        return self._extract_section(text, education_keywords)

    def extract_experience(self, text):
        """Extract work experience information from resume text"""
        experience_keywords = [
            'experience', 'employment', 'work history', 'professional experience',
            'work experience', 'career history', 'professional background',
            'employment history', 'job history', 'positions held', 'experience',
            'job title', 'job responsibilities', 'job description', 'job summary'
        ]
        return self._extract_section(text, experience_keywords)

    def extract_projects(self, text):
        """Extract project information from resume text"""
        project_keywords = [
            'projects', 'personal projects', 'academic projects', 'key projects',
            'major projects', 'professional projects', 'project experience',
            'relevant projects', 'featured projects','latest projects',
            'top projects'
        ]
        return self._extract_section(text, project_keywords)

    def extract_summary(self, text):
        """Extract summary/objective from resume text"""
        summary_keywords = [
            'summary', 'professional summary', 'career summary', 'objective',
            'career objective', 'professional objective', 'about me', 'profile',
            'professional profile', 'career profile', 'overview', 'skill summary'
        ]
        return ' '.join(self._extract_section(text, summary_keywords))