import os
import openai
import streamlit as st
import json
from io import BytesIO
import pandas as pd

# Retrieve API key from environment variable
openai.api_key = st.secrets["OPENAI_API_KEY"]

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
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        return f"An error occurred while asking the question: {e}"

def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Line Items')
    processed_data = output.getvalue()
    return processed_data
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
        # st.write(f"Answer: {response}")
        cleaned_response = response.split("```json")[1].strip().strip("```")

       # Parse the response string to JSON
        response_json = json.loads(cleaned_response)

        # Display the JSON in a nicely formatted way
        st.json(response_json)

        line_items = response_json.get("lineItems", [])

        # Convert lineItems to a DataFrame
        line_items_df = pd.DataFrame(line_items)

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
    else:
        st.write("Please upload a file to provide context for your question.")

