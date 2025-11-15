import os
def configure_genai():
    from google import genai
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))