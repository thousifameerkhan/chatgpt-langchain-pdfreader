import os
import openai
from dotenv import load_dotenv
from openai.embeddings_utils import get_embedding
import pandas as pd
import weaviate

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

def main():
  # Declare Global Variables
  load_env_variables()
  global class_name
  global weaviate_client
  openai.api_key = os.getenv("OPENAI_API_KEY")
  
  # Reading User Input & Embedding
  prompt = input('Enter field name - ')
  input_embedding = get_embedding(prompt, engine="text-embedding-ada-002")

  # Semantic Search
  vec = {"vector": input_embedding}
  result = weaviate_client \
        .query.get(class_name, ["key","description", "_additional {certainty}"]) \
        .with_near_vector(vec) \
        .with_limit(4) \
        .do()
  print(result)


if __name__ == "__main__":
  main()