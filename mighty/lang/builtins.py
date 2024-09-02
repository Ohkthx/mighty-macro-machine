from typing import Any, Callable
import pyautogui
from .environment import Environment, BuiltinFunction


def builtin_mouse_position(x: int, y: int) -> None:
    """Moves the mouse to a specific position."""
    pyautogui.moveTo(x, y, _pause=False)


def builtin_print(*args: Any) -> None:
    """Prints to the console."""
    print(*args)


def builtin_len(arg: Any) -> int:
    """Return the length of the given string."""
    if isinstance(arg, str):
        return len(arg)
    else:
        raise TypeError(f"len() argument must be a string, not '{type(arg).__name__}'")


def builtin_type(arg: Any) -> str:
    """Return the type of the given value."""
    return type(arg).__name__


def builtin_int(arg: Any) -> int:
    """Convert the given value to an integer."""
    try:
        return int(arg)
    except ValueError:
        raise ValueError(f"Cannot convert '{arg}' to int")


def builtin_float(arg: Any) -> float:
    """Convert the given value to a float."""
    try:
        return float(arg)
    except ValueError:
        raise ValueError(f"Cannot convert '{arg}' to float")


def builtin_str(arg: Any) -> str:
    """Convert the given value to a string."""
    return str(arg)


# Maps the built-in functions to the callable names.
BUILTINS: dict[str, Callable[..., Any]] = {
    "mpos": builtin_mouse_position,
    "print": builtin_print,
    "len": builtin_len,
    "type": builtin_type,
    "int": builtin_int,
    "float": builtin_float,
    "str": builtin_str,
}


def add_builtins(environment: Environment) -> None:
    """Add built-in functions to the functions environment."""
    for name, func in BUILTINS.items():
        environment.functions[name] = BuiltinFunction(func)
