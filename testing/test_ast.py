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
        return f"Expr[{self._value}]"


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
        return f"Bin[{self._left} {self._op} {self._right}]"


class UnaryOp(Expr):
    def __init__(self, op: TokenType, right: Expr, ) -> None:
        self._op = op
        self._right = right

        super().__init__(self)

    def __str__(self):
        return f"Unary[{self._op} {self._right}]"


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
        node = self._unary()

        while self.__current_token.type in (TokenType.STAR, TokenType.SLASH):
            token = self.__current_token
            if token.type == TokenType.STAR:
                self._consume(token.type)
                node = BinaryOp(node, TokenType.STAR, self._unary())
            elif token.type == TokenType.SLASH:
                self._consume(token.type)
                node = BinaryOp(node, TokenType.SLASH, self._unary())

        return node

    def _term(self):
        """Term detector
        factor ( ( "+" | "-" ) factor ) *
        """
        node = self._factor()

        while self.__current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.__current_token
            if token.type == TokenType.PLUS:
                self._consume(token.type)
                node = BinaryOp(node, TokenType.PLUS, self._factor())
            elif token.type == TokenType.MINUS:
                self._consume(token.type)
                node = BinaryOp(node, TokenType.MINUS, self._factor())

        return node

    def _compare(self):
        """Comparison detector
        term ( ( ">" | "<" | ">=" | "<=" ) term ) *
        """
        node = self._term()

        while self.__current_token.type in (TokenType.GREATER_THAN, TokenType.GREATER_EQUAL, TokenType.LESS_THAN, TokenType.LESS_EQUAL):
            token = self.__current_token
            if token.type == TokenType.GREATER_THAN:
                self._consume(token.type)
                node = BinaryOp(node, TokenType.GREATER_THAN, self._term())
            elif token.type == TokenType.GREATER_EQUAL:
                self._consume(token.type)
                node = BinaryOp(node, TokenType.GREATER_EQUAL, self._term())
            elif token.type == TokenType.LESS_THAN:
                self._consume(token.type)
                node = BinaryOp(node, TokenType.LESS_THAN, self._term())
            elif token.type == TokenType.LESS_EQUAL:
                self._consume(token.type)
                node = BinaryOp(node, TokenType.LESS_EQUAL, self._term())

        return node

    def _equality(self):
        # TODO: Need to fix scanner to get equality to work. It's not picking up the '==' or '!='
        """Equality detector
        compare ( ( "!=" | "==" ) compare ) *
        """
        node = self._compare()

        while self.__current_token.type in (TokenType.EQUAL_EQUAL, TokenType.EXCLAIMATION_EQUAL):
            token = self.__current_token
            if token.type == TokenType.EQUAL_EQUAL:
                self._consume(token.type)
                node = BinaryOp(node, TokenType.EQUAL_EQUAL, self._compare())
            elif token.type == TokenType.EXCLAIMATION_EQUAL:
                self._consume(token.type)
                node = BinaryOp(
                    node, TokenType.EXCLAIMATION_EQUAL, self._compare())

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
    code = "5 < (1/4 + -2 - (3+5) * 6 * 7) > 10.0"

    # TODO: This doesn't work - scanner isn't picking up '<=' or '=='
    # code = "5 < (1/4 + -2 - (3+5) * 6 * 7) <= 10.0"
    # code = "5 == 10"

    with open(filename, "w") as f:
        f.write(code)

    scanner = Scanner(filename)
    parser = Parser(scanner.getTokens())
    node = parser.walk()

    print(node)

    # assert False
