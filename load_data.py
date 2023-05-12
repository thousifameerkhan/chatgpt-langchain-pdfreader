import os
import time
import traceback
import requests
import weaviate
from openai.embeddings_utils import get_embedding
from dotenv import load_dotenv
import pandas as pd

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
    weaviate_client = weaviate.Client(
                                        weaviate_url,
                                        additional_headers = {
                                                                "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")
                                                             }
                                     )
    
    try:
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
                            "vectorizer": "text2vec-openai",
                            "moduleConfig": {
                                "text2vec-openai": {
                                    "vectorizeClassName": True,
                                    "model": "davinci",
                                    "modelVersion": "003",
                                    "type": "text"
                                }
                            },
                            "properties": [
                                {
                                    "name": "key",
                                    "dataType": ["text"],
                                    "description": "Key Column"
                                },
                                {
                                    "name": "description",
                                    "dataType": ["text"],
                                    "description": "Description of Account Table Data",
                                    "moduleConfig": {
                                        "text2vec-openai": {
                                            "vectorizePropertyName": False,
                                            "skip": True,
                                            "vectorizer": "text2vec-openai"
                                        }
                                    },
                                    "indexFilterable": True,
                                    "indexSearchable": True
                                }
                            ]
                        }
                    ]
                }
        weaviate_client.schema.create(schema)
        Weaviate(weaviate_client,"key","description")
        print("Schema created successfully")
        print('##########################################################\n')
    except:
        print("Error Creating Schema")
        traceback.print_exc()

    return weaviate_client

def load_csv_data(weaviate_client):
    print('##########################################################')
    print('>>>>>>>>>>>>>>>  Loading data from CSV File  <<<<<<<<<<<<<')
    print('##########################################################')
    
    class_name = os.getenv("MASTER_CLASS_NAME")
    print("Initiated Data Load Process")
    
    # Loading CSV
    df = pd.read_csv(os.getenv("CSV_FILE_LOCATION"), usecols=['key', 'description'])

    # Create and add Weaviate objects for each row in the CSV
    for i, row in df.iterrows():
        # Display CSV DataLoaded
        # print('Row {}: {}'.format(i+1, row))
        
        key = row['key']
        description = row['description']

        print('Row Value, key:'+key+', description:'+description)
    
        # Create a Weaviate object with the Key and Description fields
        data_object = {
            "key": key,
            "description": description
        }

        # Add the object to Weaviate
        retry_attempts = 3
        retry_interval = 120  # seconds

        for attempt in range(retry_attempts):
            try:
                weaviate_client.data_object.create(data_object, class_name=class_name)
                # If the request succeeds, exit the loop
                break  
            except Exception as e:
                print("An error occurred:", str(e))
                time.sleep(retry_interval)

            if attempt == retry_attempts - 1:
                print("Maximum retry attempts reached. Exiting...")

        # print('Object {}: {} added to Weaviate'.format(i+1, data_object))

    print("CSV Data Loaded Successfully")
    print('##########################################################\n')

def main():
    print("\nStarted Updating Knowledge of DataMappingGPT")
    
    weaviate_client = create_weaviate_schema_and_class()
    load_csv_data(weaviate_client)

    print("Completed Updating Knowledge of DataMappingGPT\n")

if __name__ == '__main__':
    main()


# << Init pip Commands >>
#########################
# pip install --upgrade pip
# pip install python-dotenv weaviate-client langchain openai pandas tiktoken scikit-learn plotly matplotlib
# python load_data.py

# << Weaviate Endpoints >>
##########################
# https://<>.weaviate.network/v1/meta
# https://<>.weaviate.network/v1/schema
# https://<>.weaviate.network/v1/schema/Master