from utils.symbolic.solve_convexity import *
from utils.symbolic.solve_equation import *
from sympy import sympify


from sympy import sympify

def route_problem(expr_str):
    expr = sympify(expr_str)
    free_vars = expr.free_symbols

    if len(free_vars) > 1:
        return analyze_multivariable_convexity(expr_str)
    else:
        return solve_convexity(expr_str)


def route_query(query_type, expr_str):
    """
    Routes the symbolic expression to the correct SymPy validator based on query_type.
    """
    if query_type == "expression":
        return route_problem(expr_str)
    elif query_type == "equation":
        return solve_equation(expr_str)
    else:
        return {"error": f"Unsupported query type: {query_type}"}
