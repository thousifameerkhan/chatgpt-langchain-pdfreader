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
- Add `.env` file by copying `.env.sample`
- Generate openAI API keys [here](https://platform.openai.com/account/api-keys) and update `OPENAI_API_KEY` in `.env`
- Install below python libraries 
  ```python
  pip install --upgrade pip
  pip install langchain pypdf2 python-dotenv streamlit openai tiktoken
  ```

## Installation - HuggingFace
- Clone the repo
- Add `.env` file by copying `.env.sample`
- Generate HuggingFace API keys [here](https://huggingface.co/settings/tokens) and update `HUGGING_FACE_API_KEY` in `.env`
- Install below python libraries 
  ```python
  pip install --upgrade pip
  pip install pypdf2 python-dotenv streamlit transformers torch
  ```


## Installation - Cohere
- Clone the repo
- Add `.env` file by copying `.env.sample`
- Generate Cohere API keys [here](https://dashboard.cohere.ai/api-keys) and update `COHERE_KEY` in `.env`
- Install below python libraries 
  ```python
  pip install --upgrade pip
  pip install pypdf2 python-dotenv streamlit cohere langchain weaviate-client
  ```
- To view UI run below
  ```sh
  streamlit run /workspace/chatgpt-langchain-pdfreader/cohere_chat.py
  ```

## Reference
- [Cohere](https://python.langchain.com/en/latest/modules/models/text_embedding/examples/cohere.html)
- [Weaviate](https://python.langchain.com/en/latest/modules/indexes/vectorstores/examples/weaviate.html)
- [CSV Chat](https://www.youtube.com/watch?v=nr-mDSi9LxA)

## Misc
- pip install pandas openpyxl
- remove_comma.py is the file that travers through the excel sheet and extracts the data into csv files. comma is replaced by a space.


refernce :

https://weaviate.io/developers/weaviate/api/graphql/vector-search-parameters#nearvector
https://openai.com/blog/new-and-improved-embedding-model
