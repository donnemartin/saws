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
import re
from saws.commands import AwsCommands


class CommandsTest(unittest.TestCase):

    def test_all_commands(self):
        aws_commands = AwsCommands()
        command_lists = aws_commands.all_commands
        num_results_list = [None] * \
            aws_commands.CommandType.NUM_TYPES.value
        with open(AwsCommands.DATA_PATH) as f:
            for line in f:
                line = re.sub('\n', '', line)
                for command_header in aws_commands.headers:
                    if command_header in line:
                        command_type_value = aws_commands \
                            .header_to_type_map[command_header].value
                        num_results_list[command_type_value] = \
                            int(line.strip(command_header))
                        continue
        for index, num_results in enumerate(num_results_list):
            assert(len(command_lists[index]) == num_results)
