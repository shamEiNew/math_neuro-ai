import sympy as sp
from sympy import *
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

transformations = (standard_transformations + (implicit_multiplication_application,))



def solve_convexity(expr_str):
    try:
        symbols = sp.symbols('x y z')  # expand if needed
        expr = parse_expr(expr_str)
        x = symbols[0] if expr.free_symbols else sp.symbols('x')
        derivative = sp.diff(expr, x)
        second_derivative = sp.diff(derivative, x)
        is_convex = sp.simplify(second_derivative >= 0)
        convex_condition = second_derivative >= 0

        # Reduce inequality to find convex domain
        convex_domain = sp.reduce_inequalities([convex_condition], x)
        return {
            "expression": sp.latex(expr),
            "first_derivative": sp.latex(derivative),
            "second_derivative": sp.latex(second_derivative),
            "is_convex": sp.latex(is_convex),
            "convex_domain":sp.latex(convex_domain)
        }
    except Exception as e:
        return {"error": str(e)}
    

from sympy import Matrix

def analyze_multivariable_convexity(expr_str):
    try:
        vars = sorted(list({str(sym) for sym in sp.sympify(expr_str).free_symbols}))
        symbols = sp.symbols(vars)
        expr = sp.sympify(expr_str)

        gradient = [sp.diff(expr, var) for var in symbols]
        hessian = Matrix([[sp.diff(g, var) for var in symbols] for g in gradient])

        # Use leading principal minors test for PSD
        hessian_det = [hessian[:i, :i].det() for i in range(1, len(symbols)+1)]
        psd_check = all(sp.simplify(det >= 0) for det in hessian_det)

        return {
            "expression": sp.latex(expr),
            "variables": vars,
            "gradient": [sp.latex(g) for g in gradient],
            "hessian": sp.latex(hessian),
            "is_convex": str(psd_check)
        }
    except Exception as e:
        return {"error": str(e)}
