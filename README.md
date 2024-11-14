# PDF Scanner and Context-Based Question Answering Assistant

A Streamlit-based web application that allows users to upload documents and ask questions about their content. The app leverages OpenAI's GPT model to provide accurate and context-aware answers.

---

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Steps](#steps)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [License](#license)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)

---

## Features

- **File Upload**: Supports the following file formats:
  - PDF
  - DOCX
  - TXT
- **Text Extraction**: Automatically extracts text from uploaded files.
- **Context-Based Q&A**: Ask questions based on the uploaded file's content.
- **Interactive Web Interface**: Built with Streamlit for a seamless user experience.

---

## Technologies Used

- **[Streamlit](https://streamlit.io/)**: For building the web application interface.
- **[OpenAI API](https://openai.com/)**: For generating context-aware responses.
- **[PyPDF2](https://pypi.org/project/PyPDF2/)**: For extracting text from PDF files.
- **[python-docx](https://pypi.org/project/python-docx/)**: For extracting text from DOCX files.
- **[python-dotenv](https://pypi.org/project/python-dotenv/)**: For managing environment variables.

---

## Installation

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.8 or higher
- Pip (Python package manager)