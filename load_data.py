import os
from dotenv import load_dotenv
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings

def main():
    print("Initiating Mapping Knowledge GPT")
    
    # Loading API Key
    load_dotenv()
    print('Loaded OpenAI API Key -> '+os.getenv("OPENAI_API_KEY"))
    print('Loaded Weaviate URL   -> '+os.getenv("WEAVIATE_URL"))

    # Loading CSV
    csv_args = {
                "delimiter": ";",
                "quotechar": '"',
                'fieldnames': ['Key','Description']
               }
    loader = CSVLoader(file_path='./01-data/master_table_column_comments.csv', csv_args=csv_args);
    print(loader)


if __name__ == '__main__':
    main()


# << Init pip Commands >>
#########################
# pip install --upgrade pip
# pip install python-dotenv langchain weaviate-client openai
# python load_data.py