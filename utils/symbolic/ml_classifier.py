import torch
import sympy as sp
from sympy import Derivative, Integral, Eq
from transformers import AutoTokenizer, AutoModelForSequenceClassification


MODEL_DIR = "shamEiNew/symbolic-math-classifier"
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
model.eval()

id2label = model.config.id2label


# -------------------------
# Deterministic classifier
# -------------------------
def deterministic_classify(expr_str):
    """
    Returns (label, confidence) or (None, None)
    """
    try:
        obj = sp.sympify(expr_str)

        # Derivative
        if obj.has(Derivative):
            return "derivative", 1.0

        # Integral
        if obj.has(Integral):
            return "integral", 1.0

        # Equality (single equation)
        if isinstance(obj, sp.Equality) or isinstance(obj, sp.Relational):
            lhs = obj.lhs - obj.rhs
            syms = list(lhs.free_symbols)

            if syms and lhs.is_polynomial(*syms):
                maxdeg = max(lhs.as_poly(v).degree() for v in syms if lhs.as_poly(v) is not None)
                return ("equation_linear" if maxdeg <= 1 else "equation_nonlinear"), 1.0

            return "equation_nonlinear", 1.0

        # Systems (list/tuple)
        if isinstance(obj, (list, tuple)):
            is_linear = True
            for eq in obj:
                if isinstance(eq, (Eq, sp.Relational)):
                    lhs = eq.lhs - eq.rhs
                else:
                    lhs = eq

                if lhs.is_polynomial(*lhs.free_symbols):
                    degs = [lhs.as_poly(v).degree() for v in lhs.free_symbols if lhs.as_poly(v)]
                    if any(d > 1 for d in degs):
                        is_linear = False
                else:
                    is_linear = False

            return ("system_linear" if is_linear else "system_nonlinear"), 1.0

    except Exception:
        pass

    return None, None


# -------------------------
# ML classifier (safe)
# -------------------------
def ml_classify(expr_str, threshold=0.70):
    """
    Model classification with safe fallback.
    Returns (label, confidence).
    Uses threshold to reject low-confidence predictions.
    """

    # Canonicalize expressions for consistent model input
    try:
        obj = sp.sympify(expr_str)
        expr_str = sp.srepr(obj)
    except:
        pass

    try:
        enc = tokenizer(expr_str, truncation=True, padding=True, max_length=256, return_tensors="pt")
        with torch.no_grad():
            out = model(**enc)
        logits = out.logits.squeeze()
        probs = torch.softmax(logits, dim=-1).tolist()

        pred_id = int(torch.argmax(logits).item())
        conf = float(probs[pred_id])
        label = id2label[pred_id]

        if conf >= threshold:
            return label, conf
        else:
            return None, conf  # rejected low confidence

    except Exception as e:
        print("ML classification error:", e)
        return None, None


# -------------------------
# Unified classifier
# -------------------------
def classify(expr_str):
    """
    1. Try deterministic rules → most accurate
    2. Try ML model → robust
    3. Fallback → unknown
    """
    # Step 1 — Deterministic
    d_label, d_conf = deterministic_classify(expr_str)
    if d_label:
        return d_label, d_conf, "deterministic"

    # Step 2 — ML model
    m_label, m_conf = ml_classify(expr_str)
    if m_label:
        return m_label, m_conf, "ml"

    # Step 3 — Final fallback
    return "unknown", 0.0, "fallback"
