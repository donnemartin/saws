# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest
import pip
import pexpect


class CliTest(unittest.TestCase):

    def test_run_cli(self):
        self.cli = None
        self.step_cli_installed()
        self.step_run_cli()
        self.step_see_prompt()
        self.step_send_ctrld()

    def step_cli_installed(self):
        """
        Make sure iawscli is in installed packages.
        """
        dists = set([di.key for di in pip.get_installed_distributions()])
        assert 'iawscli' in dists

    def step_run_cli(self):
        """
        Run the process using pexpect.
        """
        self.cli = pexpect.spawnu('iawscli')

    def step_see_prompt(self):
        """
        Expect to see prompt.
        """
        self.cli.expect('iawscli> ')

    def step_send_ctrld(self):
        """
        Send Ctrl + D to exit.
        """
        self.cli.sendcontrol('d')
        self.cli.expect(pexpect.EOF)
