# PDF Reader using ChatGPT

## Overview
- Welcome to the PDF Question Answering Tool!!!!
- This tool uses the power of ChatGPT, a state-of-the-art language model, to help you find answers to your questions from any PDF document. 
- Simply upload your PDF file, type in your question, and let ChatGPT do the rest! 
- This tool is designed to make information retrieval easier and more efficient. Whether you're a student, researcher, or simply looking to find answers to your questions, this tool is here to help. 
- Give it a try today and experience the power of AI-assisted question answering!

## Installation
- Clone the repo
- Add `.env` file and .gitignore files
- Generate openAI API keys [here](https://platform.openai.com/account/api-keys )
- Install below python libraries 
  ```python
  pip install langchain pypdf2 python-dotenv streamlit openai tiktoken
  ```
- To view UI run below
  ```sh
  streamlit run /workspace/chatgpt-langchain-pdfreader/app.py
  ```