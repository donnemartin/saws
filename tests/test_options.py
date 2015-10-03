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
import unittest
from saws.saws import Saws


class OptionsTest(unittest.TestCase):

    def setUp(self):
        self.create_options()

    def create_options(self):
        self.saws = Saws(refresh_resources=False)
        self.options = self.saws.completer.options

    def test_make_header(self):
        option = '--ec2-state'
        header = '--ec2-state: '
        assert header == self.options._make_options_header(option)

    def test_generate_cluster_states(self):
        self.options.cluster_states = []
        self.options.cluster_states = self.options._generate_cluster_states()
        states = ['STARTING', 'BOOTSTRAPPING', 'RUNNING', 'WAITING',
                  'TERMINATING', 'TERMINATED', 'TERMINATED_WITH_ERRORS']
        for state in states:
            assert state in self.options.cluster_states
