# Use official Python runtime as base image
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Expose ports (API on 8001, Streamlit on 8501)
EXPOSE 8001 8501

# Default command runs the API
# (You can override with docker run -c "streamlit run app.py" for Streamlit)
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8001"]
