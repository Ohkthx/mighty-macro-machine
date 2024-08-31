from typing import Union, Iterator
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter


class Engine:
    """Contains all of the relative information to process a script."""

    def __init__(self, code: Union[str, Iterator[str]]) -> None:
        if isinstance(code, str):
            # If code is a string, split it into lines.
            self.lines: list[str] = code.splitlines()
        else:
            # If code is an iterator, convert it to a list of lines.
            self.lines: list[str] = list(code)

        lexer = Lexer(self.lines)
        parser = Parser(list(lexer.tokenize()))
        self.ast = parser.parse()

        self.interpreter = Interpreter()

    def run(self):
        """Processes the entire script."""
        self.interpreter.interpret(self.ast)
