from __future__ import unicode_literals
import os
import subprocess
import pexpect
from six import string_types
from iawscli.completion import Completer, Completion
from iawscli.shortcuts import get_input
from iawscli.history import FileHistory
from iawscli.contrib.completers import AwsCliCompleter
from iawscli.application import AbortAction
from pygments.lexers import SqlLexer
from pygments.token import Token
from iawscli.aws_styles import AwsStyle
from awscli import clidriver
from awscli import completer as aws_completer


def cli():
    keys = []
    history = FileHistory(os.path.expanduser('~/.iawscli-history'))
    aws_driver = clidriver.create_clidriver()
    aws_cli_completer = AwsCliCompleter(keys,
                                        aws_driver,
                                        aws_completer,
                                        ignore_case=True)
    while True:
        try:
            text = get_input('> ',
                             completer=aws_cli_completer,
                             aws_driver=aws_driver,
                             style=AwsStyle,
                             history=history,
                             on_abort=AbortAction.RETRY,
                             patch_stdout=True)
        except EOFError:
            # Control-D pressed.
            break
        try:
            # Pass the command onto the shell so aws-cli can execute it
            process = pexpect.spawnu(text)
            process.interact()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    cli()