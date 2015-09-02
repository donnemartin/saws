# -*- coding: utf-8
from pygments.lexer import RegexLexer
from pygments.lexer import words
from pygments.token import Keyword, Name, Operator, Generic, Literal
from .commands import GLOBAL_OPTIONS, RESOURCE_OPTIONS, \
    AWS_COMMAND, AWS_DOCS, SHORTCUTS, generate_all_commands


class CommandLexer(RegexLexer):
    commands = generate_all_commands()
    tokens = {
        'root': [
            (words(tuple(AWS_COMMAND), prefix=r'', suffix=r'\b'),
             Literal.String),
            (words(tuple(commands[0]), prefix=r'', suffix=r'\b'),
             Name.Class),
            (words(tuple(commands[1]), prefix=r'', suffix=r'\b'),
             Keyword.Declaration),
            (words(tuple(SHORTCUTS), prefix=r'', suffix=r'\b'),
             Keyword.Declaration),
            (words(tuple(GLOBAL_OPTIONS), prefix=r'', suffix=r'\b'),
             Generic.Output),
            (words(tuple(RESOURCE_OPTIONS), prefix=r'', suffix=r'\b'),
             Operator.Word),
            (words(tuple(AWS_DOCS), prefix=r'', suffix=r'\b'),
             Literal.Number),
        ]
    }
