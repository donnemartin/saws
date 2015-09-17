# -*- coding: utf-8 -*-
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
