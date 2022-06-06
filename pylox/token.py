import enum

from pyparsing import Enum


class TokenType(enum.Enum):
    # Single Character Tokens
    COMMA = ","
    DOT = "."
    EQUAL = "="
    LEFT_BRACE = "{"
    LEFT_PAREN = "("
    RIGHT_BRACE = "}"
    RIGHT_PAREN = ")"
    SEMICOLON = ";"
    QUOTE = "\""

    # Single Character Token Expressions
    EXCLAIMATION = "!"
    GREATER_THAN = ">"
    LESS_THAN = "<"
    MINUS = "-"
    PLUS = "+"
    SLASH = "/"
    STAR = "*"

    # Two Character Token Expressions
    EQUAL_EQUAL = "=="
    EXCLAIMATION_EQUAL = "!="
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="

    # Keywords
    AND = "and"
    CLASS = "class"
    ELSE = "else"
    FALSE = "false"
    FOR = "for"
    FUN = "fun"
    IF = "if"
    NIL = "nil"
    OR = "or"
    PRINT = "print"
    RETURN = "return"
    SUPER = "super"
    THIS = "this"
    TRUE = "true"
    VAR = "var"
    WHILE = "while"

    # Literals
    IDENTIFIER = "identifiers"
    NUMBER = "number"
    STRING = "string"

    EOF = "eof"


class TokenKeywords(Enum):
    """This is a helper enum so we can easily search for tokens that can only
    exist as keywords"""
    AND = TokenType.AND
    CLASS = TokenType.CLASS
    ELSE = TokenType.ELSE
    FALSE = TokenType.FALSE
    FOR = TokenType.FOR
    FUN = TokenType.FUN
    IF = TokenType.IF
    NIL = TokenType.NIL
    OR = TokenType.OR
    PRINT = TokenType.PRINT
    RETURN = TokenType.RETURN
    SUPER = TokenType.SUPER
    THIS = TokenType.THIS
    TRUE = TokenType.TRUE
    VAR = TokenType.VAR
    WHILE = TokenType.WHILE

class TokenCharacters(Enum):
    """This is a helper enum so we can easily search for tokens that don't need
    to exist by themselves"""
    COMMA = TokenType.COMMA
    DOT = TokenType.DOT
    EQUAL = TokenType.EQUAL
    LEFT_BRACE = TokenType.LEFT_BRACE
    LEFT_PAREN = TokenType.LEFT_PAREN
    RIGHT_BRACE = TokenType.RIGHT_BRACE
    RIGHT_PAREN = TokenType.RIGHT_PAREN
    SEMICOLON = TokenType.SEMICOLON
    QUOTE = TokenType.QUOTE
    EXCLAIMATION = TokenType.EXCLAIMATION
    GREATER_THAN = TokenType.GREATER_THAN
    LESS_THAN = TokenType.LESS_THAN
    MINUS = TokenType.MINUS
    PLUS = TokenType.PLUS
    SLASH = TokenType.SLASH
    STAR = TokenType.STAR
    EQUAL_EQUAL = TokenType.EQUAL_EQUAL
    EXCLAIMATION_EQUAL = TokenType.EXCLAIMATION_EQUAL
    GREATER_EQUAL = TokenType.GREATER_EQUAL
    LESS_EQUAL = TokenType.LESS_EQUAL

class Token:
    def __init__(self, type: TokenType, lexeme: str, line: int):
        self.type = type
        self.lexeme = lexeme
        self.line = line

    def __str__(self) -> str:
        return f"[{self.line}] {self.lexeme} -> {self.type}"

    def __eq__(self, obj):
        return self.type == obj.type \
            and self.lexeme == obj.lexeme \
            and self.line == obj.line
