# Use official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=7860

# Set work directory
WORKDIR /app

# Install system dependencies (required for some Python packages like sentence-transformers)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Collect static files (optional, but good practice for Django)
# RUN python manage.py collectstatic --noinput

# Expose the standard Hugging Face Space port
EXPOSE 7860

# Run gunicorn standardly for Django, binding to 0.0.0.0 and the port specified
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "core.wsgi:application"]
