# CSV Processor with AI - Streamlit App

This application allows users to upload a CSV file, describe a request in plain text, and generate Python code using OpenAI's API to process the CSV data. The code is executed dynamically within the app, and the results are displayed in real-time.

## Features:

- Upload a CSV file.
- Describe a request (e.g., "Find the average of column A").
- Generate Python code using OpenAI's API based on the CSV preview and the user's request.
- Execute the generated Python code and display the results.

## Prerequisites:

Before running this application, ensure you have the following:

- Docker (for containerized deployment)
- Python 3.13.1 (for local development)
- Streamlit (for building the web interface)
- Azure OpenAI API keys for interacting with the OpenAI API

## Setup and Installation:

### 1. Clone the Repository:

Clone the repository to your local machine (or create a new directory and add the necessary files):

```bash
git clone <repository-url>
```

### 2. Build the Docker Image:

After cloning the repository, navigate to the project directory and build the Docker image using the following command:

```bash
docker build -t quinnox-streamlit-app .
```

### 3. Run the Docker Container:

Once the Docker image has been built, you can run the container with the following command:

```bash
docker run -p 8501:8501 quinnox-streamlit-app
```

This will start the application in a Docker container and map port `8501` from the container to port `8501` on your host machine. Streamlit, by default, runs on port `8501`.

### 4. Access the Application:

After running the container, open your web browser and visit the following URL to access the app:

```
http://localhost:8501
```

This will open the **CSV Processor with AI** Streamlit app in your browser.

---

## Running the Application Locally (without Docker):

If you prefer to run the application without Docker, follow these steps:

### 1. Install Dependencies:

Ensure you have Python 3.13.1 installed on your system. Then, create a virtual environment and install the dependencies listed in `requirements.txt`:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

### 2. Set Up Environment Variables:

Make sure you have a `.env` file containing your Azure OpenAI credentials:

```bash
AZURE_DEPLOYMENT=your_azure_deployment_name
AZURE_API_KEY=your_azure_api_key
AZURE_ENDPOINT=your_azure_endpoint_url
AZURE_API_VERSION=your_azure_api_version
```

### 3. Run the Application:

After installing dependencies and setting up your environment variables, you can run the app locally with the following command:

```bash
streamlit run UI.py
```

The app will be accessible at `http://localhost:8501`.

---

## Files in the Project:

- **`UI.py`**: The main Streamlit app that handles the user interface and interaction with the backend logic.
- **`main.py`**: Contains the backend logic for generating prompts, calling the OpenAI API, and executing Python code.
- **`.env`**: Environment variables for OpenAI API and Azure configuration.
- **`Dockerfile`**: Docker configuration file for containerized deployment.
- **`requirements.txt`**: List of Python dependencies required to run the app.

---

## Troubleshooting:

- **Missing environment variables**: Ensure that the `.env` file is present and correctly configured with your Azure OpenAI credentials.
- **API errors**: Verify that your Azure OpenAI API key, deployment name, and other settings are correct.
- **Port conflict**: If port `8501` is already in use on your system, specify a different port when running the Docker container with `-p <new-port>:8501`.

---

For any further assistance, feel free to reach out or open an issue in the repository.
