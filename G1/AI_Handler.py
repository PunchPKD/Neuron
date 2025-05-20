from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('AI_TOKEN')

client = genai.Client(api_key=token)

def response(convo):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="summarise this conversation in paragraph \n"+convo,
        config=types.GenerateContentConfig(
            max_output_tokens=100,
            temperature=1
        )
    )
    return response
