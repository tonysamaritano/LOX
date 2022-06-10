import pytest

from pylox.scanner import Scanner
from pylox.parser import Parser

""" AST Experiment
https://ruslanspivak.com/lsbasi-part7/#:~:text=An%20abstract%20syntax%20tree%20(AST,the%20operands%20of%20that%20operator.
"""


def test_expression():
    filename = "/tmp/test.lox"
    code = '!(5 > (-1.2/4.4 + -2 - (3+5) * 6.5 * 7) >= 10.0) == 1 != (true == false) + "test" + nil'

    with open(filename, "w") as f:
        f.write(code)

    scanner = Scanner(filename)
    parser = Parser(scanner.getTokens())
    parser.parse()

    # assert False


def test_invalid_primary():
    filename = "/tmp/test.lox"
    code = '^ + 8'

    with open(filename, "w") as f:
        f.write(code)

    scanner = Scanner(filename)
    parser = Parser(scanner.getTokens())

    # This should fail
    fail = False
    try:
        parser.parse()
    except:
        fail = True

    assert fail


def test_double():
    filename = "/tmp/test.lox"
    code = '-1.1337 + 2.1337'

    with open(filename, "w") as f:
        f.write(code)

    scanner = Scanner(filename)
    parser = Parser(scanner.getTokens())
    parser.parse()

