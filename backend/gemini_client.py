
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(Path(__file__).resolve().parent / ".env")

key = os.getenv("GEMINI_API_KEY")

if not key:
    raise RuntimeError("GEMINI_API_KEY missing")

client = genai.Client(
    api_key=key,
    http_options=types.HttpOptions(timeout=30000)
)

def ask_gemini(prompt: str) -> str:
    print("Connecting to Gemini...", flush=True)

    try:
        response = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )

        print("Gemini responded.", flush=True)
        return response.output_text or "Empty response"

    except Exception as error:
        print(f"Gemini connection failed: {type(error).__name__}: {error}")
        raise   
