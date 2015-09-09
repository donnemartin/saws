# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import unittest
import pip
import pexpect
import mock
from saws.keys import get_key_manager
#from prompt_toolkit import CommandLineInterface
from prompt_toolkit.buffer import Buffer
#from prompt_toolkit.keys import Keys


class KeysTest(unittest.TestCase):

    #@mock.patch.object(CommandLineInterface.current_buffer,
    #                   'insert_text',
    #                   autospec=True)
    @mock.patch.object(Buffer,
                       'insert_text',
                       autospec=True)
    def test_handle_f1(self, mock_insert_text):
        pass

    """
    def test_run_cli(self):
        self.cli = None
        self.step_cli_installed()
        self.step_run_cli()
        self.step_see_prompt()
        #self.cli.Keys.F1
        #self.cli.sendline(Keys.F1)
        #self.cli.expect('saws> help')
        self.step_send_ctrld()
    """

    def step_cli_installed(self):
        """
        Make sure saws is in installed packages.
        """
        dists = set([di.key for di in pip.get_installed_distributions()])
        assert 'saws' in dists

    def step_run_cli(self):
        """
        Run the process using pexpect.
        """
        self.cli = pexpect.spawnu('saws')

    def step_see_prompt(self):
        """
        Expect to see prompt.
        """
        self.cli.expect('saws> ')

    def step_send_ctrld(self):
        """
        Send Ctrl + D to exit.
        """
        self.cli.sendcontrol('d')
        self.cli.expect(pexpect.EOF)
