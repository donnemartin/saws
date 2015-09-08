# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import os
import re
from enum import Enum


# AWS CLI entry point, listed for syntax highlighting
AWS_COMMAND = [
    'aws',
]

# AWS CLI configure command, listed for syntax highlighting
AWS_CONFIGURE = [
    'configure'
]

AWS_HELP = [
    'help',
]

# iawscli docs
AWS_DOCS = [
    'docs',
]

COMMANDS_HEADER = '[commands]: '
SUB_COMMANDS_HEADER = '[sub_commands]: '
GLOBAL_OPTIONS_HEADER = '[global_options]: '
RESOURCE_OPTIONS_HEADER = '[resource_options]: '
SOURCES_DIR = os.path.dirname(os.path.realpath(__file__))
SOURCES_PATH = os.path.join(SOURCES_DIR, 'data/SOURCES.txt')


class CommandType(Enum):

    COMMANDS, SUB_COMMANDS, GLOBAL_OPTIONS, RESOURCE_OPTIONS = range(4)


def generate_all_commands():
    commands = []
    sub_commands = []
    global_options = []
    resource_options = []
    command_type = CommandType.COMMANDS
    with open(SOURCES_PATH) as f:
        for line in f:
            line = re.sub('\n', '', line)
            if COMMANDS_HEADER in line:
                command_type = CommandType.COMMANDS
                continue
            elif SUB_COMMANDS_HEADER in line:
                command_type = CommandType.SUB_COMMANDS
                continue
            elif GLOBAL_OPTIONS_HEADER in line:
                command_type = CommandType.GLOBAL_OPTIONS
                continue
            elif RESOURCE_OPTIONS_HEADER in line:
                command_type = CommandType.RESOURCE_OPTIONS
                continue
            if command_type == CommandType.COMMANDS:
                commands.append(line)
            elif command_type == CommandType.SUB_COMMANDS:
                sub_commands.append(line)
            elif command_type == CommandType.GLOBAL_OPTIONS:
                global_options.append(line)
            elif command_type == CommandType.RESOURCE_OPTIONS:
                resource_options.append(line)
    return sorted(commands), sorted(sub_commands), \
        sorted(global_options), sorted(resource_options)
