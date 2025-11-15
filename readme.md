---
project: Math Research Assistant
status: in progress
features:
  - Convexity analysis (univariate & multivariate)
  - Equation solving
  - System of equations
  - Symbolic validation using SymPy
  - Derivative & integral computation
  - LLM-based explanation using Gemini
  - Experimental ML-based symbolic classifier (separate branch: ml-classify)
roadmap:
  current:
    - Multivariable convexity support
    - Derivative & integral handling
  next:
    - Solve equations and systems
    - Improve accuracy of ML classifier
  future:
    - Geometry solver (AlphaGeometry2)
    - Plotting support
    - Custom math DSL
    - Persistent dataset for benchmarking
---

# 🧠 Math Research Assistant

The **Math Research Assistant** is a prototype that integrates:

- **LLM-powered mathematical reasoning** (Google Gemini),
- **Symbolic algebra** using **SymPy**, and  
- **Early-stage ML-based classification** of symbolic expressions.

It is designed as an experimental research platform for building automated mathematical reasoning systems.

> ⚠️ **This project is actively under development.  
> Many modules — especially the ML classifier — are experimental and may contain bugs.**

---

# ✨ Features

### ✔ Symbolic Math Engine
- Convexity analysis (univariate & multivariate)  
- Derivative analysis (critical points, monotonicity, inflection points)  
- Integral parsing (indefinite & definite)  
- Equation solving (linear & non-linear)
- Systems of equations (classification + solving)
- SymPy-based validation of user queries  
- Comprehensive LaTeX rendering via MathJax

### ✔ LLM-Enhanced
- Gemini-based natural language → SymPy expression translation  
- Step-by-step explanations  
- Correction and interpretation of ambiguous mathematical text  

### ✔ UI Layer
- Clean black-and-white themed Flask web interface  
- Inline LaTeX rendering  
- Friendly error reporting  

---

# 🔬 Experimental: ML-Based Equation Classification (`ml-classify` branch)

A separate development branch, **`ml-classify`**, contains a new subsystem:

### 🎯 Goal  
Build a **high-accuracy classifier** that identifies the type of symbolic expression before routing:

- `equation`
- `system_of_equations`
- `convexity_problem`
- `derivative`
- `integral`
- `expression`
- (future) `geometry`, `limits`, `series`, etc.

### 🧩 Model Details
- Built using **HuggingFace Transformers**
- Custom dataset of **SymPy-formatted expressions**
- Trained for:  
  - linear equations  
  - nonlinear equations  
  - multivariable systems  
  - convexity/optimization expressions  
  - derivatives: `diff(x**3, x)`  
  - integrals: `Integral(sin(x), x)`  

### ⚠️ Current Status
- [Juoyter notebook](https://colab.research.google.com/drive/1ONuLHDp8Y93U_RYXAwJANP8-FD4kpxmX#scrollTo=QxKzjEALgUPF)
- The model is functional but **accuracy is still below expected production level**  
- The dataset is being expanded  
- Class imbalance & long expression formatting still cause misclassification  
- SymPy string variations are being normalized  

> 🧪 **This classifier is experimental**.  
> It is not used by the main branch yet and may misclassify complex or nested expressions.

---

# 🚀 Current Capabilities (Main Branch)

- ✔ Robust convexity detection using symbolic derivatives  
- ✔ Expression extraction from natural language  
- ✔ Structured symbolic validation  
- ✔ Derivative + integral support  
- ✔ Error-resistant pipeline integrating Gemini + SymPy  
- ✔ Clean mathematical UI with MathJax  

---

# 📌 Roadmap

### 🟢 **Current Work**
- Improving multivariable convexity analysis  
- Completing derivative & integral framework  
- Improving LLM → SymPy extraction prompt stability  

### 🟡 **Next Steps**
- Fully integrate equation/system solving  
- Refine ML classifier accuracy (expand dataset, add noise examples)  
- Introduce fallback architecture (ML → LLM → deterministic)

### 🔵 **Future Enhancements**
- Geometry solver using **AlphaGeometry2**  
- Symbolic plotting (2D & 3D)  
- Custom math DSL for programmatic reasoning  
- Persistent benchmark dataset for performance tracking  

---

# 🛠 Installation & Setup

```bash
pip install -r requirements.txt
export GEMINI_API_KEY=your_key_here
python app.py
