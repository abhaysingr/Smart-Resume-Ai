import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import func, cast, Date
from collections import Counter
import io
import logging
from datetime import datetime, timedelta

# Import the new database session manager and ORM models
from config.database import get_db
from config.models import ResumeData, ResumeAnalysis, AdminLog

logger = logging.getLogger(__name__)

class DashboardManager:
    def __init__(self):
        self.colors = {
            'primary': '#2196F3', 'secondary': '#1976D2', 'warning': '#FFC107',
            'danger': '#F44336', 'info': '#03A9F4', 'success': '#4CAF50',
            'purple': '#9C27B0', 'background': '#f5f5f5', 'card': '#ffffff',
            'text': '#212529', 'subtext': '#495057'
        }

    def get_resume_metrics(self):
        """Fetches key metrics about resumes from the database using ORM."""
        with get_db() as db:
            total_resumes = db.query(func.count(ResumeData.id)).scalar()
            avg_ats_score = db.query(func.avg(ResumeAnalysis.ats_score)).scalar() or 0
            
            return {
                'total_resumes': total_resumes,
                'avg_ats_score': round(float(avg_ats_score), 2),
            }

    def get_skill_distribution(self, top_n=20):
        """Analyzes skill frequency from all resumes."""
        with get_db() as db:
            all_skills_str = db.query(ResumeData.skills).filter(ResumeData.skills.isnot(None)).all()
            
            all_skills = []
            for skills_tuple in all_skills_str:
                skills_str = skills_tuple[0]
                try:
                    # This assumes skills are stored like "['python', 'java']"
                    skills_list = eval(skills_str)
                    if isinstance(skills_list, list):
                        all_skills.extend([skill.lower().strip() for skill in skills_list])
                except (SyntaxError, NameError):
                    # Handle cases where skills might be a simple comma-separated string
                    if isinstance(skills_str, str):
                        all_skills.extend([s.lower().strip() for s in skills_str.split(',')])

            if not all_skills:
                return pd.DataFrame(columns=['Skill', 'Count'])

            skill_counts = Counter(all_skills)
            df = pd.DataFrame(skill_counts.items(), columns=['Skill', 'Count']).sort_values('Count', ascending=False)
            return df.head(top_n)

    def get_weekly_trends(self):
        """Gets the count of resumes created per day for the last 7 days."""
        with get_db() as db:
            seven_days_ago = datetime.now().date() - timedelta(days=7)
            trends_query = db.query(
                cast(ResumeData.created_at, Date).label('date'),
                func.count(ResumeData.id).label('count')
            ).filter(ResumeData.created_at >= seven_days_ago).group_by('date').order_by('date').all()
            
            df = pd.DataFrame(trends_query, columns=['Date', 'Count'])
            return df
            
    def get_all_resume_data(self):
        """Gets detailed data for all resumes for exporting."""
        with get_db() as db:
            results = db.query(ResumeData).outerjoin(ResumeAnalysis).order_by(ResumeData.created_at.desc()).all()
            
            data_list = []
            for r in results:
                data = {
                    "ID": r.id, "Name": r.name, "Email": r.email, "Phone": r.phone,
                    "LinkedIn": r.linkedin, "GitHub": r.github, "Portfolio": r.portfolio,
                    "Target Role": r.target_role, "Created At": r.created_at,
                    "ATS Score": r.analysis.ats_score if r.analysis else None
                }
                data_list.append(data)
            return pd.DataFrame(data_list)
            
    def get_admin_logs(self):
        """Gets all admin logs."""
        with get_db() as db:
            logs = db.query(AdminLog).order_by(AdminLog.timestamp.desc()).all()
            return pd.DataFrame([
                {"Admin Email": log.admin_email, "Action": log.action, "Timestamp": log.timestamp}
                for log in logs
            ])

    def export_to_excel(self):
        """Exports all resume data to an Excel file in memory."""
        df = self.get_all_resume_data()
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Resumes')
        return output.getvalue()
            
    def render_dashboard(self):
        """Renders the main dashboard UI."""
        if not st.session_state.get('is_admin', False) and not st.session_state.get('is_logged_in', False):
            st.error("🔒 Access Denied: You do not have permission to view this page.")
            return

        st.title("📊 Admin & User Dashboard")
        
        # Quick Stats
        metrics = self.get_resume_metrics()
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Total Resumes Processed", value=metrics.get('total_resumes', 0))
        with col2:
            st.metric(label="Average ATS Score", value=f"{metrics.get('avg_ats_score', 0):.2f}")
        
        st.markdown("---")

        # Visualizations
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Weekly Resume Submissions")
            trends_df = self.get_weekly_trends()
            if not trends_df.empty:
                fig = px.bar(trends_df, x='Date', y='Count', title="Resumes per Day", color_discrete_sequence=[self.colors['primary']])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No resume submissions in the last 7 days.")

        with col2:
            st.subheader("Top 20 Most Common Skills")
            skills_df = self.get_skill_distribution()
            if not skills_df.empty:
                fig = px.bar(skills_df, x='Count', y='Skill', orientation='h', title="Skill Frequency", color_discrete_sequence=[self.colors['secondary']])
                fig.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No skills data available to display.")

        st.markdown("---")
        
        # Data Table and Export
        st.subheader("📄 All Resume Data")
        all_data_df = self.get_all_resume_data()
        st.dataframe(all_data_df)
        
        if not all_data_df.empty:
            excel_data = self.export_to_excel()
            st.download_button(
                label="📥 Download as Excel",
                data=excel_data,
                file_name=f"resume_data_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
        st.markdown("---")

        # Admin Logs (only for admins)
        if st.session_state.get('is_admin', False):
            st.subheader("🛡️ Admin Activity Logs")
            log_df = self.get_admin_logs()
            st.dataframe(log_df)