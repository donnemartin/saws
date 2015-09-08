#!/usr/bin/env python
from __future__ import unicode_literals
import unittest
from test_completer import CompleterTest  # NOQA
from test_commands import CommandsTest  # NOQA
try:
    from test_cli import CliTest  # NOQA
except:
# pexpect import fails on Windows
    pass


if __name__ == '__main__':
    unittest.main()
