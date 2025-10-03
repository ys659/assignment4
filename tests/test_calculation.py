# tests/test_calculations.py

"""
Unit tests for the calculator_calculations module using pytest.

This test suite covers both positive and negative scenarios for the Calculation
classes and the CalculationFactory. It ensures that calculations execute correctly,
the factory creates appropriate instances, and error handling behaves as expected.

Tests are organized following the AAA (Arrange, Act, Assert) pattern and adhere
to PEP8 standards for code style and formatting.
"""

import pytest
from unittest.mock import patch
from app.operation import Operation
from app.calculation import (
    CalculationFactory,
    AddCalculation,
    SubtractCalculation,
    MultiplyCalculation,
    DivideCalculation,
    PowerCalculation,
    Calculation
)


# -----------------------------------------------------------------------------------
# Test Concrete Calculation Classes
# -----------------------------------------------------------------------------------

@patch.object(Operation, 'addition')
def test_add_calculation_execute_positive(mock_addition):
    a, b = 10.0, 5.0
    expected_result = 15.0
    mock_addition.return_value = expected_result
    add_calc = AddCalculation(a, b)
    result = add_calc.execute()
    mock_addition.assert_called_once_with(a, b)
    assert result == expected_result


@patch.object(Operation, 'addition')
def test_add_calculation_execute_negative(mock_addition):
    a, b = 10.0, 5.0
    mock_addition.side_effect = Exception("Addition error")
    add_calc = AddCalculation(a, b)
    with pytest.raises(Exception) as exc_info:
        add_calc.execute()
    assert str(exc_info.value) == "Addition error"


@patch.object(Operation, 'subtraction')
def test_subtract_calculation_execute_positive(mock_subtraction):
    a, b = 10.0, 5.0
    expected_result = 5.0
    mock_subtraction.return_value = expected_result
    subtract_calc = SubtractCalculation(a, b)
    result = subtract_calc.execute()
    mock_subtraction.assert_called_once_with(a, b)
    assert result == expected_result


@patch.object(Operation, 'subtraction')
def test_subtract_calculation_execute_negative(mock_subtraction):
    a, b = 10.0, 5.0
    mock_subtraction.side_effect = Exception("Subtraction error")
    subtract_calc = SubtractCalculation(a, b)
    with pytest.raises(Exception) as exc_info:
        subtract_calc.execute()
    assert str(exc_info.value) == "Subtraction error"


@patch.object(Operation, 'multiplication')
def test_multiply_calculation_execute_positive(mock_multiplication):
    a, b = 10.0, 5.0
    expected_result = 50.0
    mock_multiplication.return_value = expected_result
    multiply_calc = MultiplyCalculation(a, b)
    result = multiply_calc.execute()
    mock_multiplication.assert_called_once_with(a, b)
    assert result == expected_result


@patch.object(Operation, 'multiplication')
def test_multiply_calculation_execute_negative(mock_multiplication):
    a, b = 10.0, 5.0
    mock_multiplication.side_effect = Exception("Multiplication error")
    multiply_calc = MultiplyCalculation(a, b)
    with pytest.raises(Exception) as exc_info:
        multiply_calc.execute()
    assert str(exc_info.value) == "Multiplication error"


@patch.object(Operation, 'division')
def test_divide_calculation_execute_positive(mock_division):
    a, b = 10.0, 5.0
    expected_result = 2.0
    mock_division.return_value = expected_result
    divide_calc = DivideCalculation(a, b)
    result = divide_calc.execute()
    mock_division.assert_called_once_with(a, b)
    assert result == expected_result


@patch.object(Operation, 'division')
def test_divide_calculation_execute_negative(mock_division):
    a, b = 10.0, 5.0
    mock_division.side_effect = Exception("Division error")
    divide_calc = DivideCalculation(a, b)
    with pytest.raises(Exception) as exc_info:
        divide_calc.execute()
    assert str(exc_info.value) == "Division error"


def test_divide_calculation_execute_division_by_zero():
    a, b = 10.0, 0.0
    divide_calc = DivideCalculation(a, b)
    with pytest.raises(ZeroDivisionError) as exc_info:
        divide_calc.execute()
    assert str(exc_info.value) == "Cannot divide by zero."


@patch.object(Operation, 'power')
def test_power_calculation_execute_positive(mock_power):
    a, b = 2.0, 3.0
    expected = 8.0
    mock_power.return_value = expected
    calc = PowerCalculation(a, b)
    result = calc.execute()
    mock_power.assert_called_once_with(a, b)
    assert result == expected


def test_factory_creates_power_calculation():
    a, b = 2.0, 3.0
    calc = CalculationFactory.create_calculation('power', a, b)
    assert isinstance(calc, PowerCalculation)
    assert calc.a == a
    assert calc.b == b


# -----------------------------------------------------------------------------------
# Test CalculationFactory
# -----------------------------------------------------------------------------------

def test_factory_creates_add_calculation():
    calc = CalculationFactory.create_calculation('add', 10.0, 5.0)
    assert isinstance(calc, AddCalculation)


def test_factory_creates_subtract_calculation():
    calc = CalculationFactory.create_calculation('subtract', 10.0, 5.0)
    assert isinstance(calc, SubtractCalculation)


def test_factory_creates_multiply_calculation():
    calc = CalculationFactory.create_calculation('multiply', 10.0, 5.0)
    assert isinstance(calc, MultiplyCalculation)


def test_factory_creates_divide_calculation():
    calc = CalculationFactory.create_calculation('divide', 10.0, 5.0)
    assert isinstance(calc, DivideCalculation)


