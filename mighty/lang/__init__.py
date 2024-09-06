from typing import Union, Iterator, Optional
import time
from .node import ASTNode
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter


class Engine:
    """Contains all of the relative information to process a script."""

    def __init__(self, code: Union[str, Iterator[str]], interval_ms: int, old_interval: Optional[int] = None) -> None:
        if isinstance(code, str):
            # If code is a string, split it into lines.
            self.lines: list[str] = code.splitlines()
        else:
            # If code is an iterator, convert it to a list of lines.
            self.lines: list[str] = list(code)

        lexer = Lexer(self.lines)
        tokens = list(lexer.tokenize())
        if old_interval and old_interval != interval_ms:
            # Scale the movement to a different interval.
            tokens = Lexer.scale(tokens, old_interval, interval_ms)

        parser = Parser(tokens)
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
        node: Optional[ASTNode] = None
        if self.interpreter.environment.wait == 0:
            try:
                node = next(self.iteration)
            except StopIteration:
                return False

        start = time.time()

        # Process the next node or continue to pause.
        if self.interpreter.environment.wait > 0:
            self.interpreter.environment.wait -= 1
        elif node:
            self.interpreter.interpret(node)

        # Calculate elapsed time and the required sleep time in seconds.
        sleep_time = (1.0 / self.interval) - (time.time() - start)

        if sleep_time > 0.0:
            time.sleep(sleep_time)

        return True
