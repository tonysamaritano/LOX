import os
import sys

from typing import List

from pylox.token import Token, TokenType


class ParseError(Exception):
    pass


class Expr:
    def __init__(self, value) -> None:
        self.value = value

    def print(self, level: int = 0, indent: int = 2):
        print(f"{' ' * level * indent}{self}")


class Constant(Expr):
    def __init__(self, value: float) -> None:
        super().__init__(value)

    def __str__(self):
        return f"Const[{self.value}]"


class Bool(Expr):
    def __init__(self, value: bool) -> None:
        super().__init__(value)

    def __str__(self):
        return f"Bool[{self.value}]"


class String(Expr):
    def __init__(self, value: str) -> None:
        super().__init__(value)

    def __str__(self):
        return f"String[\'{self.value}\']"


class Nil(Expr):
    def __init__(self) -> None:
        super().__init__(None)

    def __str__(self):
        return f"NIL[]"


class BinaryOp(Expr):
    def __init__(self, left: Expr, op: TokenType, right: Expr) -> None:
        self._left = left
        self._op = op
        self._right = right

        super().__init__(self)

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

    def print(self, level: int = 0, indent: int = 2):
        print(f"{' ' * level * indent}Unary[")
        print(f"{' ' * level * indent}{' ' * indent}{self._op}")
        self._right.print(level+1, indent)
        print(f"{' ' * level * indent}]")


class Parser:
    def __init__(self, tokens: List[Token], filename: str = None) -> None:
        self.__tokens = tokens
        self.__index = 0
        self.__current_token = self.__tokens[self.__index]
        self.__expressions = []
        self.__filename = filename

    def _consume(self, type: TokenType):
        """Consumes tokens as we identify valid expressions"""
        if self.__current_token.type == type:
            self.__index += 1
            self.__current_token = self.__tokens[self.__index]

    def _primary(self):
        """Primary detector
        (NUMBER "." NUMBER) | NUMBER | STRING | true | false | nil
        """
        token = self.__current_token
        if token.type == TokenType.NUMBER:
            self._consume(token.type)
            if self.__current_token.type == TokenType.DOT:
                self._consume(TokenType.DOT)
                decimal = self.__current_token
                self._consume(TokenType.NUMBER)
                return Constant(float(f"{token.lexeme}.{decimal.lexeme}"))
            else:
                return Constant(float(token.lexeme))
        elif token.type == TokenType.STRING:
            self._consume(token.type)
            return String(token.lexeme)
        elif token.type == TokenType.TRUE:
            self._consume(token.type)
            return Bool(True)
        elif token.type == TokenType.FALSE:
            self._consume(token.type)
            return Bool(False)
        elif token.type == TokenType.NIL:
            self._consume(token.type)
            return Nil()
        else:
            raise ParseError(f"Not a valid token {self.__current_token}")

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

    def parse(self) -> List[Expr]:
        # Synchronization Symbols
        synchronize = (
            TokenType.CLASS,
            TokenType.FOR,
            # etc..
        )

        while self.__current_token.type != TokenType.EOF:
            try:
                self.__expressions.append(self._exp())
                self._consume(TokenType.SEMICOLON)
            except ParseError:
                # Print the error
                file = os.path.basename(self.__filename) if self.__filename else self.__filename
                line = self.__current_token.line
                lexeme = self.__current_token.lexeme
                fstr = f"{file}:{line}" if file else f"{line}"
                print(
                    f"\x1b[1;31mParseError at [{fstr}]:\x1b[0m error with '{lexeme}'",
                    file=sys.stderr
                )

                # Synchronize
                while self.__current_token.type != TokenType.EOF:
                    self._consume(self.__current_token.type)

                    if self.__current_token.type in synchronize:
                        break
                    elif self.__current_token.type == TokenType.SEMICOLON:
                        self._consume(TokenType.SEMICOLON)
                        break

        return self.__expressions
