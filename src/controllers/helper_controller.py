from datetime import datetime


def is_float(s: str) -> bool:
    """
    Method that checks if the input is a float
    Args:
        s (str): The input string

    Returns:
    A boolean that indicates if the input is a float or not
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_date(s: str) -> bool:
    """
    Method to check if the input is a date
    Args:
        s (str): The input string

    Returns:
    A boolean that indicates if the input is a date or not
    """
    try:
        s += ":00"
        datetime.strptime(s, "%d/%m/%y %H:%M:%S")
        return True

    except ValueError:
        return False


def is_bool(s: str) -> bool | None:
    """
    Method to check if the input is a boolean.
    Args:
        s (str): The input string

    Returns:
    A boolean that indicates if the input is a boolean or not, or None otherwise.
    """
    if str(s).lower() in {"true", "false"} or (s.isdigit() and int(s) in {0, 1}):
        return True

    else:
        return False
