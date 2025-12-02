# config.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY") 

if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in environment or .env")

genai.configure(api_key=API_KEY)

MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.0-flash")

def get_model():
    """Return configured Gemini model instance."""
    return genai.GenerativeModel(MODEL_NAME)
