# Use Python 3.13.1 as the base image
FROM python:3.13.1-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8501 for the Streamlit app
EXPOSE 8501

# Run the Streamlit app on container start
CMD ["streamlit", "run", "UI.py", "--server.port=8501"]
