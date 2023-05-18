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


def read_csv(csv_filepath):
    df = pd.read_csv(csv_filepath, usecols=['source'])
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='\n') as temp_file:
        headers = ['source_text', 'Suggested key', 'Description', 'Certainity']
        writer = csv.writer(temp_file)
        writer.writerow(headers)

        for index, row in df.iterrows():
            file_path = temp_file.name
            k = str(row['source'])
            print(k)
            w1 = k
            w2 = k + " " + "Key column"
            w3 = k + " " + "Description"
            w4 = "99"
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
            file_output = gr.File()
        with gr.Row():
            upload_button = gr.UploadButton("Click to Upload a File 📁", file_types=["csv"], file_count="multiple", show_progress="True")
        upload_button.upload(upload_file, upload_button, file_output)
    demo.launch()


if __name__ == '__main__':
    main()
