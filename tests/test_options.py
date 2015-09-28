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
from saws.saws import Saws


class OptionsTest(unittest.TestCase):

    def setUp(self):
        self.create_options()

    def create_options(self):
        self.saws = Saws(refresh_resources=False)
        self.options = self.saws.completer.options

    def test_create_options_map(self):
        # TODO: Implement
        pass
