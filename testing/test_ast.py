import pytest

from typing import List

from pylox.token import Token, TokenType
from pylox.scanner import Scanner

""" AST Experiment
https://ruslanspivak.com/lsbasi-part7/#:~:text=An%20abstract%20syntax%20tree%20(AST,the%20operands%20of%20that%20operator.
"""


class Expr:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"Expr[{self.value}]"

    def print(self, level: int = 0, indent: int = 2):
        if level > 20:
            print("max recursion")
            return

        if issubclass(type(self.value), Expr):
            self.value.print(level + 1, indent)
        else:
            print(f"{' ' * level * indent}{self.value}")


class Constant(Expr):
    def __init__(self, value: float) -> None:
        super().__init__(value)


class Bool(Expr):
    def __init__(self, value: bool) -> None:
        super().__init__(value)


class BinaryOp(Expr):
    def __init__(self, left: Expr, op: TokenType, right: Expr, ) -> None:
        self._left = left
        self._op = op
        self._right = right

        super().__init__(self)

    def __str__(self):
        return f"Binary[{self._left} {self._op} {self._right}]"

    def print(self, level: int = 0, indent: int = 2):
        print(f"{' ' * level * indent}Binary[")
        self._left.print(level+1, indent)
        print(f"{' ' * level * indent}{' ' * indent}{self._op}")
        self._right.print(level+1, indent)
        print(f"{' ' * level * indent}]")


class UnaryOp(Expr):
    def __init__(self, op: TokenType, right: Expr) -> None:
        self._op = op
        self._right = right

        super().__init__(self)

    def __str__(self):
        return f"Unary[{self._op} {self._right}]"

    def print(self, level: int = 0, indent: int = 2):
        print(f"{' ' * level * indent}Unary[")
        print(f"{' ' * level * indent}{' ' * indent}{self._op}")
        self._right.print(level+1, indent)
        print(f"{' ' * level * indent}]")


class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.__tokens = tokens
        self.__index = 0
        self.__current_token = self.__tokens[self.__index]

    def _consume(self, type: TokenType):
        """Consumes tokens as we identify valid expressions"""
        if self.__current_token.type == type:
            self.__index += 1
            self.__current_token = self.__tokens[self.__index]
        else:
            print(f"ERROR {self.__current_token}")

    def _primary(self):
        """Primary detector
        NUMBER | STRING | true | false | nil
        """
        token = self.__current_token
        if token.type == TokenType.NUMBER:
            self._consume(token.type)
            return Constant(float(token.lexeme))
        elif token.type == TokenType.STRING:
            self._consume(token.type)
            return Expr(token.lexeme)
        elif token.type == TokenType.TRUE:
            self._consume(token.type)
            return Bool(True)
        elif token.type == TokenType.FALSE:
            self._consume(token.type)
            return Bool(False)
        elif token.type == TokenType.NIL:
            self._consume(token.type)
            return Expr(None)
        else:
            raise Exception(f"Not a valid token {self.__current_token}")

    def _grouping(self):
        """Grouping detector
        "(" expr ")"
        | primary
        """
        token = self.__current_token
        if token.type == TokenType.LEFT_PAREN:
            self._consume(token.type)
            node = self._exp()
            self._consume(TokenType.RIGHT_PAREN)
            return node
        else:
            return self._primary()

    def _unary(self):
        """Unary detector
        ( "!" | "-" ) unary
        | grouping
        """
        token = self.__current_token
        if token.type == TokenType.EXCLAIMATION:
            self._consume(token.type)
            return UnaryOp(TokenType.EXCLAIMATION, self._unary())
        elif token.type == TokenType.MINUS:
            self._consume(token.type)
            return UnaryOp(TokenType.MINUS, self._unary())
        else:
            return self._grouping()

    def _factor(self):
        """Factor detector
        unary ( ( "*" | "/" ) unary ) *
        """
        match = (
            TokenType.STAR,
            TokenType.SLASH
        )

        node = self._unary()

        while self.__current_token.type in match:
            token = self.__current_token
            self._consume(token.type)
            node = BinaryOp(node, token.type, self._unary())

        return node

    def _term(self):
        """Term detector
        factor ( ( "+" | "-" ) factor ) *
        """
        match = (
            TokenType.PLUS,
            TokenType.MINUS
        )

        node = self._factor()

        while self.__current_token.type in match:
            token = self.__current_token
            self._consume(token.type)
            node = BinaryOp(node, token.type, self._factor())

        return node

    def _compare(self):
        """Comparison detector
        term ( ( ">" | "<" | ">=" | "<=" ) term ) *
        """
        match = (
            TokenType.GREATER_THAN,
            TokenType.GREATER_EQUAL,
            TokenType.LESS_THAN,
            TokenType.LESS_EQUAL
        )

        node = self._term()

        while self.__current_token.type in match:
            token = self.__current_token
            self._consume(token.type)
            node = BinaryOp(node, token.type, self._term())

        return node

    def _equality(self):
        # TODO: Need to fix scanner to get equality to work. It's not picking up the '==' or '!='
        """Equality detector
        compare ( ( "!=" | "==" ) compare ) *
        """
        match = (
            TokenType.EQUAL_EQUAL,
            TokenType.EXCLAIMATION_EQUAL
        )

        node = self._compare()

        while self.__current_token.type in match:
            token = self.__current_token
            self._consume(token.type)
            node = BinaryOp(node, token.type, self._compare())

        return node

    def _exp(self):
        """Highest level detector
        equality
        """
        return self._equality()

    def walk(self):
        return self._exp()


def test_asdf():
    filename = "/tmp/test.lox"
    code = "5 > (1/4 + -2 - (3+5) * 6 * 7) >= 10 == 1"

    # TODO: This fails because of the dot
    # code = "1.0 + 2.0"

    with open(filename, "w") as f:
        f.write(code)

    scanner = Scanner(filename)
    parser = Parser(scanner.getTokens())
    node = parser.walk()

    node.print(indent=4)

    # assert False
