from typing import Optional, Union
from .token import Token


# Represents a parameter for a function.
Param = tuple[str, str]


class ASTNode:
    """Basic node that all others derive from."""
    pass


class DeclarationNode(ASTNode):
    """Represents a variable name, type, and value."""

    def __init__(self, var_type: str, identifier: str, expression: ASTNode) -> None:
        self.var_type: str = var_type
        self.identifier: str = identifier
        self.expression: ASTNode = expression


class FunctionDefNode(ASTNode):
    """Represents a function that is user-defined."""

    def __init__(self, name: str, params: list[Param], body: list[ASTNode]) -> None:
        self.name: str = name  # Identifier of the function.
        self.params: list[tuple[str, str]] = params  # List of (param_name, param_type)
        self.body: list[ASTNode] = body  # Sequential statements.


class FunctionCallNode(ASTNode):
    """Represents a function call and the parameters passed."""

    def __init__(self, name: str, args: list[ASTNode]) -> None:
        self.name: str = name  # Identifier for the function.
        self.args: list[ASTNode] = args  # Arguments / parameters passed.


class ExpressionNode(ASTNode):
    """An expression (including Binary Operation.)"""

    def __init__(self, left: Union[str, ASTNode], operator: Optional[Token] = None, right: Optional[ASTNode] = None) -> None:
        self.left: Union[str, ASTNode] = left  # Can be a literal, identifier, or another expression.
        self.operator: Optional[Token] = operator  # The operator, e.g., '+', '-', etc.
        self.right: Optional[ASTNode] = right  # Right-hand side expression.


class SameFrameNode(ASTNode):
    """Similar to functions, these are statements that must be processed on the same frame."""

    def __init__(self, statements: list[ASTNode]) -> None:
        self.statements: list[ASTNode] = statements


class ProgramNode(ASTNode):
    """Represents an entire program, where each node is processed on a frame."""

    def __init__(self, statements: list[ASTNode]) -> None:
        self.statements: list[ASTNode] = statements
