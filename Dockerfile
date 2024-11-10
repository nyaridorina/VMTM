# Use an official Python runtime as a base image
FROM python:3.11-slim

# Install PortAudio and other system dependencies
RUN apt-get update && \
    apt-get install -y portaudio19-dev ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Set up the working directory
WORKDIR /app

# Copy project files to the container
COPY . /app

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose the port that the app runs on
EXPOSE 5000

# Run the app with Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
