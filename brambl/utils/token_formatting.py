import decimal
from typing import Union

from brambl.utils.types import is_integer, is_string
from brambl.utils.units import units


class denoms:
    nanopoly = int(units["nanopoly"])
    poly = int(units["poly"])
    nanoarbit = int(units['nanoarbit'])
    arbit = int(units['arbit'])


MIN_TOKEN_VALUE = 0
MAX_TOKEN_VALUE = 2 ** 127 - 1


def from_nanotoken(number: int, unit: str) -> Union[int, decimal.Decimal]:
    """
    Takes a number of nanotoken and converts it to any other token unit (polys and arbits currently supported)
    """
    if unit.lower() not in units:
        raise ValueError(
            "Unknown unit.  Must be one of {0}".format("/".join(units.keys()))
        )

    if number == 0:
        return 0

    if number < MIN_TOKEN_VALUE or number > MAX_TOKEN_VALUE:
        raise ValueError("value must be between 1 and 2**128 - 1")

    unit_value = units[unit.lower()]

    with decimal.localcontext() as ctx:
        ctx.prec = 999
        d_number = decimal.Decimal(value=number, context=ctx)
        result_value = d_number / unit_value

    return result_value


def to_nanotoken(number: Union[int, float, str, decimal.Decimal], unit: str) -> int:
    """
    Takes a number of a unit and returns the number of that unit in nanotokens (supports arbits and polys).
    """
    if unit.lower() not in units:
        raise ValueError(
            "Unknown unit.  Must be one of {0}".format("/".join(units.keys()))
        )

    if is_integer(number) or is_string(number):
        d_number = decimal.Decimal(value=number)
    elif isinstance(number, float):
        d_number = decimal.Decimal(value=str(number))
    elif isinstance(number, decimal.Decimal):
        d_number = number
    else:
        raise TypeError("Unsupported type.  Must be one of integer, float, or string")

    s_number = str(number)
    unit_value = units[unit.lower()]

    if d_number == decimal.Decimal(0):
        return 0

    if d_number < 1 and "." in s_number:
        with decimal.localcontext() as ctx:
            multiplier = len(s_number) - s_number.index(".") - 1
            ctx.prec = multiplier
            d_number = decimal.Decimal(value=number, context=ctx) * 10 ** multiplier
        unit_value /= 10 ** multiplier

    with decimal.localcontext() as ctx:
        ctx.prec = 999
        result_value = decimal.Decimal(value=d_number, context=ctx) * unit_value

    if result_value < MIN_TOKEN_VALUE or result_value > MAX_TOKEN_VALUE:
        raise ValueError("Resulting wei value must be between 1 and 2**256 - 1")

    return int(result_value)
