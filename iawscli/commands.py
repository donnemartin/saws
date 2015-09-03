# -*- coding: utf-8
from __future__ import unicode_literals
import os
import re


# Global AWS built-in commands, listed for syntax highlighting
# TODO: Move this to SOURCES.txt
GLOBAL_OPTIONS = [
    '--debug',
    '--endpoint-url',
    '--no-verify-ssl',
    '--no-paginate',
    '--output',
    '--profile',
    '--region',
    '--version',
    '--color',
    '--query',
    '--no-sign-request',
]

# AWS built-in commands, listed for syntax highlighting
# TODO: Generate a full list of these commands and store them
# in data/SOURCES.TXT
RESOURCE_OPTIONS = [
    '--instance-ids',
    '--bucket',
    '--load-balancer-name',
]

# AWS CLI entry point, listed for syntax highlighting
AWS_COMMAND = [
    'aws',
]

# iawscli docs
AWS_DOCS = [
    'docs',
]

# iawscli shortcuts
SHORTCUTS = [
    'ls',
    '--tags',
]

# iawscli mapping of shortcuts to full commands
SHORTCUTS_MAP = {
    'aws ec2 ls': 'aws ec2 describe-instances',
    'aws dynamodb ls': 'aws dynamodb list-tables',
    'aws emr ls': 'aws emr list-clusters',
    'aws elb ls': 'aws elb describe-load-balancers',
    '--tags': '--filters "Name=tag-key,Values=%s"',
}

COMMANDS_HEADER = '[commands]: '
SUB_COMMANDS_HEADER = '[sub_commands]: '
SOURCES_DIR = os.path.dirname(os.path.realpath(__file__))
SOURCES_PATH = os.path.join(SOURCES_DIR, 'data/SOURCES.txt')


def generate_all_commands():
    commands = []
    sub_commands = []
    parsing_sub_commands = False
    with open(SOURCES_PATH) as f:
        for line in f:
            line = re.sub('\n', '', line)
            if COMMANDS_HEADER in line:
                continue
            if SUB_COMMANDS_HEADER in line:
                parsing_sub_commands = True
                continue
            if not parsing_sub_commands:
                commands.append(line)
            else:
                sub_commands.append(line)
    return sorted(list(commands)), sorted(list(sub_commands))
