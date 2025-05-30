from sympy import symbols, Eq, solve, latex
from sympy.parsing.sympy_parser import parse_expr

def solve_system_of_equations(equation_strs):
    try:
        equation_strs = equation_strs.split(',')
        eqs = [parse_expr(eq_str) for eq_str in equation_strs]
        
        # Extract all variables from all expressions
        all_symbols = set()
        for expr in eqs:
            all_symbols.update(expr.free_symbols)
        all_symbols = sorted(all_symbols, key=lambda s: s.name)

        # Convert each expression to an equality (assume == 0)
        equations = [Eq(expr, 0) for expr in eqs]
        
        solution = solve(equations, *all_symbols, dict=True)

        return {
            "equations": [latex(eq) for eq in equations],
            "solution": [ {str(k): v for k, v in sol.items()} for sol in solution]
        }
    except Exception as e:
        return {"error": str(e)}
