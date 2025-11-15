from flask import Flask, request, render_template
from utils.gemini import query_llm, format_llm_output, extract_expression, classify_math_query, LLMError
from utils.symbolic.solve_convexity import solve_convexity
from utils.router import route_query
import time
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    explanation = ""
    math_result = {}
    error_message = None
    
    if request.method == "POST":
        query = request.form["query"]
        try:
            # Classify the query
            category = classify_math_query(query, client) 
            # Get LLM explanation
            raw_explanation = query_llm(f"{query}", client)
            explanation = format_llm_output(raw_explanation)
            
            # Step 3: Extract and process mathematical expression
            expr = extract_expression(query, client)
            print(expr)
            math_result = route_query(category, expr)
            
            # Check for errors in math_result
            if "error" in math_result:
                error_message = f"Mathematical Error: {math_result['error']}"
                math_result = {}
                
        except LLMError as e:
            error_message = str(e)
            explanation = ""
            math_result = {}
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            explanation = ""
            math_result = {}

    return render_template(
        "index.html",
        explanation=explanation,
        math_result=math_result,
        error_message=error_message
    )

if __name__ == "__main__":
    from config import configure_genai
    client = configure_genai()
    app.run(debug=True)