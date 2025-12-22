# Dockerfile for OmniMind "Glass Box" Demo
# Base Image: Python 3.12 (Matching Environment)
FROM python:3.12-slim

# Set Working Directory
WORKDIR /app

# Install System Dependencies (if any)
# procps for ps command if needed by scripts
RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*

# Copy Requirements
# We will create a minimal requirements.txt for the demo to save build time
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Application Source
COPY src/ /app/src/
COPY scripts/ /app/scripts/
COPY config/ /app/config/
COPY web/ /app/web/

# Expose Streamlit Port
EXPOSE 8080

# Environment Variables
ENV PYTHONPATH=/app
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Run Command
CMD ["streamlit", "run", "web/dashboard_mvp.py"]
