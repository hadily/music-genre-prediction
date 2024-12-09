# Base image
FROM python:3.12

# Working directory
WORKDIR /app

# Copy the requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app
COPY . .
RUN mkdir -p /app/uploads

# Expose the port and start the app
EXPOSE 5000

CMD ["python", "svm_app.py"]
