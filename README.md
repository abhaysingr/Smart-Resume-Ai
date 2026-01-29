# Smart Resume AI 🚀

A next-generation, AI-powered platform designed to help you create, analyze, and optimize your resume, cover letter, and professional portfolio for the modern job market. This tool is your personal career co-pilot, helping you stand out and land your dream job.

![Project Banner](https://placehold.co/1200x400/2f343a/ffffff?text=Smart+Resume+AI)

## 🎯 Purpose of the Application

In today's competitive job market, a generic resume isn't enough to get noticed. Most companies use Applicant Tracking Systems (ATS) to filter candidates, making it crucial for your resume to be optimized for both machines and humans.

Smart Resume AI was built to solve this problem. It's an intelligent assistant that helps you:

- **Beat the Robots**: Optimize your resume to get past automated screening systems.
- **Impress the Humans**: Craft a compelling, professional narrative that highlights your skills and achievements.
- **Save Time**: Automate the tedious parts of job application writing, like tailoring resumes and writing cover letters.

## ✨ Unique Features

This application goes beyond simple template-based resume builders. Here's what makes it unique:

- **🤖 AI-Powered Content Generation**: Uses powerful Generative AI models (like GPT from OpenAI and models from Groq) to write and enhance your resume sections and cover letters.
- **🎯 ATS Optimization Score**: Get a real-time score on how well your resume is optimized for Applicant Tracking Systems.
- **🔍 Side-by-Side Analysis**: Compare your resume against a specific job description to identify missing keywords and areas for improvement.
- **👔 Professional Portfolio Generator**: Automatically create a clean, shareable web page to showcase your projects.
- **🔐 Secure User & Admin System**: Features separate, secure login systems for users and administrators, with password hashing using `bcrypt`.
- **📊 Admin Analytics Dashboard**: A dedicated dashboard for administrators to monitor application usage, user activity, and resume statistics.

---

## 🛠️ Technology Stack

This project is built with a modern, robust technology stack:

- **Backend**: Python
- **Web Framework**: Streamlit
- **Database**: PostgreSQL
- **ORM & Migrations**: SQLAlchemy, Alembic
- **Generative AI**: OpenAI, Groq APIs
- **Authentication**: `bcrypt` for password hashing
- **File Processing**: `PyPDF2` (PDFs), `python-docx` (Word Documents)
- **Deployment**: Docker

---

## 🚀 Getting Started

You can run this application using Docker (recommended for ease of use) or by setting it up manually on your local machine.

### Method 1: Docker Setup (Recommended)

This is the easiest way to get the application running, as it handles all dependencies and configuration for you.

**Prerequisites:**
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed on your machine.

**Steps:**

1.  **Start a PostgreSQL Database with Docker:**
    Run this command in your terminal to start a PostgreSQL container.
    ```bash
    docker run --name my-postgres-db -e POSTGRES_PASSWORD=your_secure_password -e POSTGRES_DB=ai_resume_db -p 5432:5432 -d postgres
    ```
    *You can change `your_secure_password`, but remember it for the next step.*

2.  **Build the Application's Docker Image:**
    In the project's root directory, run:
    ```bash
    docker build -t smart-resume-ai .
    ```

3.  **Run the Application Container:**
    Run the application, connecting it to the PostgreSQL database you just started.
    ```bash
    docker run -p 8501:8501 \
      -e DB_HOST=host.docker.internal \
      -e DB_NAME=ai_resume_db \
      -e DB_USER=postgres \
      -e DB_PASSWORD=your_secure_password \
      -e ADMIN_EMAIL=admin@example.com \
      -e ADMIN_PASSWORD=admin123 \
      smart-resume-ai
    ```
    *Note: `host.docker.internal` allows the container to connect to the PostgreSQL database running on your host machine.*

4.  **Access the Application:**
    Open your web browser and navigate to `http://localhost:8501`.

### Method 2: Manual Local Setup

Follow these steps for a local development environment.

**Prerequisites:**
- Python 3.11 or newer
- PostgreSQL installed and a database created.
- [Git](https://git-scm.com/downloads) installed.

**Steps:**

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/ShadowAniket/AI-RESUME.git
    cd AI-RESUME
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    # Create the environment
    python -m venv venv
    # Activate on Windows
    .\venv\Scripts\activate
    # Activate on macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create the Database:**
    Using your preferred PostgreSQL client (e.g., `psql` or a GUI tool), create a new database.
    ```sql
    CREATE DATABASE ai_resume_db;
    ```

5.  **Configure Environment Variables:**
    Create a file named `.env` in the project's root directory. This file stores your database credentials and should not be shared.
    ```env
    # Database Configuration
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=ai_resume_db
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password

    # Default Admin User
    ADMIN_EMAIL=admin@example.com
    ADMIN_PASSWORD=admin123
    
    # API Keys for Generative AI (Optional, but needed for AI features)
    OPENAI_API_KEY="your-openai-api-key"
    GROQ_API_KEY="your-groq-api-key"
    ```

6.  **Run Database Migrations:**
    This command uses Alembic to set up all the necessary tables in your database.
    ```bash
    alembic upgrade head
    ```
    After running migrations, you can create the default admin user with the script:
    ```bash
    python setup_db.py
    ```

7.  **Run the Application:**
    ```bash
    streamlit run app.py
    ```

8.  **Access the Application:**
    Open your browser and go to `http://localhost:8501`.

---

## 📝 How to Use the Application

1.  **Sign Up / Sign In**: Create a user account or sign in to save and manage your data.
2.  **Resume Builder**:
    - Navigate to the **"📝 RESUME BUILDER"** page.
    - Fill in your personal information, work experience, education, and projects.
    - Click the "✨" icon next to sections like "Summary" or "Experience" to get AI-generated content suggestions.
3.  **ATS Resume Optimizer**:
    - Go to the **"🎯 ATS RESUME OPTIMIZER"**.
    - Upload your resume (PDF or DOCX).
    - Paste the job description for the role you're targeting.
    - Receive an ATS score and detailed feedback on how to improve your resume.
4.  **Cover Letter Generator**:
    - Go to the **"✉️ COVER LETTER GENERATOR"**.
    - If you've filled out the resume builder, your data will be pre-filled.
    - Paste a job description to generate a tailored cover letter.
5.  **Portfolio Viewer**:
    - Add your projects in the resume builder.
    - View your automatically generated portfolio on the **"🌐 PORTFOLIO VIEWER"** page. You can share the link with recruiters.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1.  Fork the repository.
2.  Create your feature branch (`git checkout -b feature/YourAmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/YourAmazingFeature`).
5.  Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
