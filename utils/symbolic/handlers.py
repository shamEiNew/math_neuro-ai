
"""
Handlers for basic symbolic tasks:
  - handle_derivative(expr_str)
  - handle_integral(expr_str)
  - handle_expression(expr_str)

Each function returns a dict with at least:
  - status: "ok" or "error"
  - result: string (human-friendly result) or None
  - details: optional dict with extra metadata (srepr, latex, free_symbols, method)
  - error: optional error message when status == "error"
"""

from typing import Dict, Any
import sympy as sp
from sympy import Derivative, Integral
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations,
    implicit_multiplication_application, convert_xor
)

_transformations = (standard_transformations +
                    (implicit_multiplication_application, convert_xor))


def _safe_parse(s: str):
    """
    Try multiple parsing strategies and return a SymPy object.
    """
    if not isinstance(s, str):
        raise ValueError("Input must be a string")
    s_strip = s.strip()
    # common local names for parse_expr
    local_dict = {
        "sin": sp.sin, "cos": sp.cos, "exp": sp.exp, "log": sp.log,
        "Derivative": Derivative, "Integral": Integral,
        "diff": sp.diff, "integrate": sp.integrate
    }
    # try parse_expr first (more robust for user strings)
    try:
        obj = parse_expr(s_strip, local_dict=local_dict, transformations=_transformations)
        return obj
    except Exception:
        # fallback to sympify
        try:
            return sp.sympify(s_strip)
        except Exception as e:
            raise ValueError(f"Could not parse expression: {e}") from e


def _to_latex_safe(obj):
    try:
        return sp.latex(obj)
    except Exception:
        try:
            return str(obj)
        except Exception:
            return None


