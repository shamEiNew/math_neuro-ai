---
project: Math Research Assistant
status: in progress
features:
  - Convexity analysis (univariate & multivariate)
  - Equation solving
  - System of equations
  - Symbolic validation using SymPy
  - LLM-based explanation using Gemini
roadmap:
  current:
    - Multivariable convexity support
  next:
    - Solve equations and systems
  future:
    - Geometry solver (AlphaGeometry2)
    - Plotting support
    - Custom math DSL
    - Persistent dataset for benchmarking
---

# 🧠 Math Research Assistant

This is a prototype tool that integrates **LLM explanations (Gemini)** with **symbolic reasoning (SymPy)** to solve and validate mathematical problems. It's designed for researchers, students, and developers working with math automation.

## ✨ Features

- Symbolic validation for convexity (single and multivariable)
- LLM-generated explanations with LaTeX rendering
- Automatic extraction of math expressions
- Validation of expressions using custom SymPy logic
- Roadmap-based extensibility

## 🚀 Current Capabilities

- Convexity detection via second-derivative tests and symbolic inequalities
- Math expression extraction from natural language
- LaTeX-rendered explanations (MathJax)
- Custom UI built with Flask

## 📌 Roadmap

### ✅ Current
- Support for multivariable convex problems

### 🔜 Next
- Equation solving and systems of equations

### 💡 Future
- Geometry solver using AlphaGeometry2
- Plotting symbolic functions
- A custom math DSL
- Model benchmarking using a persistent dataset

## 🛠 Setup

```bash
pip install -r requirements.txt
export GEMINI_API_KEY=your_key_here
python app.py
