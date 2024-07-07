# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Create a directory for data
RUN mkdir /app/data

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable to indicate we're in a Docker environment
ENV DOCKER_ENV=true

# Make port 80 available to the world outside this container
EXPOSE 80

# Run csv_generator.py when the container launches
ENTRYPOINT ["python", "csv_generator.py"]

