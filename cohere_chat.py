import cohere
import os
from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import CohereEmbeddings
from langchain.vectorstores import Weaviate

def main():
    print('Starting Document ChatBot')

    # Creating Page
    st.set_page_config(page_title="Ask your PDF")
    st.header("Ask your PDF 😁")
    pdf = st.file_uploader("Upload your PDF",type="pdf")
    user_question = st.text_input("Ask any question about your PDF :")

    # Loading API Key
    load_dotenv()
    print('Loaded Cohere API Key ->'+os.getenv("COHERE_KEY"))
    print('Loaded Weaviate API Key ->'+os.getenv("WEAVIATE_URL"))

    # Reading PDF
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        # st.write(text)

        # Text Splitting
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)

        # Creating Weaviate Client
        # WEAVIATE_URL = getpass.getpass(os.getenv("WEAVIATE_URL"))
        # knowledgeBase = Weaviate.
        

if __name__ == '__main__':
    main()