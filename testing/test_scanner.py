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


def test_scanner_class_src():
    scanner = Scanner("testing/src/class.lox")

    expected = [
        Token(TokenType.CLASS, "class", 0),
        Token(TokenType.IDENTIFIER, "Test", 0),
        Token(TokenType.LEFT_BRACE, "{", 1),
        Token(TokenType.IDENTIFIER, "init", 2),
        Token(TokenType.LEFT_PAREN, "(", 2),
        Token(TokenType.IDENTIFIER, "name", 2),
        Token(TokenType.RIGHT_PAREN, ")", 2),
        Token(TokenType.LEFT_BRACE, "{", 3),
        Token(TokenType.THIS, "this", 4),
        Token(TokenType.DOT, ".", 4),
        Token(TokenType.IDENTIFIER, "name", 4),
        Token(TokenType.EQUAL, "=", 4),
        Token(TokenType.IDENTIFIER, "name", 4),
        Token(TokenType.SEMICOLON, ";", 4),
        Token(TokenType.THIS, "this", 5),
        Token(TokenType.DOT, ".", 5),
        Token(TokenType.IDENTIFIER, "member", 5),
        Token(TokenType.EQUAL, "=", 5),
        Token(TokenType.NUMBER, "0", 5),
        Token(TokenType.SEMICOLON, ";", 5),
        Token(TokenType.RIGHT_BRACE, "}", 6),
        Token(TokenType.IDENTIFIER, "name", 8),
        Token(TokenType.LEFT_PAREN, "(", 8),
        Token(TokenType.RIGHT_PAREN, ")", 8),
        Token(TokenType.LEFT_BRACE, "{", 9),
        Token(TokenType.RETURN, "return", 10),
        Token(TokenType.THIS, "this", 10),
        Token(TokenType.DOT, ".", 10),
        Token(TokenType.IDENTIFIER, "name", 10),
        Token(TokenType.SEMICOLON, ";", 10),
        Token(TokenType.RIGHT_BRACE, "}", 11),
        Token(TokenType.RIGHT_BRACE, "}", 12),
        Token(TokenType.SEMICOLON, ";", 12),
        Token(TokenType.CLASS, "class", 14),
        Token(TokenType.IDENTIFIER, "Derived", 14),
        Token(TokenType.LESS_THAN, "<", 14),
        Token(TokenType.IDENTIFIER, "Test", 14),
        Token(TokenType.LEFT_BRACE, "{", 15),
        Token(TokenType.IDENTIFIER, "init", 16),
        Token(TokenType.LEFT_PAREN, "(", 16),
        Token(TokenType.RIGHT_PAREN, ")", 16),
        Token(TokenType.LEFT_BRACE, "{", 17),
        Token(TokenType.SUPER, "super", 18),
        Token(TokenType.DOT, ".", 18),
        Token(TokenType.IDENTIFIER, "init", 18),
        Token(TokenType.LEFT_PAREN, "(", 18),
        Token(TokenType.STRING, "derived", 18),
        Token(TokenType.RIGHT_PAREN, ")", 18),
        Token(TokenType.SEMICOLON, ";", 18),
        Token(TokenType.RIGHT_BRACE, "}", 19),
        Token(TokenType.IDENTIFIER, "math", 21),
        Token(TokenType.LEFT_PAREN, "(", 21),
        Token(TokenType.IDENTIFIER, "a", 21),
        Token(TokenType.COMMA, ",", 21),
        Token(TokenType.IDENTIFIER, "b", 21),
        Token(TokenType.RIGHT_PAREN, ")", 21),
        Token(TokenType.LEFT_BRACE, "{", 22),
        Token(TokenType.IF, "if", 23),
        Token(TokenType.LEFT_PAREN, "(", 23),
        Token(TokenType.IDENTIFIER, "a", 23),
        Token(TokenType.GREATER_THAN, ">", 23),
        Token(TokenType.IDENTIFIER, "b", 23),
        Token(TokenType.RIGHT_PAREN, ")", 23),
        Token(TokenType.LEFT_BRACE, "{", 24),
        Token(TokenType.RETURN, "return", 25),
        Token(TokenType.IDENTIFIER, "a", 25),
        Token(TokenType.MINUS, "-", 25),
        Token(TokenType.IDENTIFIER, "b", 25),
        Token(TokenType.SEMICOLON, ";", 25),
        Token(TokenType.RIGHT_BRACE, "}", 26),
        Token(TokenType.ELSE, "else", 27),
        Token(TokenType.LEFT_BRACE, "{", 28),
        Token(TokenType.RETURN, "return", 29),
        Token(TokenType.IDENTIFIER, "a", 29),
        Token(TokenType.PLUS, "+", 29),
        Token(TokenType.IDENTIFIER, "b", 29),
        Token(TokenType.SEMICOLON, ";", 29),
        Token(TokenType.RIGHT_BRACE, "}", 30),
        Token(TokenType.RIGHT_BRACE, "}", 31),
        Token(TokenType.IDENTIFIER, "whatsup", 33),
        Token(TokenType.LEFT_PAREN, "(", 33),
        Token(TokenType.RIGHT_PAREN, ")", 33),
        Token(TokenType.LEFT_BRACE, "{", 34),
        Token(TokenType.RETURN, "return", 35),
        Token(TokenType.STRING, "hello ", 35),
        Token(TokenType.PLUS, "+", 35),
        Token(TokenType.IDENTIFIER, "math", 35),
        Token(TokenType.LEFT_PAREN, "(", 35),
        Token(TokenType.NUMBER, "1", 35),
        Token(TokenType.COMMA, ",", 35),
        Token(TokenType.NUMBER, "2", 35),
        Token(TokenType.RIGHT_PAREN, ")", 35),
        Token(TokenType.PLUS, "+", 35),
        Token(TokenType.STRING, "\\n", 35),
        Token(TokenType.SEMICOLON, ";", 35),
        Token(TokenType.RIGHT_BRACE, "}", 36),
        Token(TokenType.RIGHT_BRACE, "}", 37),
        Token(TokenType.SEMICOLON, ";", 37),
    ]

    for idx, t in enumerate(scanner.getTokens()):
        assert expected[idx] == t, f"{expected[idx]} vs {t}"
