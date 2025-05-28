from sympy import Eq, solve
from sympy.parsing.sympy_parser import parse_expr

def solve_equation(expr_str):
    try:
        print(expr_str)
        # Split at '=', assume a basic equation format
        if '=' not in expr_str:
            return {"error": "Not an equation"}
        lhs_str, rhs_str = expr_str.split('=')
        lhs = parse_expr(lhs_str.strip())
        rhs = parse_expr(rhs_str.strip())
        equation = Eq(lhs, rhs)

        solution = solve(equation)
        return {
            "equation": equation.latex(),
            "solution": [sol.latex() for sol in solution]
        }
    except Exception as e:
        return {"error": str(e)}
