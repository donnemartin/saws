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
import os
import re
try:
    from collections import OrderedDict
except:
    from ordereddict import OrderedDict
from enum import Enum


class AwsCommands(object):
    """Encapsulates AWS commands.

    Attributes:
        * AWS_COMMAND: A string representing the 'aws' command.
        * AWS_CONFIGURE: A string representing the 'configure' command.
        * AWS_HELP: A string representing the 'help' command.
        * AWS_DOCS: A string representing the 'docs' command.
        * SOURCES_DIR: A string representing the directory containing
            data/SOURCES.txt.
        * SOURCES_PATH: A string representing the full file path of
            data/SOURCES.txt.
        * command_headers: A list denoting the start of each set of
            command types.
        * command_types: A list of enums of CommandType.
        * header_to_type_map: A mapping between command_headers and
            command_types
        * command_lists: A list of lists.  Each list element contains
            completions for each CommandType.
    """

    AWS_COMMAND = 'aws'
    AWS_CONFIGURE = 'configure'
    AWS_HELP = 'help'
    AWS_DOCS = 'docs'
    SOURCES_DIR = os.path.dirname(os.path.realpath(__file__))
    SOURCES_PATH = os.path.join(SOURCES_DIR, 'data/SOURCES.txt')

    def __init__(self):
        self.command_headers = ['[commands]: ',
                                '[sub_commands]: ',
                                '[global_options]: ',
                                '[resource_options]: ',
                                '[ec2_states]: ']
        self.command_types = []
        for command_type in self.CommandType:
            if command_type != self.CommandType.NUM_COMMAND_TYPES:
                self.command_types.append(command_type)
        self.header_to_type_map = OrderedDict(zip(self.command_headers,
                                                  self.command_types))
        self.command_lists = [[] for x in range(
            self.CommandType.NUM_COMMAND_TYPES.value)]

    class CommandType(Enum):
        """Enum specifying the command type.

        Attributes:
            * AWS_COMMAND: A string representing the 'aws' command.
            * AWS_CONFIGURE: A string representing the 'configure' command.
            * AWS_HELP: A string representing the 'help' command.
            * AWS_DOCS: A string representing the 'docs' command.
            * COMMANDS: An int representing commands.
            * SUB_COMMANDS: An int representing subcommands.
            * GLOBAL_OPTIONS: An int representing global options.
            * RESOURCE_OPTIONS: An int representing resource options.
            * EC2_STATES: An int representing ec2 running states.
        """

        NUM_COMMAND_TYPES = 5
        COMMANDS, SUB_COMMANDS, GLOBAL_OPTIONS, RESOURCE_OPTIONS, \
            EC2_STATES = range(NUM_COMMAND_TYPES)

    def get_all_commands(self):
        """Gets all commands from the data/SOURCES.txt file.

        Args:
            * None.

        Returns:
            A list, where each element is a list of completions for each
                CommandType
        """
        command_type = self.CommandType.COMMANDS
        with open(self.SOURCES_PATH) as f:
            for line in f:
                line = re.sub('\n', '', line)
                parsing_header = False
                # Check if we are reading in a command header to determine
                # which set of commands we are parsing
                for key, value in self.header_to_type_map.items():
                    if key in line:
                        command_type = value
                        parsing_header = True
                        break
                if not parsing_header:
                    # Store the command in its associated list
                    self.command_lists[command_type.value].append(line)
            for command_list in self.command_lists:
                command_list.sort()
        return self.command_lists
