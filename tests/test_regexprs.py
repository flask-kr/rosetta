import pytest

from framework.core.regexprs import EMAIL_REG_EXPR


def test_email():
    print EMAIL_REG_EXPR.match('name@site.com')