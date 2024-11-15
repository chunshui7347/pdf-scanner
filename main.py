import os
import openai
import streamlit as st
import json
from io import BytesIO
import pandas as pd

# Initialize OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to upload file and get file ID
def upload_file_to_openai(file):
    response = openai.files.create(
        file=file,
        purpose="assistants"
    )
    return response.id

# Function to ask a question using threads
def ask_question_with_thread(question, file_id):
    try:
        # Create a thread
        thread = openai.beta.threads.create()

        # Get or create an assistant with file_search tool
        def get_or_create_assistant():
            for assistant in openai.beta.assistants.list():
                if assistant.name == "File QA Assistant":
                    return assistant
            return openai.beta.assistants.create(
                model="gpt-4o-mini",
                description="Assistant for file-based Q&A",
                instructions="You are a helpful assistant answering questions based on uploaded file context.",
                tools=[{"type": "file_search"}],
                name="File QA Assistant",
            )

        assistant = get_or_create_assistant()

        # Create a prompt message with attached file
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=question,
            attachments=[
                {
                    "file_id": file_id,
                    "tools": [{"type": "file_search"}]
                }
            ]
        )

        # Run the thread and get the response
        run = openai.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id,
            timeout=300
        )

        if run.status == "completed":
            messages_cursor = openai.beta.threads.messages.list(thread_id=thread.id)
            messages = [message for message in messages_cursor]
            message = messages[0] 
            res_txt = message.content[0].text.value
            return res_txt

    except Exception as e:
        return f"An error occurred: {e}"

# Convert DataFrame to Excel for download
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Line Items')
    return output.getvalue()

# Streamlit UI
st.title("OpenAI File-Based Q&A")

uploaded_file = st.file_uploader("Upload a file (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
file_id = None

if uploaded_file:
    file_id = upload_file_to_openai(uploaded_file)
    st.success("File uploaded and ready for querying!")

# User query input
if prompt := st.text_input("Enter your question:"):
    if file_id:
        res_txt = ask_question_with_thread(prompt, file_id)

        # Extract the JSON part from response
        if '```json' in res_txt and '```' in res_txt:
            res_txt = res_txt.split('```json')[1].split('```')[0].strip()
        else:
            st.error("No JSON format found in the response.")
            st.write(res_txt)  # Show raw text if JSON is not found
        try:
            # Parse JSON
            response_json = json.loads(res_txt)
            st.json(response_json)  # Display formatted JSON

            # Convert lineItems to a DataFrame
            line_items_df = pd.DataFrame(response_json)

            # Display the DataFrame in Streamlit
            st.write("### Line Items")
            st.dataframe(line_items_df)

            excel_data = convert_df_to_excel(line_items_df)

            st.download_button(
                label="Download Line Items as Excel",
                data=excel_data,
                file_name="line_items.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except json.JSONDecodeError:
            st.error("Could not parse the response as JSON.")
            st.write(res_txt)  # Display raw response if parsing fails
    else:
        st.warning("Please upload a file first.")