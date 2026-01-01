from google import genai
from dotenv import load_dotenv
import os
import time

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

if not key:
    print("No API Key found in environment!")
    exit(1)

client = genai.Client(api_key=key)

candidates = [
    "gemini-2.0-flash",
    "gemini-2.0-flash-exp",
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro",
]

print(f"Testing API Key with various models...\n")

for model in candidates:
    print(f"--- Testing {model} ---")
    try:
        response = client.models.generate_content(
            model=model,
            contents="Say 'Hello' if you can hear me."
        )
        print(f"SUCCESS! Model '{model}' is working.")
        print(f"Response: {response.text.strip()}\n")
    except Exception as e:
        print(f"FAILED. Error: {e}\n")
    
    time.sleep(1) # Be nice to the API
