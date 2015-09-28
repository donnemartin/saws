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
try:
    from collections import OrderedDict
except:
    from ordereddict import OrderedDict
from enum import Enum
from .data_util import DataUtil


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
        """

        NUM_TYPES = 4
        COMMANDS, SUB_COMMANDS, GLOBAL_OPTIONS, RESOURCE_OPTIONS = \
            range(NUM_TYPES)

    AWS_COMMAND = 'aws'
    AWS_CONFIGURE = 'configure'
    AWS_HELP = 'help'
    AWS_DOCS = 'docs'
    SOURCES_DIR = os.path.dirname(os.path.realpath(__file__))
    SOURCES_PATH = os.path.join(SOURCES_DIR, 'data/SOURCES.txt')

    def __init__(self):
        # TODO: Refactor into DataUtil
        self.command_headers = ['[commands]: ',
                                '[sub_commands]: ',
                                '[global_options]: ',
                                '[resource_options]: ']
        self.command_types = []
        for command_type in self.CommandType:
            if command_type != self.CommandType.NUM_TYPES:
                self.command_types.append(command_type)
        self.header_to_type_map = OrderedDict(zip(self.command_headers,
                                                  self.command_types))
        self.command_lists = [[] for x in range(
            self.CommandType.NUM_TYPES.value)]
        self.all_commands = self._get_all_commands()

    def _get_all_commands(self):
        """Gets all commands from the data/SOURCES.txt file.

        Args:
            * None.

        Returns:
            A list, where each element is a list of completions for each
                CommandType
        """
        return DataUtil().get_data(self.SOURCES_PATH,
                                   self.header_to_type_map,
                                   self.CommandType.COMMANDS,
                                   self.command_lists)
