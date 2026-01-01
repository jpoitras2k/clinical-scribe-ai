from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("GEMINI_API_KEY")
print(f"Key found: {'Yes' if key else 'No'}")

if key:
    client = genai.Client(api_key=key)
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents="Test"
        )
        print("Model 'gemini-2.0-flash' works!")
    except Exception as e:
        print(f"Model 'gemini-2.0-flash' failed: {e}")
        
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents="Test"
        )
        print("Model 'gemini-2.0-flash-exp' works!")
    except Exception as e:
        print(f"Model 'gemini-2.0-flash-exp' failed: {e}")
