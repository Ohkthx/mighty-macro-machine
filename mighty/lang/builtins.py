import time
from typing import Any, Callable
import pyautogui
from .environment import Environment, BuiltinFunction
from .randomness import Mouse


def builtin_wait(env: Environment, interval: int) -> None:
    """Waits for a specified amount of frames."""
    if env.wait > 0:
        return
    env.wait = interval


def builtin_mouse_position(env: Environment, x: int, y: int) -> None:
    """Moves the mouse to a specific position."""
    if env.has_moved(x, y):
        env.set_position(x, y)
        pyautogui.moveTo(x, y, _pause=False)


def builtin_mouse_click(env: Environment, button_id: str, randomize: bool = False) -> None:
    """Presses a mouse button to simulate a click."""
    pyautogui.mouseDown(button=button_id, _pause=False)
    if randomize:
        time.sleep(Mouse.click_time())
    pyautogui.mouseUp(button=button_id, _pause=False)


def builtin_print(_: Environment, *args: Any) -> None:
    """Prints to the console."""
    print(*args)


def builtin_len(_: Environment, arg: Any) -> int:
    """Return the length of the given string."""
    if isinstance(arg, str):
        return len(arg)
    else:
        raise TypeError(f"len() argument must be a string, not '{type(arg).__name__}'")


def builtin_type(_: Environment, arg: Any) -> str:
    """Return the type of the given value."""
    return type(arg).__name__


def builtin_int(_: Environment, arg: Any) -> int:
    """Convert the given value to an integer."""
    try:
        return int(arg)
    except ValueError:
        raise ValueError(f"Cannot convert '{arg}' to int")


def builtin_float(_: Environment, arg: Any) -> float:
    """Convert the given value to a float."""
    try:
        return float(arg)
    except ValueError:
        raise ValueError(f"Cannot convert '{arg}' to float")


def builtin_str(_: Environment, arg: Any) -> str:
    """Convert the given value to a string."""
    return str(arg)


# Maps the built-in functions to the callable names.
BUILTINS: dict[str, Callable[..., Any]] = {
    "wait": builtin_wait,
    "mpos": builtin_mouse_position,
    "mclick": builtin_mouse_click,
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
