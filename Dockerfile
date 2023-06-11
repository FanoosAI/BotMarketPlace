# Use a light Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt .

# Install the project dependencies
RUN pip install -r requirements.txt

# Copy the entire project directory into the container
COPY . .

# Volume for the database
VOLUME ["/app/marketplace/data"]

# Expose the port on which the FastAPI application will run
EXPOSE 8058

# Start the FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8058", "--log-config", "logging.ini"]
