from enum import Enum, auto
import re

# Token definitions, used to store captured token information.
TokenType = str
Token = tuple[TokenType, str]


class Tokens(Enum):
    # Identifiers
    IDENTIFIER = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    POWER = auto()
    MODULUS = auto()

    PLUS_ASSIGN = auto()
    MINUS_ASSIGN = auto()
    MULTIPLY_ASSIGN = auto()
    DIVIDE_ASSIGN = auto()

    NEXT = auto()  # Represents '->'
    ASSIGN = auto()  # Represents '='

    EQUAL = auto()
    NOT_EQUAL = auto()
    GREATER_THAN = auto()
    LESS_THAN = auto()
    GREATER_EQUAL = auto()
    LESS_EQUAL = auto()

    # Literals
    NUMBER = auto()  # Numeric literals
    STRING = auto()  # String literals

    # Keywords
    IF = auto()
    ELSE = auto()
    FOR = auto()
    WHILE = auto()
    FUNC = auto()

    # Indentation
    INDENT = auto()
    DEDENT = auto()

    # End of Line
    EOL = auto()

    # Comments
    COMMENT = auto()

    # Delimiters
    COLON = auto()  # Represents ':'
    COMMA = auto()  # Represents ','
    LPAREN = auto()  # Represents '('
    RPAREN = auto()  # Represents ')'
    LBRACKET = auto()  # Represents '['
    RBRACKET = auto()  # Represents ']'
    LBRACE = auto()  # Represents '{'
    RBRACE = auto()  # Represents '}'

    # Miscellaneous
    DELIMITER = auto()


_TOKEN_SPECS = [
    ('COMMENT', r'//.*'),                         # Comments
    ('FUNC', r'func'),                            # Function defintions.
    ('IDENTIFIER', r'[A-Za-z_][A-Za-z0-9_]*'),    # Identifiers
    ('NEXT', r'->'),                              # -> operator
    ('NUMBER', r'\d+(\.\d*)?'),                   # Number literals
    ('STRING', r'"[^"]*"'),                       # String literals (quoted)
    ('ASSIGN', r'='),                             # Assignment operator
    ('PLUS_ASSIGN', r'\+='),                      # += operator
    ('MINUS_ASSIGN', r'-='),                      # -= operator
    ('MULTIPLY_ASSIGN', r'\*='),                  # *= operator
    ('DIVIDE_ASSIGN', r'/='),                     # /= operator
    ('PLUS', r'\+'),                              # + operator
    ('MINUS', r'-'),                              # - operator
    ('MULTIPLY', r'\*'),                          # * operator
    ('DIVIDE', r'/'),                             # / operator
    ('POWER', r'\*\*'),                           # ** operator
    ('MODULUS', r'%'),                            # % operator
    ('EQUAL', r'=='),                             # == comparison
    ('NOT_EQUAL', r'!='),                         # != comparison
    ('GREATER_EQUAL', r'>='),                     # >= comparison
    ('LESS_EQUAL', r'<='),                        # <= comparison
    ('GREATER_THAN', r'>'),                       # > operator
    ('LESS_THAN', r'<'),                          # < operator
    ('LPAREN', r'\('),                            # ( delimiter
    ('RPAREN', r'\)'),                            # ) delimiter
    ('LBRACE', r'\{'),                            # { delimiter
    ('RBRACE', r'\}'),                            # } delimiter
    ('LBRACKET', r'\['),                          # [ delimiter
    ('RBRACKET', r'\]'),                          # ] delimiter
    ('COLON', r':'),                              # : delimiter
    ('COMMA', r','),                              # , delimiter
    ('NEWLINE', r'\n'),                           # Line endings
    ('INDENT', r'[ \t]+'),                        # Indentation (general)
    ('SKIP', r'[ \t]+'),                          # Whitespace
    ('MISMATCH', r'.'),                           # Any other character
]


_token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in _TOKEN_SPECS)
get_token = re.compile(_token_regex).match
