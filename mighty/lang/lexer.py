from typing import Iterator
from .token import Tokens, Token, get_token


class Lexer:
    """Converts source code into tokens for the parser."""

    def __init__(self, code: str):
        self.code = code
        self.position = 0
        self.line = 1
        self.indent_level = 0

    def tokenize(self) -> Iterator[Token]:
        """Starts the tokenizing process."""
        match = get_token(self.code)

        # Process matches until there are not anymore expected tokens.
        while match is not None:
            kind = match.lastgroup
            value = match.group(kind)

            if kind == 'NEWLINE':
                # Update the indent level.
                self.line += 1
                self.indent_level = 0
            elif kind == 'INDENT':
                # General indentation handling, not just with '->'.
                self.indent_level += 1
                pass
            elif kind == 'NEXT':
                # Handle inline -> to continue actions on the same frame.
                yield (Tokens.NEXT, '->')
            elif kind == 'SKIP':
                pass
            elif kind == 'MISMATCH':
                raise RuntimeError(f'Unexpected character: {value} on line {self.line}')
            else:
                token_type = Tokens[kind]
                yield (token_type, value)

            self.position = match.end()
            match = get_token(self.code, self.position)

        # Ensure to mark the end of file.
        yield (Tokens.EOL, '\\n')
