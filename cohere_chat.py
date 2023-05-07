import cohere
import os
from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter

def main():
    print('Starting Document ChatBot')

    # Creating Page
    st.set_page_config(page_title="Ask your PDF")
    st.header("Ask your PDF 😁")
    pdf = st.file_uploader("Upload your PDF",type="pdf")

    # Loading API Key
    load_dotenv()
    print('Loaded Cohere API Key ->'+os.getenv("COHERE_KEY"))
    print('Loaded Weaviate API Key ->'+os.getenv("WEAVIATE_URL"))

if __name__ == '__main__':
    main()