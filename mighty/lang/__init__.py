from typing import Union, Iterator
import time
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter


class Engine:
    """Contains all of the relative information to process a script."""

    def __init__(self, code: Union[str, Iterator[str]], interval_ms: int) -> None:
        if isinstance(code, str):
            # If code is a string, split it into lines.
            self.lines: list[str] = code.splitlines()
        else:
            # If code is an iterator, convert it to a list of lines.
            self.lines: list[str] = list(code)

        lexer = Lexer(self.lines)
        parser = Parser(list(lexer.tokenize()))
        self.ast = parser.parse()
        self.interval = interval_ms
        self.interpreter = Interpreter()
        self.iteration = iter(self.ast.statements)

    def run(self) -> None:
        """Processes the entire script."""
        while self.next():
            pass

    def next(self) -> bool:
        """Processes the next frame, pausing for the maximum of 
        the interval time.
        """
        try:
            node = next(self.iteration)
        except StopIteration:
            return False

        start = time.time()

        # Process the next node.
        self.interpreter.interpret(node)

        # Calculate elapsed time and the required sleep time in seconds.
        sleep_time = (self.interval / 1000.0) - (time.time() - start)

        if sleep_time > 0.0:
            time.sleep(sleep_time)

        return True
