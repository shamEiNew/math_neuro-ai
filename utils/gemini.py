from google import genai
from google.genai import types
import re

# client = genai.Client(api_key="AIzaSyA4QRgymGf_wS2-j7uZ53KkIr2rUHiHAjU")

def classify_math_query(query, client):
    prompt = (
        "Classify this math input as one of the following:\n"
        "1. 'equation' - if it should be solved like x^2 - 4 = 0\n"
        "2. 'expression' - if it should be analyzed like f(x) = x^2 or x^3\n"
        "3. 'system' - if it is a system of equations like x + y = 2, x - y = 3\n\n"
        f"Input: {query}\n Only respond with one of: equation, expression, system"
    )
    result = query_llm(prompt, client).strip().lower()
    return result

def query_llm(prompt, client):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
        system_instruction="You are a math assistant helping researchers and students to solve problems and keep it short wih minimal bullet points and MathJax-style LaTeX"),
        contents=prompt
    )
    return response.text

def extract_expression(query, client):
    prompt = (
        "Extract and convert the main mathematical expression or equation from the following query "
        "into valid SymPy syntax using ** for powers. Do not include any explanation, prefix, or formatting:\n\n"
        f"{query}\n\n"
        "If its a equation. for example,'x^2-4=0' return 'x**2-4=0'"
    )
    response = query_llm(prompt, client)
    return response.strip().splitlines()[0].strip()

def format_llm_output(text):
    # Convert markdown bold to HTML
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
    # Convert LaTeX inline $...$ to MathJax
    text = re.sub(r"\$(.*?)\$", r"\\( \1 \\)", text)
    # Newlines to <br> for paragraph breaks
    return text.replace("\n", "<br>")
