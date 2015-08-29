# -*- coding: utf-8
from pygments.lexer import RegexLexer
from pygments.lexer import words
from pygments.token import Operator, Keyword, Text, Name

from .options import GLOBAL_OPTIONS, RESOURCE_OPTIONS, \
    IAWS_COMMANDS, all_commands


class CommandLexer(RegexLexer):
    name = 'Command Line'
    aliases = ['cli']
    filenames = []
    commands = all_commands()

    tokens = {
        'root': [
            (words(tuple(IAWS_COMMANDS), prefix=r'', suffix=r'\b'),
             Operator.Word),
            (words(tuple(commands[0]), prefix=r'', suffix=r'\b'),
             Operator.Word),
            (words(tuple(commands[1]), prefix=r'', suffix=r'\b'),
             Operator.Word),
            (words(tuple(GLOBAL_OPTIONS), prefix=r'', suffix=r'\b'),
             Keyword),
            (words(tuple(RESOURCE_OPTIONS), prefix=r'', suffix=r'\b'),
             Keyword),
            (r'.*\n', Text),
        ]
    }
