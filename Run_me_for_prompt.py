import gradio as gr
import os
import openai
from dotenv import load_dotenv
from openai.embeddings_utils import get_embedding
import pandas as pd
import weaviate
import json

# Example DataFrame
data = {
    'Name': ['John', 'Alice', 'Bob'],
    'Age': [25, 30, 35],
    'City': ['New York', 'London', 'Paris']
}
df = pd.DataFrame(data)


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


def positive(text):
    print('submit is clicked')
    print(df)
    table_html = df.to_html()  # Generate HTML table code
    return table_html

def negative(text):
    print('clear is clicked')
    text=""
    df = pd.DataFrame()
    return text,df

def main():
    with gr.Blocks(title="OFSLL DataMapper") as demo:
        with gr.Row():
            gr.Markdown(
                """
                # OFSLL Data Mapper!
                    Please Enter Description and Press Enter.
                """
            )
        with gr.Row():
            input_box = gr.Textbox(lines=1)
        with gr.Row():
            submit_button = gr.Button("Submit")
            clear_button = gr.Button("Clear")
        with gr.Row():
             output_html = gr.outputs.Dataframe(type='pandas')

        submit_button.click(positive1, inputs=[input_box],outputs=[output_html])
        clear_button.click(negative, inputs=[input_box], outputs=[input_box,output_html])

    demo.launch()

if __name__ == '__main__':
    main()
    