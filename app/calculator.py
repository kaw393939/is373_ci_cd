"""Pure arithmetic: no HTTP or runtime configuration dependencies."""

import math
from typing import Literal

Operation = Literal["add", "subtract", "multiply", "divide"]
LIMIT = 1_000_000


class CalculationError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def calculate(a: float, b: float, operation: Operation) -> float:
    for number in (a, b):
        if isinstance(number, bool) or not isinstance(number, (int, float)):
            raise CalculationError("invalid_operand", "Enter numbers only.")
        if abs(number) > LIMIT or not math.isfinite(number):
            raise CalculationError("invalid_operand", "Numbers must be finite and within ±1,000,000.")

    match operation:
        case "add":
            result = a + b
        case "subtract":
            result = a - b
        case "multiply":
            result = a * b
        case "divide":
            if b == 0:
                raise CalculationError("division_by_zero", "Cannot divide by zero.")
            result = a / b
        case _:
            raise CalculationError("invalid_operation", "Choose a supported operation.")

    if not math.isfinite(result):
        raise CalculationError("non_finite_result", "The result is too large to represent.")
    return float(result)
