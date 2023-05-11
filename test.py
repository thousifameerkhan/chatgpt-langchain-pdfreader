import openai
import os
from dotenv import load_dotenv
from weaviate import Client
from weaviate.exceptions import UnexpectedStatusCodeException

# Configure OpenAI API
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configure Weaviate connection
weaviate_url = os.getenv("WEAVIATE_URL")

# Creating Weaviate Client to interact VectorDB
weaviate_client = Client(weaviate_url)

# User input for semantic search
user_query = input("Enter your search query: ")

# Generate embeddings for user query using the OpenAI API
response = openai.Completion.create(
    engine='text-davinci-003',
    prompt=user_query,
    max_tokens=4000
)
user_embeddings = response.choices[0].text.strip()
print('User Input Vector: '+user_embeddings)

# Create a Weaviate object with the user query
query_object = {
    "description": user_embeddings
}

# Perform the semantic search in Weaviate
try:
    search_results = weaviate_client.schema.query_object(
        class_name=os.getenv("MASTER_CLASS_NAME"),
        vector=query_object,
        limit=10
    )
    for result in search_results['data']['searchResults']:
        print(result['entity']['key'])
        # Access other relevant information from the search results as needed
except UnexpectedStatusCodeException as e:
    print(f"Semantic search failed: {e}")