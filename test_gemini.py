import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# List available Gemini models
models = genai.list_models()
for model in models:
    print(model.name, "-", model.supported_generation_methods)
