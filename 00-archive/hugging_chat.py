from dotenv import load_dotenv
import os
import torch
import streamlit as st
from PyPDF2 import PdfReader
from transformers import pipeline
from langchain.text_splitter import CharacterTextSplitter

def main():
    print('Starting Document ChatBot')

    # Loading API Key
    load_dotenv()
    print('API Key ->'+os.getenv("HUGGING_FACE_API_KEY")+' Loaded')

    # Creating Page
    st.set_page_config(page_title="Ask your PDF")
    st.header("Ask your PDF 😁")
    pdf = st.file_uploader("Upload your PDF",type="pdf")

    # Set up HuggingFace model
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = pipeline(
        "text2text-generation",
        model="OpenAssistant/oasst-sft-6-llama-30b-xor",
        tokenizer="OpenAssistant/oasst-sft-6-llama-30b-xor",
        device=device
    )

    # Upload the file
    pdf = st.file_uploader("Upload your PDF",type="pdf")

    # Extract the data
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Splitting
        chunk_size = 1000
        chunk_overlap = 200
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size - chunk_overlap)]

        # Similarity search
        user_question = st.text_input("Ask any question about your PDF :")
        if user_question:
            results = model(user_question, chunks)
            similarities = [result["score"] for result in results]
            similarities = sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)
            top_docs = [chunks[i] for i, _ in similarities[:3]]
            st.write(top_docs)

if __name__ == '__main__':
    main()