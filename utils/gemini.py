from google import genai
from google.genai import types
import re
from typing import Optional, Dict, Any

# client = genai.Client(api_key="AIzaSyA4QRgymGf_wS2-j7uZ53KkIr2rUHiHAjU")

class LLMError(Exception):
    """Custom exception for LLM-related errors"""
    pass

def query_llm(prompt: str, client) -> str:
    """
    Query the LLM with error handling
    
    Args:
        prompt: The prompt to send to the LLM
        client: The Gemini client instance
    
    Returns:
        str: The LLM response text
        
    Raises:
        LLMError: If there's an error communicating with the LLM
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
            system_instruction="You are a math assistant helping researchers and students to solve problems and keep it short wih minimal bullet points and MathJax-style LaTeX"),
            contents=prompt
        )
        if not response or not response.text:
            raise LLMError("Empty response received from LLM")
        return response.text
    except Exception as e:
        raise LLMError(f"Error querying LLM: {str(e)}")

def classify_math_query(query: str, client) -> str:
    """
    Classify the type of math query with error handling
    
    Args:
        query: The math query to classify
        client: The Gemini client instance
    
    Returns:
        str: The classification result
        
    Raises:
        LLMError: If there's an error in classification
    # """
    try:
        prompt = (
            "Classify this math input as one of the following:\n"
            "1. 'equation' - if it should be solved like x^2 - 4 = 0\n"
            "2. 'convexity' - if its a problem of convexity with functions of one variable\n"
            "3. 'system' - if it is a system of equations like x + y = 2, x - y = 3\n\n"
            "4. 'derivative' - if it involves derivatives like differentiate x^2 or derivative of x^3 or any other form of derivative\n"
            "5. 'integral' - if it involves integrals like integrate x^2 dx or integral of x^3 or any other form of integral\n"
            f"Input: {query}\n Only respond with one of: equation, convexity, system, derivative, integral"
        )
        result = query_llm(prompt, client).strip().lower()
        print(result)
        if result not in ['equation', 'expression', 'system', 'convexity', 'derivative', 'integral']:
            raise LLMError(f"Invalid classification result: {result}")
        return result
    except Exception as e:
        raise LLMError(f"Error classifying math query: {str(e)}")

def extract_expression(query:str, client) -> str:
    """
    Extract mathematical expression from query with error handling
    
    Args:
        query: The query containing the mathematical expression
        client: The Gemini client instance
    
    Returns:
        str: The extracted mathematical expression
        
    Raises:
        LLMError: If there's an error extracting the expression
    """
    try:
        prompt = (
                "Extract the single, core mathematical expression from the user's query and return it as\n"
                "valid SymPy syntax (ready to pass into sympy.sympify or parse_expr). Do NOT include any\n"
                "explanations, labels, code fences, quotes, backticks, or additional text — return only the\n"
                "expression string itself.\n\n"

                "Strict rules:\n"
                "1) Use ** for exponentiation (never ^).\n"
                "2) Do not wrap the output in quotes or backticks (for example: not `diff(x**4, x)` or \"x**2\").\n"
                "3) For a single expression or equation, return exactly that expression (e.g. x**2 - 4 = 0).\n"
                "4) For a system of expressions/equations, return a single comma-separated string of the expressions\n"
                "   (for example: 2*x + 3*y - 5, x - y - 1) — do NOT add brackets or JSON, just the comma list.\n"
                "5) For derivatives use diff(f, x) (do not evaluate it unless asked). For integrals use Integral(f, x)\n"
                "   or Integral(f, (x, a, b)) for definite integrals. Use SymPy function names (diff, Integral, sin, cos, exp, etc.).\n"
                "6) Use plain ASCII math (no LaTeX macros). Convert LaTeX to SymPy form if present.\n"
                "7) Do not include explanatory text, headings, or punctuation before/after the expression. The output must be\n"
                "a single clean SymPy expression string with no surrounding whitespace, quotes or backticks.\n\n"

    f"Convert the following user query into that exact SymPy expression string:\n{query}"
)
        response = query_llm(prompt, client)
        if not response:
            raise LLMError("Failed to extract mathematical expression")
        return response.strip().splitlines()[0].strip()
    except Exception as e:
        raise LLMError(f"Error extracting expression: {str(e)}")

def format_llm_output(text):
    # Convert markdown bold to HTML
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
    # Convert LaTeX inline $...$ to MathJax
    text = re.sub(r"\$(.*?)\$", r"\\( \1 \\)", text)
    # Newlines to <br> for paragraph breaks
    return text.replace("\n", "<br>")