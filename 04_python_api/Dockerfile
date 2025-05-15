# Use an official Python runtime as a base image
# Using a lightweight image like alpine or slim is good for smaller images
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY main.py /app/
COPY requirements.txt /app/

# Install the Datadog Python library
RUN pip install -r requirements.txt

# Run the python script when the container starts
# Environment variables DATADOG_API_KEY and DATADOG_APP_KEY will be passed when running the container
CMD ["python", "main.py"]
