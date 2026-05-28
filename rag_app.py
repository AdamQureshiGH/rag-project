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
        outline_prompt = (
            "Create a 3-bullet-point outline explaining why virtual environments are important in Python"
            "Provide only the bullet points nothing else"
        )

        print("Requesting outline from Gemini...")
        outline_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=outline_prompt
        )
        
        outline_text = outline_response.text
        print(f"Outline captured:\n{outline_text}")

        expansion_prompt = (
            f"Here is a 3 bullet point outline:\n"
            f"{outline_text}\n"
            f"Now use this outline by writing a single cohesive paragraph that explains these points to a newbie developer"
        )

        final_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=expansion_prompt
        )

        return {
            "status": "success",
            "final_output": final_response.text
        }
    except Exception as e:
        raise ValueError(f"Gemini API Call Failed: {str(e)}")