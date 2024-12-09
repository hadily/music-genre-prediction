# Base image
# Use an official Python image as the base
FROM python:3.12-slim

# Working directory
WORKDIR /app

# Copy the requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app
COPY . .
RUN mkdir -p /app/uploads

# Expose port and define entry point
EXPOSE 5001

CMD ["python", "vgg_app.py"]
