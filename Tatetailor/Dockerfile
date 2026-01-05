# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /Tatetailor

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run Daphne ASGI server (Daphne uses $PORT on Render, or we can use 8000)
# Most Render Docker setups expect the app to listen on $PORT
CMD daphne -b 0.0.0.0 -p $PORT Tatetailor.asgi:application
