from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('AI_TOKEN')

client = genai.Client(api_key=token)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="summarise this conversation in paragraph" \
    "Mukesh : Aur Bhai kaisa Hai?" \
    "Suresh : Thik hu tu apna bata" \
    "Mukesh : Mai bhi thik hu",
    config=types.GenerateContentConfig(
        max_output_tokens=100,
        temperature=1
    )
)

print(response.text)