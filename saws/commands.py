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
from enum import Enum
from .data_util import DataUtil


class AwsCommands(object):
    """Encapsulates AWS commands.

    All commands are listed in the periodically updated data/SOURCES.txt file.

    Attributes:
        * AWS_COMMAND: A string representing the 'aws' command.
        * AWS_CONFIGURE: A string representing the 'configure' command.
        * AWS_HELP: A string representing the 'help' command.
        * AWS_DOCS: A string representing the 'docs' command.
        * DATA_DIR: A string representing the directory containing
            data/SOURCES.txt.
        * DATA_PATH: A string representing the full file path of
            data/SOURCES.txt.
        * data_util: An instance of DataUtil().
        * headers: A list denoting the start of each set of command types.
        * header_to_type_map: A dictionary mapping between headers and
            CommandType.
        * all_commands: A list of all commands, sub_commands, options, etc
            from data/SOURCES.txt.
    """

    class CommandType(Enum):
        """Enum specifying the command type.

        Attributes:
            * COMMANDS: An int representing commands.
            * SUB_COMMANDS: An int representing subcommands.
            * GLOBAL_OPTIONS: An int representing global options.
            * RESOURCE_OPTIONS: An int representing resource options.
            * NUM_TYPES: An int representing the number of command types.
        """

        NUM_TYPES = 4
        COMMANDS, SUB_COMMANDS, GLOBAL_OPTIONS, RESOURCE_OPTIONS = \
            range(NUM_TYPES)

    AWS_COMMAND = 'aws'
    AWS_CONFIGURE = 'configure'
    AWS_HELP = 'help'
    AWS_DOCS = 'docs'
    DATA_DIR = os.path.dirname(os.path.realpath(__file__))
    DATA_PATH = os.path.join(DATA_DIR, 'data/SOURCES.txt')

    def __init__(self):
        self.data_util = DataUtil()
        self.headers = ['[commands]: ',
                        '[sub_commands]: ',
                        '[global_options]: ',
                        '[resource_options]: ']
        self.header_to_type_map = self.data_util.create_header_to_type_map(
            headers=self.headers,
            data_type=self.CommandType)
        self.all_commands = self.data_util.get_data(
            data_file_path=self.DATA_PATH,
            header_to_type_map=self.header_to_type_map,
            data_type=self.CommandType)
