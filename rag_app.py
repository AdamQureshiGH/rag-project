import os 
from dotenv import load_dotenv

#web framework that handles the HTTP requests and responses
from fastapi import FastAPI

load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the .env file")


#This creates an instance of the web server.
#Think of this as your "Main" application object. 
#It’s the engine that will listen for connections.
app = FastAPI()

#Here, it tells FastAPI:Here, it tells FastAPI: "Whenever a user visits the URL path /health using a GET request, run this health_check function and send the result back to them." "Whenever a user visits the URL path /health using a GET request, 
#run this health_check function and send the result back to them."
@app.get("/health")
def health_check():
    return {"status": "running", "api_key_loaded": bool(api_key)}