def handle_derivative(expr_str: str) -> Dict[str, Any]:
    """
    Analyze derivative information for an expression.
    Assumes expr_str is already valid SymPy-style (e.g., "diff(x**3, x)" or "x**3").
    Returns a structured dict similar in style to solve_convexity.
    """
    try:
        if not expr_str or not isinstance(expr_str, str):
            return {"status": "error", "error": "Input must be a non-empty SymPy-style string."}

        # Parse expression; prefer parse_expr for structured input
        try:
            expr = parse_expr(expr_str, transformations=_transformations)
        except Exception:
            expr = sp.sympify(expr_str)

        expr_simpl = sp.simplify(expr)
        expr_latex = sp.latex(expr_simpl)
        expr_srepr = sp.srepr(expr_simpl)

        free_syms = sorted(list(expr_simpl.free_symbols), key=lambda s: str(s))
        vars_list = [str(s) for s in free_syms]

        result: Dict[str, Any] = {
            "status": "ok",
            "expression": expr_latex,
            "expression_srepr": expr_srepr,
            "variables": vars_list,
            "verdict": "undetermined",
            "details": {}
        }

        # No variables -> constant
        if len(free_syms) == 0:
            result["verdict"] = "constant_function"
            result["details"]["note"] = "Expression has no free symbols (constant)."
            return result

        # Single-variable analysis
        if len(free_syms) == 1:
            x = free_syms[0]
            try:
                # If user provided an explicit Derivative/Diff, try to get the underlying function
                # but we treat expr_simpl as the function f(x)
                f = expr_simpl
                # If it's a Derivative node (e.g., parse_expr("diff(f(x), x)")), convert to function where possible
                if isinstance(f, sp.Derivative):
                    # derivative object; get the expression by calling .doit()? Keep as provided
                    # treat original as derivative; integrate? but primary goal: compute derivatives of function
                    # We'll convert to the expression inside derivative if possible:
                    try:
                        inner = f.expr
                        f = inner
                    except Exception:
                        # fallback: keep f as-is
                        pass

                # first and second derivatives
                f1 = sp.diff(f, x)
                f2 = sp.diff(f1, x)
                f1_s = sp.simplify(f1)
                f2_s = sp.simplify(f2)

                # Critical points: solve f1 == 0
                critical_points = []
                try:
                    sols = sp.solve(sp.Eq(f1_s, 0), x)
                    # normalize sols to list
                    if isinstance(sols, dict):
                        sols = list(sols.values())
                    unique = []
                    for s in sols:
                        s_simpl = sp.simplify(s)
                        if s_simpl not in unique:
                            unique.append(s_simpl)
                    for s in unique:
                        # classify using second derivative test where possible
                        classification = "inconclusive"
                        try:
                            val = f2_s.subs(x, s)
                            # prefer symbolic flags if available
                            if getattr(val, "is_positive", None) is True or (val.is_real and val > 0):
                                classification = "local_minimum"
                            elif getattr(val, "is_negative", None) is True or (val.is_real and val < 0):
                                classification = "local_maximum"
                            else:
                                classification = "inconclusive"
                        except Exception:
                            classification = "inconclusive"
                        critical_points.append({"point": s, "classification": classification})
                except Exception:
                    critical_points = []

                # Monotonicity: try reduce_inequalities on f1 >= 0 and f1 <= 0
                monotonicity = {"increasing_intervals": None, "decreasing_intervals": None}
                try:
                    inc_cond = sp.Ge(f1_s, 0)
                    dec_cond = sp.Le(f1_s, 0)
                    inc_domain = sp.reduce_inequalities([inc_cond], x)
                    dec_domain = sp.reduce_inequalities([dec_cond], x)
                    monotonicity["increasing_intervals"] = inc_domain
                    monotonicity["decreasing_intervals"] = dec_domain
                except Exception:
                    monotonicity = {"increasing_intervals": None, "decreasing_intervals": None}

                # Inflection points: solve f2 == 0 and attempt sign change test (numerical probe)
                inflection_points = []
                try:
                    inf_sols = sp.solve(sp.Eq(f2_s, 0), x)
                    for ip in inf_sols:
                        try:
                            ip_val = float(sp.N(ip))
                            eps = 1e-3
                            left = float(sp.N(f2_s.subs(x, ip_val - eps)))
                            right = float(sp.N(f2_s.subs(x, ip_val + eps)))
                            if (left < 0 and right > 0) or (left > 0 and right < 0):
                                inflection_points.append(ip)
                            else:
                                # still include symbolically but mark uncertain
                                inflection_points.append(ip)
                        except Exception:
                            inflection_points.append(ip)
                except Exception:
                    inflection_points = []

                # Heuristic verdict
                verdict = "undetermined"
                try:
                    if getattr(f1_s, "is_nonnegative", None) is True:
                        verdict = "nondecreasing"
                    elif getattr(f1_s, "is_nonpositive", None) is True:
                        verdict = "nonincreasing"
                    else:
                        # if reduce_inequalities says it's all reals
                        if monotonicity.get("increasing_intervals") is not None and str(monotonicity["increasing_intervals"]) in ("True", "Interval(-oo, oo)"):
                            verdict = "nondecreasing"
                except Exception:
                    verdict = "undetermined"

                result.update({
                    "first_derivative": sp.latex(f1_s),
                    "second_derivative": sp.latex(f2_s),
                    "critical_points": [
                        {"point_latex": sp.latex(cp["point"]), "classification": cp["classification"]}
                        for cp in critical_points
                    ],
                    "monotonicity": {
                        "increasing_intervals": sp.latex(monotonicity["increasing_intervals"]) if monotonicity["increasing_intervals"] is not None else None,
                        "decreasing_intervals": sp.latex(monotonicity["decreasing_intervals"]) if monotonicity["decreasing_intervals"] is not None else None
                    },
                    "inflection_points": [sp.latex(ip) for ip in inflection_points] if inflection_points else [],
                    "verdict": verdict
                })
                result["details"].update({
                    "first_derivative_srepr": sp.srepr(f1_s),
                    "second_derivative_srepr": sp.srepr(f2_s)
                })
                return result

            except Exception as e:
                return {"status": "error", "error": f"Single-variable derivative error: {e}"}

        # Multi-variable analysis
        try:
            sym_list = free_syms
            grad = [sp.diff(expr_simpl, v) for v in sym_list]
            H = sp.Matrix([[sp.diff(g, v) for v in sym_list] for g in grad])
            H_simpl = sp.simplify(H)

            # attempt to solve gradient == 0
            critical_points_mv = []
            try:
                sol = sp.solve([sp.Eq(g, 0) for g in grad], sym_list, dict=True)
                for s in sol:
                    pt = tuple(s.get(v, None) for v in sym_list)
                    critical_points_mv.append(pt)
            except Exception:
                critical_points_mv = []

            principal_minors = []
            for k in range(1, len(sym_list) + 1):
                M = H_simpl[:k, :k]
                try:
                    detk = sp.simplify(M.det())
                except Exception:
                    detk = None
                principal_minors.append(detk)

            result.update({
                "gradient_latex": [sp.latex(g) for g in grad],
                "hessian_latex": sp.latex(H_simpl),
                "principal_minors_latex": [sp.latex(m) if m is not None else None for m in principal_minors],
                "critical_points": [
                    {"point": [sp.latex(val) for val in pt]} for pt in critical_points_mv
                ],
                "verdict": "multi_var_undetermined_or_candidate"
            })
            result["details"].update({
                "gradient_srepr": [sp.srepr(g) for g in grad],
                "hessian_srepr": sp.srepr(H_simpl),
                "principal_minors_srepr": [sp.srepr(m) if m is not None else None for m in principal_minors]
            })
            return result
        except Exception as e:
            return {"status": "error", "error": f"Multi-variable derivative error: {e}"}

    except Exception as outer_e:
        return {"status": "error", "error": str(outer_e)}


