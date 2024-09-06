from typing import Any, Optional
from .token import Tokens, Token
from .environment import Environment, BuiltinFunction
from .builtins import add_builtins
from .node import *


class Interpreter:
    """Responsible for initializing an environment and processing the abstract
    syntax tree (AST) created by the parser.
    """

    def __init__(self, environment: Optional[Environment] = None) -> None:
        self.environment: Environment = environment if environment is not None else Environment()
        add_builtins(self.environment)

    def interpret(self, node: ASTNode) -> Optional[Any]:
        """Processes a node of the AST. This could be an entire program or a singular frame."""
        if isinstance(node, ProgramNode):
            self.visit_program(node)
        elif isinstance(node, DeclarationNode):
            self.visit_declaration(node)
            return None
        elif isinstance(node, FunctionDefNode):
            self.visit_function_definition(node)
            return None
        elif isinstance(node, FunctionCallNode):
            return self.visit_function_call(node)
        elif isinstance(node, ExpressionNode):
            return self.visit_expression(node)
        elif isinstance(node, SameFrameNode):
            self.visit_same_frame(node)
            return None
        else:
            raise Exception(f"Unknown node type: {type(node)}")

    def visit_program(self, node: ProgramNode) -> None:
        """Processes all statements within the program, 'line-by-line'"""
        for statement in node.statements:
            self.interpret(statement)

    def visit_declaration(self, node: DeclarationNode) -> None:
        """Check if a declaration such as a variables."""
        # Interpret the expression to get the value.
        value: Any = self.interpret(node.expression)

        # Cast the value to the declared type.
        if node.var_type == 'int':
            value = int(value)
        elif node.var_type == 'float':
            value = float(value)
        elif node.var_type == 'str':
            value = str(value)
        else:
            raise TypeError(f"Unsupported variable type: {node.var_type}")

        # Store the name / value into the environment.
        self.environment.set(node.identifier, value)

    def visit_function_definition(self, node: FunctionDefNode) -> None:
        """Stores the user-defined function into the environment."""
        self.environment.set_function(node.name, node.params, node.body)

    def visit_function_call(self, node: FunctionCallNode) -> Optional[Any]:
        """Processes a function call by checking the environment and then calling it.
        Built-in functions have priority in naming over user-defined.
        """
        func = self.environment.get_function(node.name)
        if isinstance(func, BuiltinFunction):
            # Checks the built-in functions first.
            args = [self.interpret(arg) for arg in node.args]
            return func(self.environment, *args)
        else:
            # Process a function, creating a new local environment for it.
            params, body = func
            local_env = Environment()
            for (param_name, _), arg in zip(params, node.args):
                local_env.set(param_name, self.interpret(arg))

            # Interpret the body of the function.
            interpreter = Interpreter(environment=local_env)
            result = None
            for stmt in body:
                result = interpreter.interpret(stmt)

            return result

    def visit_expression(self, node: ExpressionNode) -> Any:
        """Process and expression node."""
        if node.operator is None:
            # Handle literals and identifiers.
            if isinstance(node.left, str):
                if node.left.isdigit():
                    # Handle integer literals.
                    return int(node.left)
                try:
                    # Try to convert to float.
                    return float(node.left)
                except ValueError:
                    if node.left.startswith('"') and node.left.endswith('"'):
                        # Handle string literals.
                        return node.left.strip('"')
                    else:
                        # It's an identifier, so get the value from the environment.
                        return self.environment.get(node.left)
            else:
                # Numeric value, nothing needed to be done.
                return node.left
        else:
            # Handle binary operations.
            left_val: Any = self.interpret(node.left)
            right_val: Any = self.interpret(node.right)

            if node.operator[0] == Tokens.PLUS:
                return left_val + right_val
            elif node.operator[0] == Tokens.MINUS:
                return left_val - right_val
            elif node.operator[0] == Tokens.MULTIPLY:
                return left_val * right_val
            elif node.operator[0] == Tokens.DIVIDE:
                return left_val / right_val
            elif node.operator[0] == Tokens.MODULUS:
                return left_val % right_val
            else:
                raise Exception(f"Unknown operator: {node.operator}")

    def visit_same_frame(self, node: SameFrameNode) -> None:
        """Processes nodes / statements that are required to happen on
        the same frame of each other.
        """
        for statement in node.statements:
            self.interpret(statement)
