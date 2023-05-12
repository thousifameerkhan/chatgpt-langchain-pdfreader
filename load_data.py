import os
import openai
import time
import traceback
import requests
import weaviate
import pandas as pd
from dotenv import load_dotenv
from openai.embeddings_utils import get_embedding
from langchain.vectorstores import Weaviate

weaviate_client = None
class_name = None
csv_filepath = None

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
    
    # Declare Global Variables
    global csv_filepath
    global class_name
    global weaviate_client

    # Setting Variables
    weaviate_url = os.getenv("WEAVIATE_URL")
    class_name = os.getenv("MASTER_CLASS_NAME")
    schema_url = f"{weaviate_url}/schema"
    class_url = f"{weaviate_url}/v1/schema/{class_name}"
    openai.api_key = os.getenv("OPENAI_API_KEY")
    csv_filepath = os.getenv("CSV_FILE_LOCATION")

    # Creating Weaviate Client to interact VectorDB
    weaviate_client = weaviate.Client(
                                        weaviate_url
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
                            "vectorizer": "none",
                            "properties": [
                                {
                                    "name": "key",
                                    "dataType": ["text"],
                                    "description": "Key Column"
                                },
                                {
                                    "name": "description",
                                    "dataType": ["text"],
                                    "description": "Description of Master Table Key Data"
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

def load_csv_data():
    print('##########################################################')
    print('>>>>>>>>>>>>>>>  Loading data from CSV File  <<<<<<<<<<<<<')
    print('##########################################################')
    
    print("Initiated Data Load Process")
    
    # Declare Global Variables
    global csv_filepath
    global class_name
    global weaviate_client

    # Loading CSV
    df = pd.read_csv(csv_filepath, usecols=['key', 'description'])
    
    # Updating Embedding
    retry_attempts = 3
    retry_interval = 65
    new_embedding= []

    for index, row in df.iterrows():
        for attempt in range(retry_attempts):
            try:
                embedding = get_embedding(row['description'], engine="text-embedding-ada-002")
                new_embedding.append(embedding)
                print('Added Index: ' + str(index) + ' & Key: ' + row['key'])
                break
            except Exception as e:
                time.sleep(retry_interval)
                print(str(e))
        else:
            print("Maximum retry attempts reached. Exiting...")

    df['embedding']=new_embedding    

    # Create and add Weaviate objects for each row in the CSV
    for i, row in df.iterrows():
        # Display CSV DataLoaded
        # print('Row {}: {}'.format(i+1, row))
        
        key = row['key']
        description = row['description']
        vector = row['embedding']

        print('Row Value, key:'+key+', description:'+description)
    
        # Create a Weaviate object with the Key and Description fields
        data_object = {
            "key": key,
            "description": description
        }

        # Add the object to Weaviate
        weaviate_client.data_object.create(data_object, class_name=class_name, vector=vector)
        # print('Object {}: {} added to Weaviate'.format(i+1, data_object))

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
# pip install python-dotenv weaviate-client langchain openai pandas tiktoken scikit-learn plotly matplotlib
# python load_data.py

# << Weaviate Endpoints >>
##########################
# https://<>.weaviate.network/v1/meta
# https://<>.weaviate.network/v1/schema
# https://<>.weaviate.network/v1/schema/Master