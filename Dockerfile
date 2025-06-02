# Use official Python slim image for smaller size
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose port (Cloud Run requires 8080)
EXPOSE 8080

# Set environment variable for Cloud Run
ENV PORT=8080

# Run the application
CMD exec python app.py
