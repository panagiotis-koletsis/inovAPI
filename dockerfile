# Use Miniconda base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install pip dependencies inside base environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application
COPY . .

# Create uploads folder
RUN mkdir -p uploads

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI using uvicorn
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]