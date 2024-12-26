import streamlit as st
import pandas as pd
import os
import main

# Function to clear the subfolder and save the new file
def clear_and_save(uploaded_file, subfolder):
    # Create the subfolder if it doesn't exist
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)

    # Clear the subfolder by removing all files
    for filename in os.listdir(subfolder):
        file_path = os.path.join(subfolder, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # Define the path to save the new uploaded file
    file_path = os.path.join(subfolder, uploaded_file.name)

    # Save the new uploaded file to the subfolder
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    return file_path


# Streamlit UI
st.title(":rainbow[AI-Powered CSV Analyzer & Code Executor]")

# File upload
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
user_message = st.text_input("Describe your request", placeholder="e.g., Find the average of column A")

# Define the subfolder path
subfolder = "uploaded_files"

# Button is visible from the start
if st.button("Generate Code and Execute"):
    # Error handling upon button click
    if uploaded_file is None:
        st.error("Please upload a CSV file.")
    elif not user_message.strip():
        st.error("Please provide a description of your request.")
    else:
        # Proceed with processing
        try:
            file_path = clear_and_save(uploaded_file, subfolder)
            df = pd.read_csv(uploaded_file)
            df_head = df.head()
            prompt = main.generate_prompt(df_head, user_message, file_path)
            with st.spinner("Generating Python code..."):
                try:
                    generated_code = main.generate_code(prompt)
                    st.write("Generated Python Code:")
                    st.code(generated_code)
                except Exception as e:
                    st.error(f"Error during code generation: {e}")
                    st.stop()

            # Execute the generated code
            with st.spinner("Executing Python code..."):
                result, error = main.execute_code(generated_code)

            if error:
                st.error(f"Error during execution: {error}")
            else:
                st.success("Execution Result:")
                st.write(result)
        except pd.errors.EmptyDataError:
            st.error("The uploaded CSV file is empty. Please upload a valid CSV file with data.")
        