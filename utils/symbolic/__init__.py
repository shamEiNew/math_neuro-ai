# utils/symbolic/__init__.py

from .solve_convexity import solve_convexity, analyze_multivariable_convexity
from .solve_equation import solve_equation, solve_nonlinear_equation
from .solve_linear_system import solve_system_of_equations
from .non_linear_system import solve_nonlinear_system
from . import *
from .handlers import handle_derivative, handle_integral, handle_expression
from .ml_classifier import classify