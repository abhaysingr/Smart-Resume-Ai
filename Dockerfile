# Use an official Python runtime as a parent image
# We are choosing Python 3.11 as it has good compatibility with ML libraries like TensorFlow
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies that might be required by Python packages
# For example, git for installing packages from git repositories, or build-essential for compiling
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Using --no-cache-dir makes the image smaller
RUN pip install --no-cache-dir -r requirements.txt

# Download the spaCy language model
RUN python -m spacy download en_core_web_sm

# Copy the rest of the application code into the container at /app
COPY . .

# Make port 8501 available to the world outside this container
# This is the default port for Streamlit
EXPOSE 8501

# Define environment variables for the database connection
# These should be replaced with your actual database credentials in your deployment environment
ENV DB_HOST=db
ENV DB_NAME=ai_resume
ENV DB_USER=postgres
ENV DB_PASSWORD=root
ENV DB_PORT=5432

# Run app.py when the container launches
# Using --server.enableCORS=false can be useful for some deployment scenarios
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
