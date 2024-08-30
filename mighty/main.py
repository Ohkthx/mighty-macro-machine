from lang.lexer import Lexer
from lang.parser import Parser
from lang.interpreter import Interpreter


def main():
    """Main entry point of the application."""
    code = """
        x: float = 2.2 + 3
            -> print(x)
        y: int = 3 -> print(y)
    """
    lexer = Lexer(code)
    tokens = list(lexer.tokenize())
    # for token in tokens:
    #     print(token)

    parser = Parser(tokens)
    ast = parser.parse()
    # for node in ast.statements:
    #     print(node)

    interpreter = Interpreter()
    interpreter.interpret(ast)


if __name__ == "__main__":
    main()
