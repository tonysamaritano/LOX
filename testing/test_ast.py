from typing import List
import pytest

from pylox.token import Token, TokenType
from pylox.scanner import Scanner

""" AST Experiment
https://ruslanspivak.com/lsbasi-part7/#:~:text=An%20abstract%20syntax%20tree%20(AST,the%20operands%20of%20that%20operator.
"""


class Expr:
    def __init__(self, value) -> None:
        self._value = value

    def __str__(self) -> str:
        return f"{self._value}"


class Constant(Expr):
    def __init__(self, value: float) -> None:
        super().__init__(value)


class BinaryOp(Expr):
    def __init__(self, left: Expr, op: TokenType, right: Expr, ) -> None:
        self._left = left
        self._op = op
        self._right = right

        super().__init__(self)

    def __str__(self):
        return f"{self._left} {self._op} {self._right}"


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
        NUMBER | STRING | true | false | nil | "(" expr ")"
        """
        token = self.__current_token
        if token.type == TokenType.NUMBER:
            self._consume(TokenType.NUMBER)
            return Constant(float(token.lexeme))

    def _unary(self):
        """Unary detector
        ( "!" | "-" ) | primary
        """
        node = self._primary()

        # while self.__current_token.type in (TokenType.EXCLAIMATION):
        #     pass

        return node

    def _exp(self):
        """Highest level detector"""
        
        # We make a call to then next highest level. It'll keep failing through
        # until it knows what to do with the token and creates a node 
        node = self._unary()

        while self.__current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.__current_token
            if token.type == TokenType.PLUS:
                self._consume(TokenType.PLUS)
                node = BinaryOp(left=node, op=token.type, right=self._unary())

        return node

    def walk(self):
        return self._exp()


def test_asdf():
    filename = "/tmp/test.lox"
    code = "1 + 2"

    with open(filename, "w") as f:
        f.write(code)

    scanner = Scanner(filename)
    parser = Parser(scanner.getTokens())
    node = parser.walk()

    print(node)

    assert False
