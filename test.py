import openai
import os
from dotenv import load_dotenv


# Configure OpenAI API
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

text = "Account Number"
model = "text-davinci-003"

response = openai.Completion.create(
  engine=model,
  prompt=text,
  max_tokens=4000,
  n=1,
  stop=None
)

# vector = response.choices[0].logprobs.token_logits[0]

# print(vector)

print(response)