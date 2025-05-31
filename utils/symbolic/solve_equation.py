from sympy import Eq, solve, sympify, latex
from sympy.parsing.sympy_parser import parse_expr
from sympy.core.numbers import I

def solve_equation(expr_str):
    
    try:

        # Split at '=', assume a basic equation format
        if '=' not in expr_str:
            return {"error": "Not an equation"}
        
        lhs_str, rhs_str = expr_str.split('=')
        lhs = parse_expr(lhs_str.strip())
        rhs = parse_expr(rhs_str.strip())
        equation = Eq(lhs, rhs)

        solution = solve(equation)

        all_real = all(not sol.has(I) for sol in solution)
        all_complex = all(sol.has(I) for sol in solution)
        return {
            "number_of_solution": len(solution),
            "equation": latex(equation),
            "solution": [latex(sol) for sol in solution],
            "all_roots_real": all_real,
            "all_roots_complex": all_complex,
        }
    except Exception as e:
        return {"error": str(e)}
    
def solve_nonlinear_equation(expr_str):
    
    try:

        # Split at '=', assume a basic equation format
        if '=' not in expr_str:
            return {"error": "Not an equation"}
        
        lhs_str, rhs_str = expr_str.split('=')
        lhs = parse_expr(lhs_str.strip())
        rhs = parse_expr(rhs_str.strip())
        equation = Eq(lhs, rhs)

        solution = solve(equation)

        all_real = all(not sol.has(I) for sol in solution)
        all_complex = all(sol.has(I) for sol in solution)
        return {
            "number_of_solution": len(solution),
            "equation": latex(equation),
            "solution": [latex(sol) for sol in solution]
        }
    except Exception as e:
        return {"error": str(e)}
