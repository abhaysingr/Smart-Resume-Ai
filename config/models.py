from sqlalchemy import (
    create_engine, Column, Integer, String, Text, DateTime,
    ForeignKey, REAL
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AdminLog(Base):
    __tablename__ = 'admin_logs'
    id = Column(Integer, primary_key=True)
    admin_email = Column(String, nullable=False)
    action = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class PasswordResetToken(Base):
    __tablename__ = 'password_reset_tokens'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    token = Column(String, nullable=False, unique=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)

class ResumeData(Base):
    __tablename__ = 'resume_data'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    linkedin = Column(Text)
    github = Column(Text)
    portfolio = Column(Text)
    summary = Column(Text)
    target_role = Column(Text)
    target_category = Column(Text)
    skills = Column(Text)  # Storing as string, could be improved to a related table
    template = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    experiences = relationship("Experience", back_populates="resume", cascade="all, delete-orphan")
    education = relationship("Education", back_populates="resume", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="resume", cascade="all, delete-orphan")
    skills_entries = relationship("ResumeSkill", back_populates="resume", cascade="all, delete-orphan")
    analysis = relationship("ResumeAnalysis", back_populates="resume", cascade="all, delete-orphan", uselist=False) # One-to-one

class Experience(Base):
    __tablename__ = 'experiences'
    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey('resume_data.id'), nullable=False)
    company = Column(Text)
    position = Column(Text)
    start_date = Column(Text)
    end_date = Column(Text)
    description = Column(Text)
    
    resume = relationship("ResumeData", back_populates="experiences")

class Education(Base):
    __tablename__ = 'education'
    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey('resume_data.id'), nullable=False)
    school = Column(Text)
    degree = Column(Text)
    field = Column(Text)
    graduation_date = Column(Text)
    gpa = Column(Text)
    
    resume = relationship("ResumeData", back_populates="education")

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey('resume_data.id'), nullable=False)
    name = Column(Text)
    technologies = Column(Text)
    description = Column(Text)
    link = Column(Text)
    
    resume = relationship("ResumeData", back_populates="projects")

class ResumeSkill(Base):
    __tablename__ = 'resume_skills'
    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey('resume_data.id'), nullable=False)
    skill_name = Column(Text, nullable=False)
    skill_category = Column(Text, nullable=False)
    proficiency_score = Column(REAL)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    resume = relationship("ResumeData", back_populates="skills_entries")

class ResumeAnalysis(Base):
    __tablename__ = 'resume_analysis'
    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey('resume_data.id'), nullable=False, unique=True) # Ensure one-to-one
    ats_score = Column(REAL)
    keyword_match_score = Column(REAL)
    format_score = Column(REAL)
    section_score = Column(REAL)
    missing_skills = Column(Text)
    recommendations = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    resume = relationship("ResumeData", back_populates="analysis")
