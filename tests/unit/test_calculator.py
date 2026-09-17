import pytest

from app.calculator import CalculationError, calculate


@pytest.mark.parametrize("a,b,operation,result", [
    (2, 3, "add", 5), (-4, 2, "subtract", -6),
    (6, 7, "multiply", 42), (9, 2, "divide", 4.5),
    (0.1, 0.2, "add", 0.3), (1_000_000, 1_000_000, "multiply", 1e12),
])
def test_calculation(a, b, operation, result):
    assert calculate(a, b, operation) == pytest.approx(result)


@pytest.mark.parametrize("a,b,operation,code", [
    (1, 0, "divide", "division_by_zero"),
    (1, -0.0, "divide", "division_by_zero"),
    (1, 5e-324, "divide", "non_finite_result"),
    (float("inf"), 1, "add", "invalid_operand"),
    (1, float("nan"), "add", "invalid_operand"),
    (1_000_001, 1, "add", "invalid_operand"),
    (True, 1, "add", "invalid_operand"),
    ("1", 1, "add", "invalid_operand"),
    (1, 2, "power", "invalid_operation"),
])
def test_rejects_invalid_arithmetic(a, b, operation, code):
    with pytest.raises(CalculationError) as error:
        calculate(a, b, operation)
    assert error.value.code == code
