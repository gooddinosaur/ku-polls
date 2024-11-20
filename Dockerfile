# Use the official Python image with Alpine as the base
FROM python:3.10-alpine

# Arguments passed during the build
ARG ALLOWED_HOSTS=127.0.0.1,localhost

# Set the working directory
WORKDIR /app

# Environment variables for the application
ENV DEBUG=True
ENV TIMEZONE=UTC
ENV ALLOWED_HOSTS=${ALLOWED_HOSTS}

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose port 8000 for the Django development server
EXPOSE 8000

# Run migrations and start the Django development server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
