import streamlit as st
import pandas as pd
from openai import AzureOpenAI
import re 
import sys
import io
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client= AzureOpenAI( azure_deployment=os.getenv('AZURE_DEPLOYMENT'),
    api_key=os.getenv('AZURE_API_KEY'), 
    azure_endpoint=os.getenv('AZURE_ENDPOINT'), 
    api_version=os.getenv('AZURE_API_VERSION')
    )

def generate_prompt(df, user_message, file_path):
    """Generate a prompt for the API based on CSV content and user request."""
    preview = df.head(5).to_dict()  # Provide a small sample of the CSV
    return f"""
    The user uploaded a CSV file with the following preview:
    {preview}
    The user wants to: {user_message}
    Write Python code using pandas to fulfill the request and print it. Make sure to include negative scenarios/error handling
    The given preview is just for your reference, the generated code should take the input as file path: {file_path}
    Note: Surround your python code with @@@ and @@@. Don't include delimiters such as ```python and ```.
    """

def generate_code(prompt):
    """Call the OpenAI API to generate Python code."""
    result =client.chat.completions.create( 
                model="deployment_name", 
                messages=[ {"role": "user", "content": prompt} ], 
                temperature=0, 
                max_tokens=4096 )
    code = result.choices[0].message.content
    # Regular expression to match content between @@@ markers
    pattern = r"@@@(.*?)@@@"

    # Use re.DOTALL to match across multiple lines
    matches = re.findall(pattern, code, re.DOTALL)

    # Extract and clean the matched code
    if matches:
        extracted_code = matches[0].strip()
        return extracted_code
    else:
        return "No code found between @@@ markers."

def execute_code(code, retries=3, delay=2):
    """
    Execute Python code dynamically, capture its printed output, and handle errors with retries.

    Args:
        code (str): The Python code to execute.
        retries (int): The number of times to retry execution in case of failure (default is 3).
        delay (int): The delay in seconds between retries (default is 2).

    Returns:
        tuple: A tuple containing:
            - captured_output (str): Any output printed by the code.
            - error (str): An error message if any occurred, otherwise None.
    """
    attempt = 0
    while attempt < retries:
        attempt += 1
        
        # Redirect stdout to capture print statements
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()

        try:
            # Execute the code
            exec(code, {})
            
            # Get the captured output
            result = captured_output.getvalue()
            sys.stdout = old_stdout  # Restore stdout

            # Return captured output
            return result, None
        
        except Exception as e:
            # Restore stdout if there's an exception
            sys.stdout = old_stdout
            error_message = f"Error on attempt {attempt}: {str(e)}"
            
            # If retry is needed, wait before retrying
            if attempt < retries:
                print(f"Attempt {attempt} failed. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                # After final attempt, return the error
                return None, error_message


