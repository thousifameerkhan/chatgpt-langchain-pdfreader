import gradio as gr
import os
import openai
from dotenv import load_dotenv
from openai.embeddings_utils import get_embedding
import pandas as pd
import weaviate

valid_file = True
weaviate_client = None
class_name = None

def load_env_variables():
    # Declare Global Variables
    global class_name
    global weaviate_client

    # Loading API Key
    load_dotenv()

    print('\n##########################################################')
    print('>>>>>>>>>>>>>  Displaying Environment Variables <<<<<<<<<<')
    print('##########################################################')
    print('Loaded OpenAI API Key     -> ' + os.getenv("OPENAI_API_KEY"))
    print('Loaded Weaviate URL       -> ' + os.getenv("WEAVIATE_URL"))
    print('Loaded CSV Location       -> ' + os.getenv("CSV_FILE_LOCATION"))
    print('Loaded Master ClassName   -> ' + os.getenv("MASTER_CLASS_NAME"))
    print('##########################################################\n')

    class_name = os.getenv("MASTER_CLASS_NAME")
    weaviate_url = os.getenv("WEAVIATE_URL")
    weaviate_client = weaviate.Client(weaviate_url)


def prompt_text(prompt):
    # Declare Global Variables
    load_env_variables()
    global class_name
    global weaviate_client
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Embedding User Input
    input_embedding = get_embedding(prompt, engine="text-embedding-ada-002")

    # Semantic Search
    vec = {"vector": input_embedding}
    result = weaviate_client \
        .query.get(class_name, ["key", "description", "_additional {certainty}"]) \
        .with_near_vector(vec) \
        .with_limit(4) \
        .do()
    print(result)

    output = []
    closest_paragraphs = result.get('data').get('Get').get(class_name)
    for p in closest_paragraphs:
        output.append(p.get('key'))

    return output


def add_text(history, text):
    global valid_file

    print("In Add Text")
    matched_columns = prompt_text(text)
    if matched_columns:
        output_table = pd.DataFrame(matched_columns, columns=["Matched Columns"])
        history = history + [(text, output_table)]
    else:
        history = history + [(text, "No matching columns found")]

    return history, ""


def add_file(history, file):
    global valid_file

    print("In Add File")
    if file.name.endswith(".csv"):  # Only accept CSV files
        valid_file = True
        history = history + [("Uploaded file - " + file.name, None)]
    else:
        valid_file = False
        history = history + [(None, "Upload only CSV Files")]
    return history


def bot(history):
    global valid_file
    print("In Bot Response")

    valid_file = True
    return history


def main():
    with gr.Interface(fn=bot, inputs="text", outputs="text") as iface:
        iface.launch()


if __name__ == '__main__':
    main()
