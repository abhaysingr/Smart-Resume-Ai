import os
import logging
from contextlib import contextmanager
from datetime import datetime, timedelta

import bcrypt
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from .models import (
    Admin, AdminLog, User, PasswordResetToken,
    ResumeData, Experience, Education, Project, ResumeAnalysis
)

logger = logging.getLogger(__name__)

# --- SQLAlchemy Engine and Session Setup ---

@st.cache_resource
def get_engine():
    """Create and cache the SQLAlchemy engine."""
    load_dotenv(override=True)
    
    db_url = None
    try:
        # First, try connecting using Streamlit secrets
        if "supabase" in st.secrets and "url" in st.secrets["supabase"]:
            db_url = st.secrets["supabase"]["url"]
            # SQLAlchemy uses 'postgresql://' instead of 'postgres://'
            if db_url.startswith("postgres://"):
                db_url = "postgresql" + db_url[len("postgres"):]
            logger.info("Connecting to DB using Streamlit secrets (Supabase).")
    except Exception as e:
        logger.warning(f"Could not connect using Streamlit secrets, falling back to env vars. Error: {e}")

    # Fallback to environment variables if secrets are not available
    if not db_url:
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME")

        if not all([db_user, db_password, db_host, db_port, db_name]):
            st.error("Database connection failed. Essential environment variables are missing.")
            logger.error("Database environment variables are not fully set. Engine not created.")
            return None
        
        db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        logger.info(f"Connecting to DB using environment variables.")

    try:
        engine = create_engine(db_url)
        return engine
    except Exception as e:
        st.error(f"Database connection failed. Please check your configuration. Error: {e}")
        logger.error(f"Could not create SQLAlchemy engine: {e}", exc_info=True)
        return None

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    """Provide a transactional scope around a series of operations."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ORM-based Data Functions ---

def add_user(email, password):
    """Add a new user with a hashed password to the users table."""
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(email=email, password=hashed_password)
    
    with get_db() as db:
        try:
            db.add(new_user)
            db.commit()
            return True
        except IntegrityError:
            db.rollback()
            logger.warning(f"Attempted to add existing user: {email}")
            return False
        except Exception as e:
            db.rollback()
            logger.error(f"Error adding user: {e}", exc_info=True)
            return False

def verify_user(email, password):
    """Verify user credentials using bcrypt from the users table."""
    with get_db() as db:
        try:
            user = db.query(User).filter(User.email == email).first()
            if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return True
            return False
        except Exception as e:
            logger.error(f"Error verifying user: {e}", exc_info=True)
            return False

def add_admin(email, password):
    """Add a new admin with a hashed password."""
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_admin = Admin(email=email, password=hashed_password)
    
    with get_db() as db:
        try:
            db.add(new_admin)
            db.commit()
            return True
        except IntegrityError:
            db.rollback()
            logger.warning(f"Attempted to add existing admin: {email}")
            return False
        except Exception as e:
            db.rollback()
            logger.error(f"Error adding admin: {e}", exc_info=True)
            return False

def verify_admin(email, password):
    """Verify admin credentials using bcrypt."""
    with get_db() as db:
        try:
            admin = db.query(Admin).filter(Admin.email == email).first()
            if admin and bcrypt.checkpw(password.encode('utf-8'), admin.password.encode('utf-8')):
                return True
            return False
        except Exception as e:
            logger.error(f"Error verifying admin: {e}", exc_info=True)
            return False

def log_admin_action(admin_email, action):
    """Log admin login/logout actions."""
    new_log = AdminLog(admin_email=admin_email, action=action)
    with get_db() as db:
        try:
            db.add(new_log)
            db.commit()
        except Exception as e:
            db.rollback()
            logger.error(f"Error logging admin action: {e}", exc_info=True)

def update_user_password(email, new_password):
    """Updates the user's password in the users table."""
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    with get_db() as db:
        try:
            user = db.query(User).filter(User.email == email).first()
            if user:
                user.password = hashed_password
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating user password: {e}", exc_info=True)
            return False

def store_reset_token(email, token):
    """Stores a password reset token in the database."""
    expires_at = datetime.now() + timedelta(hours=1)
    new_token = PasswordResetToken(email=email, token=token, expires_at=expires_at)
    with get_db() as db:
        try:
            db.add(new_token)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error storing reset token: {e}", exc_info=True)
            return False

def get_user_email_by_token(token):
    """Retrieves the user's email for a given valid token."""
    with get_db() as db:
        try:
            record = db.query(PasswordResetToken).filter(
                PasswordResetToken.token == token,
                PasswordResetToken.expires_at > datetime.now()
            ).first()
            return record.email if record else None
        except Exception as e:
            logger.error(f"Error retrieving user by token: {e}", exc_info=True)
            return None

