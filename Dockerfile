# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt 

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the Python script when the container launches
CMD ["python", "agents.py"]