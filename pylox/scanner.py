import re

from typing import List, Tuple

from pylox.token import Token, TokenType, TokenKeywords, TokenCharacters


class Scanner:
    def __init__(self, src: str) -> None:
        self.__src = src
        self.__tokens = []

        self.__scan()

    def __scan(self) -> None:
        with open(self.__src) as f:
            lines = f.readlines()

            for idx, line in enumerate(lines):
                tokens = Scanner.__processLine(line, idx)
                self.__tokens += tokens

    def getTokens(self) -> List[Token]:
        return self.__tokens

    def __processLine(line: str, line_num: int) -> List[Token]:
        tokens = []

        for expression in [e + ";" for e in line.rstrip().lstrip().split(";") if e]:
            for idx, s in enumerate(expression.split("\"")):
                # Strings end up being odd numbered because a line can never
                # start with a string
                if idx % 2 == 1:
                    tokens.append(Token(TokenType.STRING, s, line_num))
                else:
                    for lexeme in re.split('(\\W)', s):
                        if len(lexeme) == 0 or lexeme == ' ':
                            continue

                        # First, search for keywords
                        found, type = Scanner.__findKeywords(lexeme)
                        if found:
                            tokens.append(Token(type, lexeme, line_num))
                            continue

                        # Look for characters
                        if len(lexeme) == 1:
                            found, type = Scanner.__findSingleCharacters(
                                lexeme)
                            if found:
                                tokens.append(Token(type, lexeme, line_num))
                                continue

                        # Look for numbers
                        if lexeme.isnumeric():
                            tokens.append(
                                Token(TokenType.NUMBER, lexeme, line_num))
                            continue

                        # Anything left is an identifier
                        for t in TokenType:
                            assert lexeme.find(t.value) < 0, \
                                f"{t.value} found when there should only be identifiers"

                        tokens.append(
                            Token(TokenType.IDENTIFIER, lexeme, line_num))

        return tokens

    def __findKeywords(lexeme: str) -> Tuple[bool, TokenType]:
        for t in TokenKeywords:
            if t.value.value == lexeme:
                return (True, t.value)

        return (False, TokenType.NIL)

    def __findSingleCharacters(lexeme: str) -> Tuple[bool, TokenType]:
        for c in lexeme:
            for t in TokenCharacters:
                if t.value.value == c:
                    return (True, t.value)

        return (False, TokenType.NIL)
