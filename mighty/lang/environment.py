from typing import Any, Callable, Union
from .node import Param, ASTNode


class BuiltinFunction:
    """Used to define and filter for functions that are considered built-in."""

    def __init__(self, func: Callable[..., Any]) -> None:
        self.func = func

    def __call__(self, *args: Any) -> Any:
        return self.func(*args)


class Environment:
    """Holds the built-in and delcared variables and functions for an instance."""

    def __init__(self) -> None:
        self.variables: dict[str, Any] = {}
        self.functions: dict[str, Any] = {}
        self.wait: int = 0

    def get(self, name: str) -> Any:
        """Obtains a variables then function value if it exists."""
        if name in self.variables:
            return self.variables[name]
        elif name in self.functions:
            return self.functions[name]
        else:
            raise NameError(f"Variable or function '{name}' not defined.")

    def set(self, name: str, value: Any) -> None:
        """Sets the value of a variable."""
        self.variables[name] = value

    def set_function(self, name: str, params: list[Param], body: list[ASTNode]) -> None:
        """Sets a new function into the environment. Usually this is user defined."""
        self.functions[name] = (params, body)

    def get_function(self, name: str) -> Union[BuiltinFunction, tuple[list[Param], list[ASTNode]]]:
        """Obtains a declared function, first checking built-in functions and returns the callable object."""
        if name in self.functions:
            return self.functions[name]
        else:
            raise TypeError(f"Function '{name}' is not a built-in function.")
