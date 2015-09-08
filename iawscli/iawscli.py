# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import os
import click
import subprocess
import webbrowser
from prompt_toolkit import AbortAction, Application, CommandLineInterface
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.filters import Always, HasFocus, IsDone
from prompt_toolkit.layout.processors import \
    HighlightMatchingBracketProcessor, ConditionalProcessor
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.shortcuts import create_default_layout, create_eventloop
from prompt_toolkit.history import FileHistory
from awscli import completer as awscli_completer
from .completer import AwsCompleter
from .lexer import CommandLexer
from .config import read_configuration
from .style import style_factory
from .keys import get_key_manager
from .toolbar import create_toolbar_handler
from .commands import AWS_COMMAND, AWS_CONFIGURE, AWS_DOCS, AWS_HELP, \
    generate_all_commands
from .logger import create_logger
from .__init__ import __version__


click.disable_unicode_literals_warning = True


class IAwsCli(object):
    """
    The CLI implementation.
    """
    aws_cli = None
    keyword_completer = None
    saved_less_opts = None
    config = None

    def __init__(self):
        """
        Initialize class members.
        """
        self.init_config()
        self.completer = AwsCompleter(
            awscli_completer,
            self.config,
            fuzzy_match=self.get_fuzzy_match(),
            shortcut_match=self.get_shortcut_match(),
            refresh_instance_ids=self.refresh_instance_ids,
            refresh_instance_tags=self.refresh_instance_tags,
            refresh_bucket_names=self.refresh_bucket_names)
        self.commands, self.sub_commands, self.global_options, \
            self.resource_options = generate_all_commands()

    def init_config(self):
        self.config = read_configuration()
        self.log_file = self.config['main']['log_file']
        self.log_level = self.config['main']['log_level']
        self.logger = create_logger(__name__, self.log_file, self.log_level)
        self.refresh_instance_ids = \
            self.config['main'].as_bool('refresh_instance_ids')
        self.refresh_instance_tags = \
            self.config['main'].as_bool('refresh_instance_tags')
        self.refresh_bucket_names = \
            self.config['main'].as_bool('refresh_bucket_names')
        self.theme = 'vim'

    def set_color(self, is_color):
        """
        Setter for color output mode
        :param is_color: boolean
        """
        self.config['main']['color_output'] = is_color

    def get_color(self):
        """
        Getter for color output mode
        :return: boolean
        """
        return self.config['main'].as_bool('color_output')

    def set_fuzzy_match(self, is_fuzzy):
        """
        Setter for fuzzy matching mode
        :param is_fuzzy: boolean
        """
        self.config['main']['fuzzy_match'] = is_fuzzy
        self.completer.fuzzy_match = is_fuzzy

    def get_fuzzy_match(self):
        """
        Getter for fuzzy matching mode
        :return: boolean
        """
        return self.config['main'].as_bool('fuzzy_match')

    def set_shortcut_match(self, is_shortcut):
        """
        Setter for shortcut matching mode
        :param is_shortcut: boolean
        """
        self.config['main']['shortcut_match'] = is_shortcut
        self.completer.shortcut_match = is_shortcut

    def get_shortcut_match(self):
        """
        Getter for shortcut matching mode
        :return: boolean
        """
        return self.config['main'].as_bool('shortcut_match')

    def refresh_resources(self):
        self.completer.refresh_resources(force_refresh=True)

    def handle_docs(self, from_fkey=False):
        base_url = 'http://docs.aws.amazon.com/cli/latest/reference/'
        index_html = 'index.html'
        text = self.aws_cli.current_buffer.document.text
        # If the user hit the F2 key, append 'docs' to the text
        if from_fkey:
            text = text.strip() + ' ' + AWS_DOCS[0]
        tokens = text.split()
        if len(tokens) > 2 and tokens[-1] == AWS_DOCS[0]:
            prev_word = tokens[-2]
            # If we have a command, build the url
            if prev_word in self.commands:
                prev_word = prev_word + '/'
                url = base_url + prev_word + index_html
                webbrowser.open(url)
                return True
            # if we have a command and subcommand, build the url
            elif prev_word in self.sub_commands:
                command_url = tokens[-3] + '/'
                sub_command_url = tokens[-2] + '.html'
                url = base_url + command_url + sub_command_url
                webbrowser.open(url)
                return True
            webbrowser.open(base_url + index_html)
        # If we still haven't opened the help doc at this point and the
        # user hit the F2 key or typed docs, just open the main docs index
        if from_fkey or AWS_DOCS[0] in tokens:
            webbrowser.open(base_url + index_html)
            return True
        return False

    def colorize_output(self, text):
        stripped_text = text.strip()
        if stripped_text != '' and \
            stripped_text != AWS_COMMAND[0] + ' ' + AWS_CONFIGURE[0] and \
                AWS_HELP[0] not in stripped_text and \
                AWS_COMMAND[0] in stripped_text:
            return text.strip() + ' | pygmentize -l json'
        else:
            return text

    def run_cli(self):
        """
        Run the main loop
        """
        print('Version:', __version__)
        history = FileHistory(os.path.expanduser('~/.iawscli-history'))
        toolbar_handler = create_toolbar_handler(self.get_color,
                                                 self.get_fuzzy_match,
                                                 self.get_shortcut_match)
        layout = create_default_layout(
            message='iawscli> ',
            reserve_space_for_menu=True,
            lexer=CommandLexer,
            get_bottom_toolbar_tokens=toolbar_handler,
            extra_input_processors=[
                ConditionalProcessor(
                    processor=HighlightMatchingBracketProcessor(
                        chars='[](){}'),
                    filter=HasFocus(DEFAULT_BUFFER) & ~IsDone())
            ]
        )
        cli_buffer = Buffer(
            history=history,
            completer=self.completer,
            complete_while_typing=Always())
        manager = get_key_manager(
            self.set_color,
            self.get_color,
            self.set_fuzzy_match,
            self.get_fuzzy_match,
            self.set_shortcut_match,
            self.get_shortcut_match,
            self.refresh_resources,
            self.handle_docs)
        application = Application(
            style=style_factory(self.theme),
            layout=layout,
            buffer=cli_buffer,
            key_bindings_registry=manager.registry,
            on_exit=AbortAction.RAISE_EXCEPTION,
            ignore_case=True)
        eventloop = create_eventloop()
        self.aws_cli = CommandLineInterface(
            application=application,
            eventloop=eventloop)
        while True:
            document = self.aws_cli.run()
            try:
                if self.handle_docs():
                    continue
                text = self.completer.handle_shortcuts(document.text)
                if AWS_COMMAND[0] not in text:
                    print('usage: aws <command> <subcommand> [parameters] [options]')
                    continue
                if self.get_color():
                    text = self.colorize_output(text)
                # Pass the command onto the shell so aws-cli can execute it
                subprocess.call(text, shell=True)
                print('executed: ', text)
            except Exception as e:
                print(e)
