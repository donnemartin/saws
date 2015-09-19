# -*- coding: utf-8 -*-

# Copyright 2015 Donne Martin. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from __future__ import unicode_literals
from __future__ import print_function
import mock
import unittest
from pygments.token import Token
from saws.saws import Saws
from saws.toolbar import Toolbar


class ToolbarTest(unittest.TestCase):

    @mock.patch('saws.resources.print')
    def setUp(self, mock_print):
        self.saws = Saws()
        self.toolbar = Toolbar(self.saws.get_color,
                               self.saws.get_fuzzy_match,
                               self.saws.get_shortcut_match)
        mock_print.assert_called_with('Loaded resources from cache')

    def test_toolbar_on(self):
        expected = [
            (Token.Toolbar, ' [F1] Docs '),
            (Token.Toolbar.On, ' [F2] Color: ON '),
            (Token.Toolbar.On, ' [F3] Fuzzy: ON '),
            (Token.Toolbar.On, ' [F4] Shortcuts: ON '),
            (Token.Toolbar, ' [F5] Refresh '),
            (Token.Toolbar, ' [F10] Exit ')]
        assert expected == self.toolbar.handler(None)

    def test_toolbar_off(self):
        self.saws.set_color(False)
        self.saws.set_fuzzy_match(False)
        self.saws.set_shortcut_match(False)
        expected = [
            (Token.Toolbar, ' [F1] Docs '),
            (Token.Toolbar.Off, ' [F2] Color: OFF '),
            (Token.Toolbar.Off, ' [F3] Fuzzy: OFF '),
            (Token.Toolbar.Off, ' [F4] Shortcuts: OFF '),
            (Token.Toolbar, ' [F5] Refresh '),
            (Token.Toolbar, ' [F10] Exit ')]
        assert expected == self.toolbar.handler(None)
