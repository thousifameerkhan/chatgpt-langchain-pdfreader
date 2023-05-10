import openai
import requests

# Configure OpenAI API
openai.api_key = "YOUR_OPENAI_API_KEY"

# Configure Weaviate connection
weaviate_url = "https://mapping-data-gpt-v3n86qqk.weaviate.network/v1"
headers = {"Content-Type": "application/json"}

# Define OpenAI GPT-3 completion function
def complete_prompt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    return response.choices[0].text.strip()

# Define Weaviate semantic search function
def semantic_search(query):
    query = f'{{Find the key where Description: "{query}"}}'
    response = requests.post(f"{weaviate_url}/graphql", headers=headers, data=query)
    response_json = response.json()
    print(response_json)
    concepts = response_json["data"]["Get"]["Concepts"]["result"]
    return [concept["id"] for concept in concepts]

# Main program
def main():
    while True:
        user_query = input("Enter your search query (or 'q' to quit): ")
        if user_query == 'q':
            break
        semantic_results = semantic_search(user_query)
        for result in semantic_results:
            prompt = f"What is the meaning of {result}?"
            completion = complete_prompt(prompt)
            print(f"Result: {result}\nExplanation: {completion}\n")

if __name__ == "__main__":
    main()
