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
