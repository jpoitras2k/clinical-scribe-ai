from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

if not key:
    print("No key found.")
else:
    client = genai.Client(api_key=key)
    print("Available models:")
    try:
        for m in client.models.list():
            print(f" - {m.name}")
    except Exception as e:
        print(f"Error listing models: {e}")
