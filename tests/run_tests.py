#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import unittest
from test_completer import CompleterTest  # NOQA
from test_commands import CommandsTest  # NOQA
from test_resources import ResourcesTest  # NOQA
from test_saws import SawsTest  # NOQA
from test_toolbar import ToolbarTest  # NOQA
from test_keys import KeysTest  # NOQA
try:
    from test_cli import CliTest  # NOQA
except:
    # pexpect import fails on Windows
    pass


if __name__ == '__main__':
    unittest.main()
