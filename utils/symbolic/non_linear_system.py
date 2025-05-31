import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

def solve_nonlinear_system(equation_strs):
    try:
        # Parse each equation string into a SymPy expression
        expr_list_str = equation_strs.split(',')
        equations = [parse_expr(eq) for eq in expr_list_str]

        # Automatically detect all symbols from all equations
        symbols = sorted({sym for eq in equations for sym in eq.free_symbols}, key=lambda s: s.name)

        # Solve the system
        solutions = sp.nonlinsolve(equations, symbols)

        return {
            "equations": [sp.latex(eq) for eq in equations],
            "variables": [sp.latex(s) for s in symbols],
            "solution": [sp.latex(sol) for sol in solutions]
        }
    except Exception as e:
        return {"error": str(e)}
