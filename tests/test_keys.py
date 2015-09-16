# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import mock
import unittest
from prompt_toolkit.key_binding.input_processor import InputProcessor, KeyPress
from prompt_toolkit.key_binding.registry import Registry
from prompt_toolkit.keys import Key, Keys
from pygments.token import Token
from saws.saws import Saws
from saws.keys import KeyManager


class KeysTest(unittest.TestCase):

    @mock.patch('saws.resources.print')
    def setUp(self, mock_print):
        self.saws = Saws()
        mock_print.assert_called_with('Loaded resources from cache')
        self.registry = self.saws.key_manager.manager.registry
        self.processor = self.saws.aws_cli.input_processor
        self.DOCS_HOME_URL = 'http://docs.aws.amazon.com/cli/latest/reference/index.html'

    @mock.patch('saws.saws.webbrowser')
    def test_F1(self, mock_webbrowser):
        self.processor.feed_key(KeyPress(Keys.F1, ''))
        mock_webbrowser.open.assert_called_with(self.DOCS_HOME_URL)

    def test_F2(self):
        orig_color = self.saws.get_color()
        self.processor.feed_key(KeyPress(Keys.F2, ''))
        assert orig_color != self.saws.get_color()

    def test_F3(self):
        orig_fuzzy = self.saws.get_fuzzy_match()
        self.processor.feed_key(KeyPress(Keys.F3, ''))
        assert orig_fuzzy != self.saws.get_fuzzy_match()

    def test_F4(self):
        orig_shortcut = self.saws.get_shortcut_match()
        self.processor.feed_key(KeyPress(Keys.F4, ''))
        assert orig_shortcut != self.saws.get_shortcut_match()

    @mock.patch('saws.resources.print')
    def test_f5(self, mock_print):
        self.processor.feed_key(KeyPress(Keys.F5, ''))
        mock_print.assert_called_with('Done refreshing')