def test_factory_create_unsupported_calculation():
    with pytest.raises(ValueError) as exc_info:
        CalculationFactory.create_calculation('modulus', 10.0, 5.0)
    assert "Unsupported calculation type" in str(exc_info.value)


def test_factory_register_calculation_duplicate():
    with pytest.raises(ValueError) as exc_info:
        @CalculationFactory.register_calculation('add')
        class AnotherAddCalculation(Calculation):
            def execute(self) -> float:
                return Operation.addition(self.a, self.b)
    assert "already registered" in str(exc_info.value)


# -----------------------------------------------------------------------------------
# Test String Representations
# -----------------------------------------------------------------------------------

@patch.object(Operation, 'addition', return_value=15.0)
def test_calculation_str_representation_addition(mock_addition):
    add_calc = AddCalculation(10.0, 5.0)
    assert str(add_calc) == "AddCalculation: 10.0 Add 5.0 = 15.0"


@patch.object(Operation, 'subtraction', return_value=5.0)
def test_calculation_str_representation_subtraction(mock_subtraction):
    subtract_calc = SubtractCalculation(10.0, 5.0)
    assert str(subtract_calc) == "SubtractCalculation: 10.0 Subtract 5.0 = 5.0"


@patch.object(Operation, 'multiplication', return_value=50.0)
def test_calculation_str_representation_multiplication(mock_multiplication):
    multiply_calc = MultiplyCalculation(10.0, 5.0)
    assert str(multiply_calc) == "MultiplyCalculation: 10.0 Multiply 5.0 = 50.0"


@patch.object(Operation, 'division', return_value=2.0)
def test_calculation_str_representation_division(mock_division):
    divide_calc = DivideCalculation(10.0, 5.0)
    assert str(divide_calc) == "DivideCalculation: 10.0 Divide 5.0 = 2.0"


@patch.object(Operation, 'power', return_value=8.0)
def test_calculation_str_representation_power(mock_power):
    power_calc = PowerCalculation(2.0, 3.0)
    assert str(power_calc) == "PowerCalculation: 2.0 Power 3.0 = 8.0"


def test_calculation_repr_representation_subtraction():
    subtract_calc = SubtractCalculation(10.0, 5.0)
    assert repr(subtract_calc) == "SubtractCalculation(a=10.0, b=5.0)"


def test_calculation_repr_representation_division():
    divide_calc = DivideCalculation(10.0, 5.0)
    assert repr(divide_calc) == "DivideCalculation(a=10.0, b=5.0)"


# -----------------------------------------------------------------------------------
# Parameterized Tests for Execute Method
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize("calc_type, a, b, expected_result", [
    ('add', 10.0, 5.0, 15.0),
    ('subtract', 10.0, 5.0, 5.0),
    ('multiply', 10.0, 5.0, 50.0),
    ('divide', 10.0, 5.0, 2.0),
    ('power', 2.0, 3.0, 8.0),
])
@patch.object(Operation, 'addition')
@patch.object(Operation, 'subtraction')
@patch.object(Operation, 'multiplication')
@patch.object(Operation, 'division')
@patch.object(Operation, 'power')
def test_calculation_execute_parameterized(
    mock_power, mock_division, mock_multiplication, mock_subtraction, mock_addition,
    calc_type, a, b, expected_result
):
    if calc_type == 'add':
        mock_addition.return_value = expected_result
    elif calc_type == 'subtract':
        mock_subtraction.return_value = expected_result
    elif calc_type == 'multiply':
        mock_multiplication.return_value = expected_result
    elif calc_type == 'divide':
        mock_division.return_value = expected_result
    elif calc_type == 'power':
        mock_power.return_value = expected_result

    calc = CalculationFactory.create_calculation(calc_type, a, b)
    result = calc.execute()

    if calc_type == 'add':
        mock_addition.assert_called_once_with(a, b)
    elif calc_type == 'subtract':
        mock_subtraction.assert_called_once_with(a, b)
    elif calc_type == 'multiply':
        mock_multiplication.assert_called_once_with(a, b)
    elif calc_type == 'divide':
        mock_division.assert_called_once_with(a, b)
    elif calc_type == 'power':
        mock_power.assert_called_once_with(a, b)

    assert result == expected_result


# -----------------------------------------------------------------------------------
# Parameterized Tests for String Representation
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize("calc_type, a, b, expected_str", [
    ('add', 10.0, 5.0, "AddCalculation: 10.0 Add 5.0 = 15.0"),
    ('subtract', 10.0, 5.0, "SubtractCalculation: 10.0 Subtract 5.0 = 5.0"),
    ('multiply', 10.0, 5.0, "MultiplyCalculation: 10.0 Multiply 5.0 = 50.0"),
    ('divide', 10.0, 5.0, "DivideCalculation: 10.0 Divide 5.0 = 2.0"),
    ('power', 2.0, 3.0, "PowerCalculation: 2.0 Power 3.0 = 8.0"),
])
@patch.object(Operation, 'addition', return_value=15.0)
@patch.object(Operation, 'subtraction', return_value=5.0)
@patch.object(Operation, 'multiplication', return_value=50.0)
@patch.object(Operation, 'division', return_value=2.0)
@patch.object(Operation, 'power', return_value=8.0)
def test_calculation_str_parameterized(
    mock_power, mock_division, mock_multiplication, mock_subtraction, mock_addition,
    calc_type, a, b, expected_str
):
    calc = CalculationFactory.create_calculation(calc_type, a, b)
    calc_str = str(calc)
    assert calc_str == expected_str