def handle_integral(expr_str: str) -> Dict[str, Any]:
    """
    Compute integral (indefinite or definite if bounds provided).

    Returns similar dict shape as handle_derivative.
    """
    try:
        obj = _safe_parse(expr_str)

        # If it's already an Integral node, evaluate it
        if isinstance(obj, Integral):
            try:
                res = obj.doit()
                method = "Integral.doit"
            except Exception:
                # maybe definite integral not solvable symbolically
                raise
        else:
            # If user used 'integrate(' try parse + sp.integrate
            lowered = expr_str.lower()
            if "integral" in lowered or "integrate(" in lowered:
                # try to detect definite integral by parsing tuples like Integral(f,(x,a,b))
                try:
                    parsed = parse_expr(expr_str, local_dict={"Integral": Integral, "integrate": sp.integrate}, transformations=_transformations)
                    if isinstance(parsed, Integral):
                        res = parsed.doit()
                        method = "parsed_integral"
                    else:
                        # try to call integrate on parsed expression; pick first free symbol
                        syms = list(parsed.free_symbols)
                        if syms:
                            res = sp.integrate(parsed, syms[0])
                            method = f"integrate_wrt_{syms[0]}"
                        else:
                            raise ValueError("No free symbol found to integrate with respect to.")
                except Exception:
                    obj = _safe_parse(expr_str)
                    syms = list(obj.free_symbols)
                    if syms:
                        res = sp.integrate(obj, syms[0])
                        method = f"fallback_integrate_wrt_{syms[0]}"
                    else:
                        raise ValueError("No free symbol found to integrate with respect to.")
            else:
                # plain expression -> indefinite integral w.r.t. first symbol
                syms = list(obj.free_symbols)
                if not syms:
                    raise ValueError("No free symbol found to integrate with respect to.")
                syms_sorted = sorted(syms, key=lambda s: str(s))
                res = sp.integrate(obj, syms_sorted[0])
                method = f"integrate_wrt_{syms_sorted[0]}"

        res_s = str(res)
        details = {
            "srepr": sp.srepr(res),
            "latex": _to_latex_safe(res),
            "method": method
        }
        return {"status": "ok", "result": res_s, "details": details}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def handle_expression(expr_str: str) -> Dict[str, Any]:
    """
    Canonicalize and analyze a generic expression:
      - parse
      - compute simplified form
      - srepr, latex, free symbols, is_polynomial hints

    Returns:
      {'status':'ok', 'result': '<simplified_str>', 'details': {...}}
    """
    try:
        obj = _safe_parse(expr_str)

        simplified = sp.simplify(obj)
        expanded = None
        try:
            expanded = sp.expand(simplified)
        except Exception:
            expanded = None

        details = {
            "srepr": sp.srepr(simplified),
            "latex": _to_latex_safe(simplified),
            "free_symbols": [str(s) for s in sorted(list(simplified.free_symbols), key=lambda x: str(x))],
        }

        # polynomial check and degrees per symbol (if polynomial)
        try:
            syms = list(simplified.free_symbols)
            if syms and simplified.is_polynomial(*syms):
                degs = {}
                for s in syms:
                    poly = simplified.as_poly(s)
                    if poly is not None:
                        degs[str(s)] = int(poly.degree())
                details["is_polynomial"] = True
                details["poly_degrees"] = degs
            else:
                details["is_polynomial"] = False
        except Exception:
            details["is_polynomial"] = False

        # include expanded if different
        if expanded is not None and str(expanded) != str(simplified):
            details["expanded"] = str(expanded)

        return {"status": "ok", "result": str(simplified), "details": details}
    except Exception as e:
        return {"status": "error", "error": str(e)}
