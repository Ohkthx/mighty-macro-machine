from typing import Optional, Iterator
from .token import Tokens, Token
from .node import *


class Parser:
    """Takes the tokens from the Lexer and builds the Abstract Syntax Tree (AST)
    for the interpreter to process.
    """

    def __init__(self, tokens: Iterator[Token]) -> None:
        """Initializes the Parser with a list of tokens and sets the position to the start."""
        self.tokens: list[Token] = list(tokens)
        self.position: int = 0

    def current_token(self) -> Optional[Token]:
        """Obtains the current token that is being processed."""
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def advance(self) -> None:
        """Moves the position to the next token."""
        self.position += 1

    def expect(self, token_type: Tokens) -> None:
        """Validates the current token is of the expected type, 
        and advances to the next token if it is."""
        token = self.current_token()
        if token and token[0] == token_type:
            self.advance()
        else:
            raise SyntaxError(f"Expected {token_type}, got {token}")

    def parse(self) -> ProgramNode:
        """Parses the entire program and returns the root node of the AST."""
        statements: list[ASTNode] = []

        while self.current_token() is not None:
            if self.current_token()[0] == Tokens.IDENTIFIER:
                statements.append(self.parse_identifier())
            elif self.current_token()[0] == Tokens.FUNC:
                statements.append(self.parse_function_definition())
            elif self.current_token()[0] == Tokens.EOL:
                self.advance()  # Skip EOL and continue parsing.
            else:
                raise SyntaxError(f"Unexpected token {self.current_token()}")

        return ProgramNode(statements)

    def parse_identifier(self) -> ASTNode:
        """Parses an identifier which could be a variable declaration or a function call."""
        first_statement = self.parse_declaration_or_function_call()
        statements: list[ASTNode] = [first_statement]

        # Handle multiple statements on the same frame connected by `->`.
        while self.current_token() is not None:
            if self.current_token()[0] == Tokens.NEXT:
                self.advance()  # Skip the NEXT token.
                statements.append(self.parse_declaration_or_function_call())
            elif self.current_token()[0] == Tokens.EOL:
                self.advance()  # Skip EOL token.
                if self.current_token() and self.current_token()[0] == Tokens.NEXT:
                    self.advance()  # Skip the NEXT token.
                    statements.append(self.parse_declaration_or_function_call())
                else:
                    break
            else:
                break

        if len(statements) > 1:
            return SameFrameNode(statements)
        return first_statement

    def parse_declaration_or_function_call(self) -> ASTNode:
        """Determines if the identifier is part of a variable declaration or a function call."""
        if self.is_declaration():
            return self.parse_declaration()
        else:
            return self.parse_function_call()

    def is_declaration(self) -> bool:
        """Checks if the current token sequence represents a variable declaration 
        by looking ahead for a colon."""
        return (self.position + 1 < len(self.tokens) and
                self.tokens[self.position + 1][0] == Tokens.COLON)

    def parse_declaration(self) -> DeclarationNode:
        """Parses a series of tokens into a variable declaration including its type and value."""
        identifier = self.current_token()[1]
        self.advance()
        self.expect(Tokens.COLON)
        var_type = self.current_token()[1]
        self.advance()
        self.expect(Tokens.ASSIGN)
        expression = self.parse_expression()
        return DeclarationNode(var_type, identifier, expression)

    def parse_function_definition(self) -> FunctionDefNode:
        """Parses a series of tokens into a function definition, including its parameters and body."""
        self.expect(Tokens.FUNC)
        func_name = self.current_token()[1]
        self.advance()
        self.expect(Tokens.LPAREN)
        params = self.parse_params()
        self.expect(Tokens.RPAREN)
        self.expect(Tokens.LBRACE)
        body = self.parse_statements_in_block()
        self.expect(Tokens.RBRACE)
        return FunctionDefNode(func_name, params, body)

    def parse_params(self) -> list[tuple[str, str]]:
        """Parses the parameters of a function definition, 
        returning a list of tuples containing parameter names and types."""
        params: list[tuple[str, str]] = []
        if self.current_token()[0] != Tokens.RPAREN:
            param_name = self.current_token()[1]
            self.advance()
            self.expect(Tokens.COLON)
            param_type = self.current_token()[1]
            params.append((param_name, param_type))
            self.advance()
            while self.current_token()[0] == Tokens.COMMA:
                self.advance()
                param_name = self.current_token()[1]
                self.advance()
                self.expect(Tokens.COLON)
                param_type = self.current_token()[1]
                params.append((param_name, param_type))
                self.advance()
        return params

    def parse_function_call(self) -> FunctionCallNode:
        """Parses a function call from the tokens, including the function name and its arguments."""
        func_name = self.current_token()[1]
        self.advance()
        self.expect(Tokens.LPAREN)
        args = self.parse_args()
        self.expect(Tokens.RPAREN)
        return FunctionCallNode(func_name, args)

    def parse_args(self) -> list[ASTNode]:
        """Parses the arguments of a function call, returning a list of expression nodes."""
        args: list[ASTNode] = []
        if self.current_token()[0] != Tokens.RPAREN:
            args.append(self.parse_expression())
            while self.current_token()[0] == Tokens.COMMA:
                self.advance()
                args.append(self.parse_expression())
        return args

    def parse_expression(self) -> ASTNode:
        """Parses an expression from the tokens, starting with a term."""
        return self.parse_term()

    def parse_term(self) -> ASTNode:
        """Parses a term and handles binary operations like addition and subtraction."""
        node = self.parse_factor()
        while self.current_token() and self.current_token()[0] in (Tokens.PLUS, Tokens.MINUS):
            operator = self.current_token()
            self.advance()
            right = self.parse_factor()
            node = ExpressionNode(node, operator, right)
        return node

    def parse_factor(self) -> ASTNode:
        """Parses a factor, which can be a number, string, identifier, or a parenthesized expression."""
        token = self.current_token()
        if token[0] == Tokens.NUMBER:
            self.advance()
            return ExpressionNode(token[1])  # Return the number literal.
        elif token[0] == Tokens.STRING:
            self.advance()
            return ExpressionNode(token[1])  # Return the string literal.
        elif token[0] == Tokens.IDENTIFIER:
            self.advance()
            return ExpressionNode(token[1])  # Return the identifier name.
        elif token[0] == Tokens.LPAREN:
            self.advance()
            node = self.parse_expression()
            self.expect(Tokens.RPAREN)
            return node
        else:
            raise SyntaxError(f"Unexpected token {token}")

    def parse_statements_in_block(self) -> list[ASTNode]:
        """Parses a block of statements such as for functions or if/whiles."""
        statements: list[ASTNode] = []
        while self.current_token() and self.current_token()[0] != Tokens.RBRACE:
            if self.current_token()[0] == Tokens.EOL:
                self.advance()  # Skip EOL within blocks
            elif self.current_token()[0] == Tokens.IDENTIFIER:
                statements.append(self.parse_identifier())
            else:
                raise SyntaxError(f"Unexpected token in block: {self.current_token()}")
        return statements
