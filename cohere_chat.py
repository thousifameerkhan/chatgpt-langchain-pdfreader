import cohere
import os
import weaviate
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

    # Loading API Key
    load_dotenv()
    print('Loaded Cohere API Key ->'+os.getenv("COHERE_API_KEY"))
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

        # Create Embeddings
        embeddings = CohereEmbeddings()
        
        # Creating Weaviate Client
        WEAVIATE_URL = os.getenv("WEAVIATE_URL")
        client = weaviate.Client(
            url=WEAVIATE_URL,
            additional_headers={
                'X-Cohere-Api-Key': os.getenv("COHERE_API_KEY")
            })
        
        # Delete all Schema
        client.schema.delete_all()
        client.schema.get()

        # Create new Schema
        schema = {
                    "classes": [
                        {
                            "class": "UserManual",
                            "description": "OFSLL User Manual",
                            "vectorizer": "text2vec-cohere",
                            "vectorIndexConfig": {
                                "distance": "dot"
                            },
                            "moduleConfig": {
                                "text2vec-cohere": {
                                    "model": "multilingual-22-12",
                                    "truncate": "RIGHT",
                                    "vectorizeClassName": True
                                }
                            },
                            "properties": [
                                {
                                    "name": "content",
                                    "dataType": [
                                        "text"
                                    ],
                                    "description": "Vectorized data of OFSLL User Manual",
                                    "moduleConfig": {
                                        "text2vec-cohere": {
                                        "skip": False,
                                        "vectorizePropertyName": False
                                        }
                                    }
                                }
                            ]
                        }
                    ]
                }
        client.schema.create(schema)
        vectorstore = Weaviate(client, "UserManual", "content")

        # Storing Data
        knowledge_base = Weaviate.from_texts(chunks, embeddings)

        # Querying Data
        user_question = st.text_input("Ask any question about your PDF :")
        if user_question:
            docs = knowledge_base.similarity_search(user_question)
            st.write(docs)

if __name__ == '__main__':
    main()