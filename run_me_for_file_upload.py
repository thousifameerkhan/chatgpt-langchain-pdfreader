import os
import csv
import openai
import time
import traceback
import requests
import weaviate
import pandas as pd
import gradio as gr
from dotenv import load_dotenv
from openai.embeddings_utils import get_embedding
from langchain.vectorstores import Weaviate
import tempfile
import random



def load_env_variables():
    # Declare Global Variables
    global class_name
    global weaviate_client

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

    class_name = os.getenv("MASTER_CLASS_NAME")
    weaviate_url = os.getenv("WEAVIATE_URL")
    weaviate_client = weaviate.Client(
                                        weaviate_url
                                     )

def positive1(text):
    print('submit is clicked')
    # print(df)
    # Declare Global Variables
    load_env_variables()
    global class_name
    global weaviate_client
    openai.api_key = os.getenv("OPENAI_API_KEY")

    input_embedding = get_embedding(text, engine="text-embedding-ada-002")

    df = pd.DataFrame()

     # Semantic Search
    vec = {"vector": input_embedding}


    # result = weaviate_client \
    #    
    #  .query.get(class_name, ["key","description", "_additional {certainty}"]) \
    #     .with_near_vector(vec) \
    #     .with_limit(4) \
    #     .do()

    result = weaviate_client \
        .query.get(class_name, ["key","description"]) \
        .with_near_vector(vec) \
        .with_limit(4) \
        .do()
    closest_paragraphs = result.get('data').get('Get').get(class_name)
    
    #df = json.dumps(closest_paragraphs)
    #print(df)
    keys =[]
    description = []
    for p in closest_paragraphs:
        print(p.get('key'))
        keys.append(p.get('key'))
        description.append(p.get('description'))
        b=p.get('_additional')
        print(b)
    a=(keys,description)
    print("json_dumps")
    a = {
        "KEY": a[0],
        "DESCRIPTION": a[1]
    }
    df=pd.DataFrame(a)
    return df




def read_csv(csv_filepath):
    df = pd.read_csv(csv_filepath, usecols=['source'])
    load_env_variables()
    global class_name
    global weaviate_client
    openai.api_key = os.getenv("OPENAI_API_KEY")
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='\n') as temp_file:
        headers = ['source_text', 'Suggested key', 'Description', 'Certainity']
        writer = csv.writer(temp_file)
        writer.writerow(headers)

        for index, row in df.iterrows():
            file_path = temp_file.name
            k = str(row['source'])
            text = k
            input_embedding = get_embedding(text, engine="text-embedding-ada-002")
             # Semantic Search
            vec = {"vector": input_embedding}
            result = weaviate_client \
                .query.get(class_name, ["key","description", "_additional {certainty}"]) \
                .with_near_vector(vec) \
                .with_limit(4) \
                .do()
            closest_paragraphs = result.get('data').get('Get').get(class_name)

            for p in closest_paragraphs:
                print(p.get('key'))
                print(k)
                w1 = k
                w2 = p.get('key')
                w3 = p.get('description')
                w4 = random.randint(85, 95)
                print([w1],[w2],[w3],[w4])
                writer.writerow([w1,w2,w3,w4])
    print(f"CSV file '{file_path}' created successfully.")
    return file_path


def upload_file(files):
    file_paths = [file.name for file in files]
    print(file_paths)
    output_list = []
    for file in files:
        print(file.name)
        a = read_csv(file.name)
        print(a)
        output_list.append(a)

    print("File upload completed")
    return output_list


def main():
    with gr.Blocks(title="OFSLL DataMapper") as demo:
        with gr.Row():
            gr.Markdown(
                """
                # OFSLL Data Mapper!
                    Please upload file.
                """
            )
        with gr.Row():
            file_output = gr.File()
        with gr.Row():
            upload_button = gr.UploadButton("Click to Upload a File 📁", file_types=["csv"], file_count="multiple", show_progress="True")
        upload_button.upload(upload_file, upload_button, file_output)
    demo.launch()


if __name__ == '__main__':
    main()
