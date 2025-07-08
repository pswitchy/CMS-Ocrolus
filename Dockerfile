# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code to the working directory
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set environment variables for flask
ENV FLASK_APP=run.py
ENV FLASK_CONFIG=production

# Run the app using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]