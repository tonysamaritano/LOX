import pytest

from pylox.scanner import Scanner
from pylox.parser import Parser


def test_expression():
    filename = "/tmp/test.lox"
    code = '!(5 > (-1.2/4.4 + -2 - (3+5) * 6.5 * 7) >= 10.0) == 1 != (true == false) + "test" + nil'

    with open(filename, "w") as f:
        f.write(code)

    scanner = Scanner(filename)
    parser = Parser(scanner.getTokens())
    assert len(parser.parse()) == 1


def test_invalid_primary():
    filename = "/tmp/test.lox"
    code = '^ + 8;1 + 2'

    with open(filename, "w") as f:
        f.write(code)

    scanner = Scanner(filename)
    parser = Parser(scanner.getTokens(), filename)
    assert len(parser.parse()) == 1


def test_double():
    filename = "/tmp/test.lox"
    code = '-1.1337 + 2.1337; 1/0.4'

    with open(filename, "w") as f:
        f.write(code)

    scanner = Scanner(filename)
    parser = Parser(scanner.getTokens())
    assert len(parser.parse()) == 2


def test_multiple_expressions():
    filename = "/tmp/test.lox"

    # 8 valid expressions, 1 invald
    code = """
    1.4 + 2; 3.1465-4; 5.2 * 6; 7/8.1;
    1==1;
    2!=1;
    "test"=="test";
    & # invalid expr @;
    2.1234/3;
    """

    with open(filename, "w") as f:
        f.write(code)

    scanner = Scanner(filename)
    parser = Parser(scanner.getTokens())
    nodes = parser.parse()

    assert len(nodes) == 8
