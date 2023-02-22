# Use an official Python runtime as the base image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /views

# Copy the current directory contents into the container at /app
COPY . /views

# Define environment variables
ENV FLASK_APP=views
ENV FLASK_DEBUG=true

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt
# RUN python3 -m flask db migrate

# Run the command to start the service
CMD ["flask", "run", "--host=0.0.0.0"]
