from flask import Flask, request, render_template
from utils.gemini import query_llm, format_llm_output, extract_expression, classify_math_query
from utils.symbolic.solve_convexity import solve_convexity
from utils.router import route_query
import time
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    explanation = ""
    math_result = {}
    if request.method == "POST":
        query = request.form["query"]
        category = classify_math_query(query, client)
        raw_explanation = query_llm(f"{query}",client)
        explanation = format_llm_output(raw_explanation)
        expr = extract_expression(query, client)
        math_result = route_query(category, expr)

    return render_template("index.html", explanation=explanation, math_result=math_result)

if __name__ == "__main__":
    from config import configure_genai
    client = configure_genai()
    app.run(debug=True)