def delete_reset_token(token):
    """Deletes a password reset token from the database."""
    with get_db() as db:
        try:
            db.query(PasswordResetToken).filter(PasswordResetToken.token == token).delete()
            db.commit()
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting reset token: {e}", exc_info=True)

def save_resume_data(data):
    """Save resume data using ORM."""
    personal_info = data.get('personal_info', {})
    
    new_resume = ResumeData(
        name=personal_info.get('full_name', ''),
        email=personal_info.get('email', ''),
        phone=personal_info.get('phone', ''),
        linkedin=personal_info.get('linkedin', ''),
        github=personal_info.get('github', ''),
        portfolio=personal_info.get('portfolio', ''),
        summary=data.get('summary', ''),
        target_role=data.get('target_role', ''),
        target_category=data.get('target_category', ''),
        skills=str(data.get('skills', [])), # Keeping this simple for now
        template=data.get('template', '')
    )

    for exp_data in data.get('experience', []):
        new_resume.experiences.append(Experience(**exp_data))
    
    for edu_data in data.get('education', []):
        new_resume.education.append(Education(**edu_data))

    for proj_data in data.get('projects', []):
        new_resume.projects.append(Project(**proj_data))

    with get_db() as db:
        try:
            db.add(new_resume)
            db.commit()
            db.refresh(new_resume)
            return new_resume.id
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving resume data: {e}", exc_info=True)
            return None

def save_analysis_data(resume_id, analysis):
    """Save resume analysis data using ORM."""
    new_analysis = ResumeAnalysis(
        resume_id=resume_id,
        ats_score=float(analysis.get('ats_score', 0)),
        keyword_match_score=float(analysis.get('keyword_match_score', 0)),
        format_score=float(analysis.get('format_score', 0)),
        section_score=float(analysis.get('section_score', 0)),
        missing_skills=analysis.get('missing_skills', ''),
        recommendations=analysis.get('recommendations', '')
    )
    with get_db() as db:
        try:
            db.add(new_analysis)
            db.commit()
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving analysis data: {e}", exc_info=True)

def get_resume_stats():
    """Get statistics about resumes using ORM."""
    with get_db() as db:
        try:
            total_resumes = db.query(func.count(ResumeData.id)).scalar()
            avg_ats_score = db.query(func.avg(ResumeAnalysis.ats_score)).scalar() or 0
            
            recent_activity_query = db.query(
                ResumeData.name,
                ResumeData.target_role,
                Resume_data.created_at
            ).order_by(ResumeData.created_at.desc()).limit(5).all()

            # Convert to list of dicts to match previous output format if needed
            recent_activity = [
                {"name": r.name, "target_role": r.target_role, "created_at": r.created_at}
                for r in recent_activity_query
            ]
            
            return {
                'total_resumes': total_resumes,
                'avg_ats_score': round(float(avg_ats_score), 2),
                'recent_activity': recent_activity
            }
        except Exception as e:
            logger.error(f"Error getting resume stats: {e}", exc_info=True)
            return None

def get_all_resume_data():
    """Get all resume data for admin dashboard using ORM."""
    with get_db() as db:
        try:
            # Query using join and return objects
            results = db.query(ResumeData).outerjoin(ResumeAnalysis).order_by(ResumeData.created_at.desc()).all()
            
            # Format data to be similar to old RealDictCursor output
            data_list = []
            for r in results:
                data = {
                    "id": r.id, "name": r.name, "email": r.email, "phone": r.phone,
                    "linkedin": r.linkedin, "github": r.github, "portfolio": r.portfolio,
                    "target_role": r.target_role, "target_category": r.target_category,
                    "created_at": r.created_at,
                    "ats_score": r.analysis.ats_score if r.analysis else None,
                    "keyword_match_score": r.analysis.keyword_match_score if r.analysis else None,
                    "format_score": r.analysis.format_score if r.analysis else None,
                    "section_score": r.analysis.section_score if r.analysis else None
                }
                data_list.append(data)
            return data_list
        except Exception as e:
            logger.error(f"Error getting all resume data: {e}", exc_info=True)
            return []

def get_admin_logs():
    """Get all admin logs using ORM."""
    with get_db() as db:
        try:
            # Query and return list of dicts to match old format
            logs = db.query(AdminLog).order_by(AdminLog.timestamp.desc()).all()
            return [
                {"admin_email": log.admin_email, "action": log.action, "timestamp": log.timestamp}
                for log in logs
            ]
        except Exception as e:
            logger.error(f"Error getting admin logs: {e}", exc_info=True)
            return []
