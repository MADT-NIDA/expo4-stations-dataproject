# Use the official Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

run pip install uv 
run uv pip install --upgrade pip --system


# Install dependencies
COPY requirements.txt .

RUN uv pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the app
COPY . .

# Run the app with Gunicorn + Uvicorn worker
CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
