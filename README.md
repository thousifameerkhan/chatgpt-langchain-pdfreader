# PDF Reader using ChatGPT

## Overview
- Welcome to the PDF Question Answering Tool!!!!
- This tool uses the power of ChatGPT, a state-of-the-art language model, to help you find answers to your questions from any PDF document. 
- Simply upload your PDF file, type in your question, and let ChatGPT do the rest! 
- This tool is designed to make information retrieval easier and more efficient. Whether you're a student, researcher, or simply looking to find answers to your questions, this tool is here to help. 
- Give it a try today and experience the power of AI-assisted question answering!

## Fundamentals
- `Chunk Size:` 
  - It refers to the number of characters or words that a text is divided into when using a text splitter. 
  - It determines the size of each individual chunk of text that is processed.
- `CharacterTextSplitter:`
  - It works by taking in a string of text and a chunk size, and then splitting the text into chunks of that size. 
  - The chunks can be used for various purposes, such as indexing or processing with language models.
- `Text Embedding:`
  - It is the process of representing words or phrases in a numerical vector space, such that the distance between the vectors reflects the semantic similarity between the corresponding words or phrases.
  - This techniques provide a powerful way to represent natural language text data in a numerical vector space, enabling downstream machine learning models to more effectively capture semantic relationships between words and phrases.
- `Vector Store:`
  - It is a database system that stores and manages precomputed vector embeddings of text data, typically used for natural language processing tasks.
  - It allows efficient storage and retrieval of precomputed embeddings, which can significantly speed up the process of training machine learning models on large text datasets.

## Installation - OpenAI
- Clone the repo
- Add `.env` file and .gitignore files
- Generate openAI API keys [here](https://platform.openai.com/account/api-keys) and update `OPENAI_API_KEY` in `.env`
- Install below python libraries 
  ```python
  pip install langchain pypdf2 python-dotenv streamlit openai tiktoken
  ```
- To view UI run below
  ```sh
  streamlit run /workspace/chatgpt-langchain-pdfreader/app.py
  ```

## Installation - HuggingFace
- Clone the repo
- Add `.env` file and .gitignore files
- Generate openAI API keys [here](https://huggingface.co/settings/tokens) and update `HUGGING_FACE_API_KEY` in `.env`
- Install below python libraries 
  ```python
  pip install pypdf2 python-dotenv streamlit transformers torch
  ```
- To view UI run below
  ```sh
  streamlit run /workspace/chatgpt-langchain-pdfreader/hugging_chat.py
  ```

## Installation - Cohere
- Clone the repo
- Add `.env` file and .gitignore files
- Generate openAI API keys [here](https://huggingface.co/settings/tokens) and update `HUGGING_FACE_API_KEY` in `.env`
