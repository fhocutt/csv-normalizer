import pytest

from normalizer.cli import (pad_zip_code, convert_to_seconds,
                            calculate_total_duration, uppercase_name)


def test_pad_zip_code_5_digits():
    assert pad_zip_code('11111') == '11111'


def test_pad_zip_code_1_digit():
    assert pad_zip_code('1') == '00001'


def test_pad_zip_code_empty_string():
    assert pad_zip_code('') == '00000'


def test_pad_zip_code_int_variable():
    with pytest.raises(AttributeError):
        pad_zip_code(1)


def test_convert_to_seconds():
    assert convert_to_seconds('1:23:32.123') == '5012.123'


def test_convert_to_seconds_zero():
    assert convert_to_seconds('0:00:00.000') == '0.0'


def test_convert_to_seconds_non_numeric_string():
    with pytest.raises(ValueError):
        convert_to_seconds('I am bad data')


def test_calculate_total_duration_both_numerical_strings():
    assert calculate_total_duration('11111.111', '11111.111') == '22222.222'


def test_calculate_total_duration_zero():
    assert calculate_total_duration('0.0', '0.0') == '0.0'


def test_calculate_total_duration_floats():
    assert calculate_total_duration(11111.111, 11111.111) == '22222.222'


def test_calculate_total_duration_alpha_str():
    with pytest.raises(ValueError):
        calculate_total_duration('I am very bad data', 'So am I')


def test_uppercase_name():
    assert uppercase_name('good data') == 'GOOD DATA'


# TODO: add test cases with unicode
# TODO: write unit tests for as much coverage as reasonable
