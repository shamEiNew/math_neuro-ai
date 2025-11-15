from utils.symbolic import *
from sympy import sympify
from sympy.parsing.sympy_parser import parse_expr
import sympy as sp


from sympy import sympify

def route_problem(expr_str):
    expr = sympify(expr_str)
    free_vars = expr.free_symbols

    if len(free_vars) > 1:
        return analyze_multivariable_convexity(expr_str)
    else:
        return solve_convexity(expr_str)
    
from sympy import sympify, Eq, sin, symbols
from sympy.core.relational import Relational

def is_nonlinear_equation(expr):
    try:
        if isinstance(expr, str):
            expr = sympify(expr)

        if isinstance(expr, Relational):  # Ensure it's an equation
            symbols_in_expr = list(expr.free_symbols)
            lhs = expr.lhs - expr.rhs  # Transform into f(x) = 0 form

            # Check if polynomial in all symbols
            if not lhs.is_polynomial(*symbols_in_expr):
                return True

            # Check if any degree > 1
            for var in symbols_in_expr:
                if lhs.as_poly(var) and lhs.as_poly(var).degree() > 1:
                    return True

            return False  # It's a linear equation
        return True  # Not a recognized equation type
    except Exception:
        return True  # Assume nonlinear if unsure

    
def is_nonlinear_system(equation_strs):
    """
    Checks if the system of equations is nonlinear by identifying:
    - Any variable raised to power > 1
    - Any multiplication of different variables (e.g. x*y)
    """
    try:
        expr_list_str = equation_strs.split(',')
        equations = [parse_expr(eq) for eq in expr_list_str]
        for eq in equations:
            for term in eq.atoms(sp.Mul, sp.Pow):
                if isinstance(term, sp.Pow):
                    base, exp = term.args
                    if exp.is_number and exp > 1:
                        return True
                if isinstance(term, sp.Mul):
                    vars_in_term = [a for a in term.args if a.is_Symbol]
                    if len(vars_in_term) >= 2:
                        return True
        return False
    except Exception as e:
        # If parsing fails, passing to non-linear
        return True


def route_query(query_type, expr_str):
    """
    Routes the symbolic expression to the correct SymPy validator based on query_type.
    """
    if query_type == "convexity":
        return route_problem(expr_str)
    elif query_type == "equation":
        if is_nonlinear_equation(expr_str):
            return solve_nonlinear_equation(expr_str)
        else:
            return solve_equation(expr_str)

        return solve_equation(expr_str)
    elif query_type == 'system':
        if is_nonlinear_system(expr_str):
            return solve_nonlinear_system(expr_str)
        else:
            return solve_system_of_equations(expr_str)
    elif query_type == 'derivative':
        return handle_derivative(expr_str)
    elif query_type == 'integral':
        return handle_integral(expr_str)
    else:
        return {"error": f"Unsupported query type: {query_type}"}
    

