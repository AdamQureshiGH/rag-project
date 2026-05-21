import os 
from dotenv import load_dotenv

#web framework that handles the HTTP requests and responses
from fastapi import FastAPI
from google import genai

load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the .env file")

client = genai.Client()
app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "running", "api_key_loaded": bool(api_key)}

@app.get("/test-gemini")
def test_gemini():
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Explain what an LLM is and how it works!"
        )
        return {"response": response.text}

    except Exception as e:
        raise ValueError(f"Gemini API Call Failed: {str(e)}")