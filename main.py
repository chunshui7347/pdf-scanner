import os
import openai
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# OpenAI API key initialization
def ask_question(question: str, context: str):
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",  # Specify the model you want to use
            messages=[
                {"role": "system", "content": "You are a knowledgeable assistant for answering questions based on the given context."},
                {"role": "user", "content": f"Context: {context}"},
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message
        return answer
    except Exception as e:
        return f"An error occurred while asking the question: {e}"

# Streamlit UI
st.title("File-Based Question Answering Assistant")

# Upload file and process context
uploaded_file = st.file_uploader("Upload a file for context-based question answering", type=["pdf", "docx", "txt"])
file_content = ""

if uploaded_file is not None:
    # Process the file based on type
    if uploaded_file.type == "application/pdf":
        from PyPDF2 import PdfReader
        reader = PdfReader(uploaded_file)
        file_content = "\n".join([page.extract_text() for page in reader.pages])
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        import docx
        doc = docx.Document(uploaded_file)
        file_content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    elif uploaded_file.type == "text/plain":
        file_content = uploaded_file.read().decode("utf-8")

    st.write("File uploaded successfully and processed.")

# Handle user question input
if prompt := st.text_input("What would you like to know?"):
    if file_content:
        response = ask_question(prompt, file_content)
        st.write(response)
    else:
        st.write("Please upload a file to provide context for your question.")
