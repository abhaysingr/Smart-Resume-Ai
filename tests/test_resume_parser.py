import pytest
from utils.resume_parser import ResumeParser

@pytest.fixture
def parser():
    """Provides a ResumeParser instance for testing."""
    return ResumeParser()

def test_extract_skills_found(parser):
    """Tests that skills are correctly extracted from text."""
    text = "My skills include Python, Java, and some SQL. I have experience with AWS."
    expected_skills = ["python", "java", "sql", "aws"]
    
    # The order doesn't matter, so we compare sets
    assert set(parser.extract_skills(text)) == set(expected_skills)

def test_extract_skills_none_found(parser):
    """Tests that an empty list is returned when no skills are found."""
    text = "This is a document about cooking and baking."
    expected_skills = []
    
    assert parser.extract_skills(text) == expected_skills

def test_extract_skills_case_insensitivity(parser):
    """Tests that skills are found regardless of case."""
    text = "I am a PYTHON developer with experience in Docker and REACT."
    expected_skills = ["python", "docker", "react"]
    
    assert set(parser.extract_skills(text)) == set(expected_skills)

def test_extract_skills_duplicates(parser):
    """Tests that each skill is returned only once."""
    text = "I love python and I am good at python."
    expected_skills = ["python"]
    
    assert parser.extract_skills(text) == expected_skills
