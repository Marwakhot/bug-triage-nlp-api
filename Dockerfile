# Base image: Use a slim Python runtime for a smaller final image
FROM python:3.11-slim

# Set the project's working directory inside the container
WORKDIR /app

# Install system-level dependencies. libgomp1 is required by LightGBM.
RUN apt-get update && apt-get install -y libgomp1

# Copy requirements file first to leverage Docker's layer caching
COPY requirements.txt .

# Install all Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code
COPY . .

# Expose the default port Streamlit runs on
EXPOSE 8501

# Command to execute when the container starts
CMD ["streamlit", "run", "dashboard.py"]