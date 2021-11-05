import decimal

import pytest
from hypothesis import (
    given,
    strategies as st
)

from brambl.utils.token_formatting import MIN_TOKEN_VALUE, MAX_TOKEN_VALUE, from_nanotoken, to_nanotoken
from brambl.utils.units import units


@given(
    amount_in_token=st.integers(min_value=MIN_TOKEN_VALUE, max_value=MAX_TOKEN_VALUE),
    intermediate_unit=st.sampled_from(tuple(units.keys())),
)
def test_conversion_round_trip(amount_in_token, intermediate_unit):
    intermediate_amount = from_nanotoken(amount_in_token, intermediate_unit)
    result_amount = to_nanotoken(intermediate_amount, intermediate_unit)
    assert result_amount == amount_in_token


MAX_TOPL_WHOLE = 115792089237316195423570985008687907853269984665640564039457
MAX_TOPL_DECIMAL_MAX = 584007913129639935
MAX_TOPL_DECIMAL = 999999999999999999


def make_token_string_value(amount_in_token):
    s_amount_in_token = str(amount_in_token)
    whole_part = s_amount_in_token[:-9] or "0"
    decimal_part = s_amount_in_token[-9:]

    s_amount_in_token = "{0}.{1}".format(
        whole_part, decimal_part.zfill(9).rstrip("0")
    ).rstrip(".")
    return s_amount_in_token


@given(st.integers(min_value=0, max_value=MAX_TOKEN_VALUE).map(make_token_string_value))
def test_conversion_revers_round_trip_trip(amount_in_token):
    intermediate_amount = to_nanotoken(amount_in_token, "poly")
    result_amount = from_nanotoken(intermediate_amount, "poly")
    assert decimal.Decimal(result_amount) == decimal.Decimal(str(amount_in_token))


@pytest.mark.parametrize(
    "value,expected",
    [
        ([1000000000, "nanopoly"], "1000000000"),
        ([1000000000, "poly"], "1"),
        ([1000000000, "nanoarbit"], "1000000000"),
        ([1000000000, "arbit"], "1"),
    ],
)
def test_from_nanotoken(value, expected):
    assert from_nanotoken(*value) == decimal.Decimal(expected)


@pytest.mark.parametrize(
    "value,expected",
    [
        ([1, "nanopoly"], "1"),
        ([1, "poly"], "1000000000"),
        ([1, "nanoarbit"], "1"),
        ([1, "arbit"], "1000000000"),
        ([0.05, "poly"], "50000000"),
        ([1.2, "arbit"], "1200000000"),
    ],
)
def test_to_nanotoken(value, expected):
    assert to_nanotoken(*value) == decimal.Decimal(expected)


@pytest.mark.parametrize("value,unit", ((1, "wei"), (1, "not-a-unit"), (-1, "token")))
def test_invalid_to_nanotoken_values(value, unit):
    with pytest.raises(ValueError):
        to_nanotoken(value, unit)

    with pytest.raises(ValueError):
        from_nanotoken(value, unit)
