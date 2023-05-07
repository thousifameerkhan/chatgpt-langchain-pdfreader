from dotenv import load_dotenv
import os
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS


def main():
    load_dotenv()
    # print('Hello World')
    st.set_page_config(page_title="Ask your PDF")
    st.header("Ask yout PDF 😁")

    ##upload the file
    pdf = st.file_uploader("Upload your PDF",type="pdf")
    # print(os.getenv("OPENAI_API_KEY"))

    #etract the data
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        #st.write(text)

        #splitting
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        # st.write(chunks)
        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)
        
        user_question = st.text_input("Ask any question about your PDF :")
        if user_question:
            docs = knowledge_base.similarity_search(user_question)
        st.write(docs)

if __name__ == '__main__':
    main()