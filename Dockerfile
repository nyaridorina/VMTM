# Base image
FROM python:3.11

# Install system dependencies
RUN apt-get update && apt-get install -y portaudio19-dev

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run the application
CMD ["python", "app.py"]
