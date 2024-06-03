# Use the official Ubuntu image as a base
FROM ubuntu:latest

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    libpq-dev \
    build-essential \
    && apt-get clean

# Create and set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Create a virtual environment
RUN python3 -m venv /app/venv

# Activate the virtual environment and install Python dependencies
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the Django project files into the container
COPY . /app/

# Set environment variables to use the virtual environment's Python and Pip
ENV PATH="/app/venv/bin:$PATH"

# Expose the port that the app runs on
EXPOSE 8000

# Run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
