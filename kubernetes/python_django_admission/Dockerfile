FROM python:3.13 AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---- Builder Stage ----
FROM base AS builder

# Install build dependencies
RUN pip install --upgrade pip

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# ---- Final Stage ----
FROM base AS final

# Copy the installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn
COPY --from=builder /usr/local/bin/django-admin /usr/local/bin/django-admin

# Create app directory
WORKDIR /app

# Copy your application code
COPY my_django_app/ .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create a non-root user
RUN adduser --disabled-password --gecos '' django
RUN chown -R django:django /app
USER django

# Expose the port Gunicorn will run on
EXPOSE 8000

# Command to run migrations, create sample data, and start the Gunicorn server
CMD ["sh", "-c", "python manage.py migrate && python manage.py create_sample_data && gunicorn --bind 0.0.0.0:8000 my_django_app.wsgi:application"]
