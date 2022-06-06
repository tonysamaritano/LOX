import pytest

from pylox.token import Token, TokenType


def test_token():
    token = Token(TokenType.DOT, ".", 1337)
    assert("[1337] . -> TokenType.DOT" == str(token))
    assert("[1336] . -> TokenType.DOT" != str(token))
    assert("[1337] , -> TokenType.DOT" != str(token))
    assert("[1337] . -> TokenType.WHILE" != str(token))
