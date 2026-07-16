# Use an official Python image
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY app.py .

# Expose Flask's port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]