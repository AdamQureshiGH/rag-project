# Learning Gen AI

This repository contains my learning project for the Fusion Cyber - GenAI Secure Coding course.

This project will be built incrementally each week.

##Sections
/health endpoint:

The health_check() function executes. It asks the OS through os.getenv for the API key in the internal RAM block.

The function will then return a python dictionary that says whether the API key is loaded, and FastAPI will turn the into JSON and send it back through port 8000 to the browser.

/test_gemini endpoint:

Step 1: Asks Gemini for a 3-bullet outline about Python virtual environments.

Step 2: Takes those exact bullets, injects them into an expansion prompt, and requests a cohesive explanation paragraph.

Notes:

First the os makes a process for our python script

load_dotenv will read our .env file and write our GEMINI_API_KEY into the process's internal environment block

FastAPI will then scan rag_app.py, and it is set so if someone goes to /health it runs the health_check() function which will return whether the API key is set up

So then when you type http://127.0.0.1:8000/health into your browser and hit enter:

The browser sees 127.0.0.1 and knows, " I'm talking to this same computer."
It wraps a request in an HTTP GET envelope and sends it to Port 8000.
The OS sees the packet for Port 8000 and hands it to your waiting Python Process.

