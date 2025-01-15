FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN apt-get update --fix-missing && \
    apt-get install -y --fix-missing build-essential && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . /app

# Expose port
EXPOSE 8081

# Run main.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]