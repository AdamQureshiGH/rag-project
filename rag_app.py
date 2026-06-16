import os 
import time

from dotenv import load_dotenv


#web framework that handles the HTTP requests and responses
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai

load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the .env file")

client = genai.Client()
app = FastAPI()
class QueryRequest(BaseModel):
    question: str


def validate_user_input(text: str):
    if text is None or text.strip() == "":
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    if len(text) < 5:
        raise HTTPException(status_code=400, detail="Question is too short")
    if len(text) > 500:
        raise HTTPException(status_code=400, detail="Question is too long")
    return text

def validate_model_output(text: str):
    if text is None or text.strip() == "":
        raise HTTPException(status_code=500, detail="AI returned an empty response")
    if len(text) < 10:
        raise HTTPException(status_code=500, detail="AI response is too short")
    return text
def review_model_output(original_answer: str):
    review_prompt = f"""You are reviewing an AI-generated response.
        Your job:
        - If the response is unclear, incomplete, or poorly written, improve it.
        - If the response is already good, return it unchanged.

    AI response to review:
    {original_answer}"""

    review_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=review_prompt
    )
    return review_response.text        

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
        
        time.sleep(2)
        
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
@app.post("/query")
def query_ai(request: QueryRequest):
    try:
        # 1. Check user input at the gate
        validate_user_input(request.question)
        
        # 2. Fire the primary model generation request
        primary_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=request.question
        )
        raw_answer = primary_response.text
        
        validate_model_output(raw_answer)
        
        time.sleep(2)
        
        reviewed_answer = review_model_output(raw_answer)
        
        return {
            "question": request.question,
            "answer": reviewed_answer
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query Pipeline Failed: {str(e)}")