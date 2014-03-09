import pytest

import email.utils


def test_email():
    assert(email.utils.parseaddr
           ('first_name last_name <id@site.com>') ==
           ('first_name last_name', 'id@site.com'))

if __name__ == '__main__':
    test_email()
