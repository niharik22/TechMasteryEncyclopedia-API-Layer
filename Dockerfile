# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /main
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables (these will be replaced with values from the .env file)
ENV API_USERNAME=${API_USERNAME}
ENV API_PASSWORD=${API_PASSWORD}

# Expose the port the main runs on
EXPOSE 8000

# Command to run the FastAPI main with Uvicorn
CMD ["uvicorn", "main.api.tech_mastery_api:app", "--host", "0.0.0.0", "--port", "8000"]
