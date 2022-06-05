import pytest

from pylox.token import Token, TokenType
from pylox.scanner import Scanner

filename = "/tmp/scanner_test.lox"


def test_scanner_0():
    with open(filename, "w") as f:
        src_content = 'print "Hello World";'
        f.write(src_content)

    expected = [
        Token(TokenType.PRINT, "print", 0),
        Token(TokenType.STRING, "Hello World", 0),
        Token(TokenType.SEMICOLON, ";", 0)
    ]

    scanner = Scanner(filename)

    for idx, t in enumerate(scanner.getTokens()):
        assert expected[idx] == t, f"{expected[idx]} vs {t}"


def test_scanner_1():
    with open(filename, "w") as f:
        src_content = 'print "cake==awesome or a+b=10";'
        f.write(src_content)

    expected = [
        Token(TokenType.PRINT, "print", 0),
        Token(TokenType.STRING, "cake==awesome or a+b=10", 0),
        Token(TokenType.SEMICOLON, ";", 0)
    ]

    scanner = Scanner(filename)

    for idx, t in enumerate(scanner.getTokens()):
        assert expected[idx] == t, f"{expected[idx]} vs {t}"


def test_scanner_2():
    with open(filename, "w") as f:
        src_content = 'print "cake==awesome or a+b=10";\nprint "hellloooooo";'
        f.write(src_content)

    expected = [
        Token(TokenType.PRINT, "print", 0),
        Token(TokenType.STRING, "cake==awesome or a+b=10", 0),
        Token(TokenType.SEMICOLON, ";", 0),
        Token(TokenType.PRINT, "print", 1),
        Token(TokenType.STRING, "hellloooooo", 1),
        Token(TokenType.SEMICOLON, ";", 1),
    ]

    scanner = Scanner(filename)

    for idx, t in enumerate(scanner.getTokens()):
        assert expected[idx] == t, f"{expected[idx]} vs {t}"


def test_scanner_3():
    with open(filename, "w") as f:
        src_content = 'var a = beta + c;\nvar a=beta+c;'
        f.write(src_content)

    expected = [
        Token(TokenType.VAR, "var", 0),
        Token(TokenType.IDENTIFIER, "a", 0),
        Token(TokenType.EQUAL, "=", 0),
        Token(TokenType.IDENTIFIER, "beta", 0),
        Token(TokenType.PLUS, "+", 0),
        Token(TokenType.IDENTIFIER, "c", 0),
        Token(TokenType.SEMICOLON, ";", 0),

        Token(TokenType.VAR, "var", 1),
        Token(TokenType.IDENTIFIER, "a", 1),
        Token(TokenType.EQUAL, "=", 1),
        Token(TokenType.IDENTIFIER, "beta", 1),
        Token(TokenType.PLUS, "+", 1),
        Token(TokenType.IDENTIFIER, "c", 1),
        Token(TokenType.SEMICOLON, ";", 1),
    ]

    scanner = Scanner(filename)

    for idx, t in enumerate(scanner.getTokens()):
        assert expected[idx] == t, f"{expected[idx]} vs {t}"


def test_scanner_4():
    with open(filename, "w") as f:
        src_content = 'var poop = "one" + "two" + alpha + b + "three" + fn("input1", b, "input2") + "four" + (a*b)/5;'
        f.write(src_content)

    expected = [
        Token(TokenType.VAR, "var", 0),
        Token(TokenType.IDENTIFIER, "poop", 0),
        Token(TokenType.EQUAL, "=", 0),
        Token(TokenType.STRING, "one", 0),
        Token(TokenType.PLUS, "+", 0),
        Token(TokenType.STRING, "two", 0),
        Token(TokenType.PLUS, "+", 0),
        Token(TokenType.IDENTIFIER, "alpha", 0),
        Token(TokenType.PLUS, "+", 0),
        Token(TokenType.IDENTIFIER, "b", 0),
        Token(TokenType.PLUS, "+", 0),
        Token(TokenType.STRING, "three", 0),
        Token(TokenType.PLUS, "+", 0),
        Token(TokenType.IDENTIFIER, "fn", 0),
        Token(TokenType.LEFT_PAREN, "(", 0),
        Token(TokenType.STRING, "input1", 0),
        Token(TokenType.COMMA, ",", 0),
        Token(TokenType.IDENTIFIER, "b", 0),
        Token(TokenType.COMMA, ",", 0),
        Token(TokenType.STRING, "input2", 0),
        Token(TokenType.RIGHT_PAREN, ")", 0),
        Token(TokenType.PLUS, "+", 0),
        Token(TokenType.STRING, "four", 0),
        Token(TokenType.PLUS, "+", 0),
        Token(TokenType.LEFT_PAREN, "(", 0),
        Token(TokenType.IDENTIFIER, "a", 0),
        Token(TokenType.STAR, "*", 0),
        Token(TokenType.IDENTIFIER, "b", 0),
        Token(TokenType.RIGHT_PAREN, ")", 0),
        Token(TokenType.SLASH, "/", 0),
        Token(TokenType.NUMBER, "5", 0),
        Token(TokenType.SEMICOLON, ";", 0),
    ]

    scanner = Scanner(filename)

    for idx, t in enumerate(scanner.getTokens()):
        assert expected[idx] == t, f"{expected[idx]} vs {t}"
