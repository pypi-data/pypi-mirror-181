from typing import Any, Optional

def convert_to_float(value: str) -> float | Any:
    """Attempts to convert a string, number, or boolean < value > in the < try > block to a float.
    Can also convert numbers masquerading as strings that include one or more thousand separator
    commas (e.g., "5,000,000").

    If a runtime exception is encountered the < value > is returned unchanged in the except block.

    Parameters:
        value (obj): string or number to be converted

    Returns:
        float|any: float if value successfully converted; otherwise returns value unchanged
    """

    try:
        return float(value.replace(',', ''))
    except (AttributeError, TypeError, ValueError):
        return value


def convert_to_int(value: str) -> int | Any:
    """Attempts to convert a string, number boolean < value > in the < try > block to an integer.
    Can also convert numbers masquerading as strings that include one or more thousand separator
    commas (e.g., "5,000,000") or a period that designates a fractional component
    (e.g., "5,000,000.9999").

    If a runtime exception is encountered the < value > is returned unchanged in the except block.

    Parameters:
        value (str|int): string or number to be converted

    Returns:
        int|any: integer if value successfully converted else returns value unchanged
    """

    try:
        return int(float(value.replace(',', '')))
    except (AttributeError, TypeError, ValueError):
        return value


def convert_to_list(value: str, delimiter: Optional[str] = None)  -> list | Any:
    """Attempts to convert a string < value > to a list in the < try > block using the provided
    < delimiter >. Removes leading/trailing spaces before converting < value > to a list.

    If a runtime exception is encountered the < value > is returned unchanged in the except block.

    Parameters:
        value (str): string to be split.
        delimiter (str): optional delimiter provided for splitting the string

    Returns:
         list|any: list if value successfully converted else returns value unchanged
    """

    try:
        if delimiter:
            return value.strip().split(delimiter)
        else:
            return value.strip().split()
    except (AttributeError, TypeError, ValueError):
        return value
