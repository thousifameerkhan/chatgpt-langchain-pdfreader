import os
import requests
import weaviate
from dotenv import load_dotenv

from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Weaviate


def load_env_variables():
    # Loading API Key
    load_dotenv()
    
    print('\n##########################################################')
    print('>>>>>>>>>>>>>  Displaying Environment Variables <<<<<<<<<<')
    print('##########################################################')
    print('Loaded OpenAI API Key     -> '+os.getenv("OPENAI_API_KEY"))
    print('Loaded Weaviate URL       -> '+os.getenv("WEAVIATE_URL"))
    print('Loaded CSV Location       -> '+os.getenv("CSV_FILE_LOCATION"))
    print('Loaded Master ClassName   -> '+os.getenv("MASTER_CLASS_NAME"))
    print('##########################################################\n')

def create_weaviate_schema_and_class():
    # Loading Env Variables
    load_env_variables()
    
    print('##########################################################')
    print('>>>>>>>>>>  Creating Master Schema and Classes  <<<<<<<<<<')
    print('##########################################################')
    # Setting Variables
    weaviate_url = os.getenv("WEAVIATE_URL")
    schema_url = f"{weaviate_url}/schema"
    class_name = os.getenv("MASTER_CLASS_NAME")
    class_url = f"{weaviate_url}/v1/schema/{class_name}"

    # Creating Weaviate Client to interact VectorDB
    weaviate_client = weaviate.Client(weaviate_url)
    
    # Drop Master Class
    response = requests.delete(class_url)
    if response.status_code == 200:
        print(f"Class {class_name} deleted successfully")
    else:
        print(f"Failed to delete class {class_name} or {class_name} class does not exist")
    
    # Drop Schema
    response = requests.delete(schema_url)
    if response.status_code == 200:
        print("Schema deleted successfully")
    else:
        print("Failed to delete schema or no schema exist")
    
    # Creating New Schema
    schema = {
                "classes": [
                    {
                        "class": class_name,
                        "description": "Used to store the Master Data",
                        "properties": [
                            {
                                "name": "Key",
                                "dataType": ["text"],
                                "description": "Key Column"
                            },
                            {
                                "name": "Description",
                                "dataType": ["text"],
                                "description": "Description on Data. This field will be store as Vector"
                            }
                        ]
                    }
                ]
            }
    weaviate_client.schema.create(schema)
    Weaviate(weaviate_client,"Key","Description")
    print('##########################################################\n')

def load_csv_data():
    print('##########################################################')
    print('>>>>>>>>>>>>>>>  Loading data from CSV File  <<<<<<<<<<<<<')
    print('##########################################################')
    print("Initiated Data Load Process")
    
    # Loading CSV
    csv_args = {
                "delimiter": ",",
                'fieldnames': ['Key','Description']
               }
    doc = CSVLoader(file_path=os.getenv("CSV_FILE_LOCATION"), csv_args=csv_args)
    
    # Display CSV DataLoaded
    # for i, row in enumerate(doc.load()):
    #     print('Row {}: {}'.format(i+1, row))
    
    print("CSV Data Loaded Successfully")
    print('##########################################################\n')

def main():
    print("\nStarted Updating Knowledge of DataMappingGPT")
    
    create_weaviate_schema_and_class()
    load_csv_data()
    
    print("Completed Updating Knowledge of DataMappingGPT\n")

if __name__ == '__main__':
    main()


# << Init pip Commands >>
#########################
# pip install --upgrade pip
# pip install python-dotenv langchain weaviate-client openai
# python load_data.py

# << Weaviate Endpoints >>
##########################
# https://<>.weaviate.network/v1/meta
# https://<>.weaviate.network/v1/schema
# https://<>.weaviate.network/v1/schema/Master