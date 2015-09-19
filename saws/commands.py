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
from enum import Enum


class AwsCommands(object):
    """Encapsulates AWS commands.

    Attributes:
        * AWS_COMMAND: A string representing the 'aws' command.
        * AWS_CONFIGURE: A string representing the 'configure' command.
        * AWS_HELP: A string representing the 'help' command.
        * AWS_DOCS: A string representing the 'docs' command.
        * COMMANDS_HEADER: A string denoting the start of
            commands in data/SOURCES.txt.
        * SUB_COMMANDS_HEADER: A string denoting the start of
            subcommands in data/SOURCES.txt.
        * GLOBAL_OPTIONS_HEADER: A string denoting the start of
            global options in data/SOURCES.txt.
        * RESOURCE_OPTIONS_HEADER: A string denoting the start of
            resource options in data/SOURCES.txt.
        * EC2_STATES_HEADER: A string denoting the start of
            ec2 states in data/SOURCES.txt.
        * SOURCES_DIR: A string representing the directory containing
            data/SOURCES.txt.
        * SOURCES_PATH: A string representing the full file path of
            data/SOURCES.txt.
    """

    AWS_COMMAND = 'aws'
    AWS_CONFIGURE = 'configure'
    AWS_HELP = 'help'
    AWS_DOCS = 'docs'
    COMMANDS_HEADER = '[commands]: '
    SUB_COMMANDS_HEADER = '[sub_commands]: '
    GLOBAL_OPTIONS_HEADER = '[global_options]: '
    RESOURCE_OPTIONS_HEADER = '[resource_options]: '
    EC2_STATES_HEADER = '[ec2_states]: '
    SOURCES_DIR = os.path.dirname(os.path.realpath(__file__))
    SOURCES_PATH = os.path.join(SOURCES_DIR, 'data/SOURCES.txt')

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

        COMMANDS, SUB_COMMANDS, GLOBAL_OPTIONS, RESOURCE_OPTIONS, \
            EC2_STATES = range(5)

    def generate_all_commands(self):
        """Generates all commands from the data/SOURCES.txt file.

        Args:
            * None.

        Returns:
            A tuple, where each tuple element is a list of:
                * commands
                * sub_commands
                * global_options
                * resource_options
                * ec2_states
        """
        commands = []
        sub_commands = []
        global_options = []
        resource_options = []
        ec2_states = []
        command_type = self.CommandType.COMMANDS
        with open(self.SOURCES_PATH) as f:
            for line in f:
                line = re.sub('\n', '', line)
                if self.COMMANDS_HEADER in line:
                    command_type = self.CommandType.COMMANDS
                    continue
                elif self.SUB_COMMANDS_HEADER in line:
                    command_type = self.CommandType.SUB_COMMANDS
                    continue
                elif self.GLOBAL_OPTIONS_HEADER in line:
                    command_type = self.CommandType.GLOBAL_OPTIONS
                    continue
                elif self.RESOURCE_OPTIONS_HEADER in line:
                    command_type = self.CommandType.RESOURCE_OPTIONS
                    continue
                elif self.EC2_STATES_HEADER in line:
                    command_type = self.CommandType.EC2_STATES
                    continue
                if command_type == self.CommandType.COMMANDS:
                    commands.append(line)
                elif command_type == self.CommandType.SUB_COMMANDS:
                    sub_commands.append(line)
                elif command_type == self.CommandType.GLOBAL_OPTIONS:
                    global_options.append(line)
                elif command_type == self.CommandType.RESOURCE_OPTIONS:
                    resource_options.append(line)
                elif command_type == self.CommandType.EC2_STATES:
                    ec2_states.append(line)
        return sorted(commands), sorted(sub_commands), \
            sorted(global_options), sorted(resource_options), \
            sorted(ec2_states)
