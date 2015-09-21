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
import click
import os
import subprocess
import traceback
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
from .config import Config
from .style import StyleFactory
from .keys import KeyManager
from .toolbar import Toolbar
from .commands import AwsCommands
from .logger import SawsLogger
from .__init__ import __version__


class Saws(object):
    """Encapsulates the Saws CLI.

    Attributes:
        * aws_cli: An instance of prompt_toolkit's CommandLineInterface.
        * config: An instance of Config.
        * config_obj: An instance of ConfigObj, reads from ~/.sawsrc.
        * aws_commands: An instance of AwsCommands
        * commands: A list of commands from data/SOURCES.txt.
        * sub_commands: A list of sub_commands from data/SOURCES.txt.
        * global_options: A list of global_options from data/SOURCES.txt.
        * resource_options: A list of resource_options from data/SOURCES.txt,
            used for syntax coloring.
        * ec2_states: A list of ec2_states from data/SOURCES.txt.
        * completer: An instance of AwsCompleter.
        * key_manager: An instance of KeyManager
        * logger: An instance of SawsLogger.
        * theme: A string representing the lexer theme.
            Currently only 'vim' is supported.
    """

    def __init__(self):
        """Inits Saws.

        Args:
            * None.

        Returns:
            None.
        """
        self.aws_cli = None
        self.key_manager = None
        self.theme = 'vim'
        self.PYGMENTS_CMD = ' | pygmentize -l json'
        self.config = Config()
        self.config_obj = self.config.read_configuration()
        self.logger = SawsLogger(__name__,
                                 self.config_obj['main']['log_file'],
                                 self.config_obj['main']['log_level']).logger
        self.aws_commands = AwsCommands()
        self.commands, self.sub_commands, self.global_options, \
            self.resource_options, self.ec2_states \
            = self.aws_commands.generate_all_commands()
        self.completer = AwsCompleter(
            awscli_completer,
            self.commands,
            self.config_obj,
            self.log_exception,
            ec2_states=self.ec2_states,
            fuzzy_match=self.get_fuzzy_match(),
            shortcut_match=self.get_shortcut_match())
        self.create_cli()

    def log_exception(self, e, traceback, echo=False):
        """Logs the exception and traceback to the log file ~/.saws.log.

        Args:
            * e: A Exception that specifies the exception.
            * traceback: A Traceback that specifies the traceback.
            * echo: A boolean that specifies whether to echo the exception
                to the console using click.

        Returns:
            None.
        """
        self.logger.debug('exception: %r.', str(e))
        self.logger.error("traceback: %r", traceback.format_exc())
        if echo:
            click.secho(str(e), fg='red')

    def set_color(self, color):
        """Setter for color output mode.

        Used by prompt_toolkit's KeyBindingManager.
        KeyBindingManager expects this function to be callable so we can't use
        @property and @attrib.setter.

        Args:
            * color: A boolean that represents the color flag.

        Returns:
            None.
        """
        self.config_obj['main']['color_output'] = color

    def get_color(self):
        """Getter for color output mode.

        Used by prompt_toolkit's KeyBindingManager.
        KeyBindingManager expects this function to be callable so we can't use
        @property and @attrib.setter.

        Args:
            * None.

        Returns:
            A boolean that represents the color flag.
        """
        return self.config_obj['main'].as_bool('color_output')

    def set_fuzzy_match(self, fuzzy):
        """Setter for fuzzy matching mode

        Used by prompt_toolkit's KeyBindingManager.
        KeyBindingManager expects this function to be callable so we can't use
        @property and @attrib.setter.

        Args:
            * color: A boolean that represents the fuzzy flag.

        Returns:
            None.
        """
        self.config_obj['main']['fuzzy_match'] = fuzzy
        self.completer.fuzzy_match = fuzzy

    def get_fuzzy_match(self):
        """Getter for fuzzy matching mode

        Used by prompt_toolkit's KeyBindingManager.
        KeyBindingManager expects this function to be callable so we can't use
        @property and @attrib.setter.

        Args:
            * None.

        Returns:
            A boolean that represents the fuzzy flag.
        """
        return self.config_obj['main'].as_bool('fuzzy_match')

    def set_shortcut_match(self, shortcut):
        """Setter for shortcut matching mode

        Used by prompt_toolkit's KeyBindingManager.
        KeyBindingManager expects this function to be callable so we can't use
        @property and @attrib.setter.

        Args:
            * color: A boolean that represents the shortcut flag.

        Returns:
            None.
        """
        self.config_obj['main']['shortcut_match'] = shortcut
        self.completer.shortcut_match = shortcut

    def get_shortcut_match(self):
        """Getter for shortcut matching mode

        Used by prompt_toolkit's KeyBindingManager.
        KeyBindingManager expects this function to be callable so we can't use
        @property and @attrib.setter.

        Args:
            * None.

        Returns:
            A boolean that represents the shortcut flag.
        """
        return self.config_obj['main'].as_bool('shortcut_match')

    def refresh_resources(self):
        """Convenience function to refresh resources for completion.

        Used by prompt_toolkit's KeyBindingManager.

        Args:
            * None.

        Returns:
            None.
        """
        self.completer.refresh_resources(force_refresh=True)

    def handle_docs(self, text=None, from_fkey=False):
        """Displays contextual web docs for `F9` or the `docs` command.

        Displays the web docs specific to the currently entered:

        * (optional) command
        * (optional) subcommand

        If no command or subcommand is present, the docs index page is shown.

        Docs are only displayed if:

        * from_fkey is True
        * from_fkey is False and `docs` is found in text

        Args:
            * text: A string representing the input command text.
            * from_fkey: A boolean representing whether this function is
                being executed from an `F9` key press.

        Returns:
            A boolean representing whether the web docs were shown.
        """
        base_url = 'http://docs.aws.amazon.com/cli/latest/reference/'
        index_html = 'index.html'
        if text is None:
            text = self.aws_cli.current_buffer.document.text
        # If the user hit the F9 key, append 'docs' to the text
        if from_fkey:
            text = text.strip() + ' ' + AwsCommands.AWS_DOCS
        tokens = text.split()
        if len(tokens) > 2 and tokens[-1] == AwsCommands.AWS_DOCS:
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
        # user hit the F9 key or typed docs, just open the main docs index
        if from_fkey or AwsCommands.AWS_DOCS in tokens:
            webbrowser.open(base_url + index_html)
            return True
        return False

    def handle_cd(self, text):
        """Handles a `cd` shell command by calling python's os.chdir.

        Simply passing in the `cd` command to subprocess.call doesn't work.
        Note: Changing the directory within Saws will only be in effect while
        running Saws.  Exiting the program will return you to the directory
        you were in prior to running Saws.

        Attributes:
            * text: A string representing the input command text.

        Returns:
            A boolean representing a `cd` command was found and handled.
        """
        CD_CMD = 'cd'
        stripped_text = text.strip()
        if stripped_text.startswith(CD_CMD):
            directory = ''
            if stripped_text == CD_CMD:
                # Treat `cd` as a change to the root directory.
                # os.path.expanduser does this in a cross platform manner.
                directory = os.path.expanduser('~')
            else:
                tokens = text.split(CD_CMD + ' ')
                directory = tokens[-1]
            try:
                os.chdir(directory)
            except OSError as e:
                self.log_exception(e, traceback, echo=True)
            return True
        return False

    def colorize_output(self, text):
        """Highlights output with pygments.

        Only highlights the output if all of the following conditions are True:

        * The color option is enabled
        * The text does not contain the `configure` command
        * The text does not contain the `help` command, which already does
            output highlighting

        Args:
            * text: A string that represents the input command text.

        Returns:
            A string that represents:
                * The original command text if no highlighting was performed.
                * The pygments highlighted command text otherwise.
        """
        if not self.get_color():
            return text
        stripped_text = text.strip()
        excludes = [AwsCommands.AWS_CONFIGURE, AwsCommands.AWS_HELP]
        if not any(substring in stripped_text for substring in excludes):
            return text.strip() + self.PYGMENTS_CMD
        else:
            return text

    def process_command(self, text):
        """Processes the input command, called by the cli event loop

        Args:
            * text: A string that represents the input command text.

        Returns:
            None.
        """
        if AwsCommands.AWS_COMMAND in text:
            text = self.completer.replace_shortcut(text)
            if self.handle_docs(text):
                return
            text = self.colorize_output(text)
        try:
            if not self.handle_cd(text):
                # Pass the command onto the shell so aws-cli can execute it
                subprocess.call(text, shell=True)
            print('')
        except Exception as e:
            self.log_exception(e, traceback, echo=True)

    def create_cli(self):
        """Creates the prompt_toolkit's CommandLineInterface.

        Long description.

        Args:
            * None.

        Returns:
            None.
        """
        history = FileHistory(os.path.expanduser('~/.saws-history'))
        toolbar = Toolbar(self.get_color,
                          self.get_fuzzy_match,
                          self.get_shortcut_match)
        layout = create_default_layout(
            message='saws> ',
            reserve_space_for_menu=True,
            lexer=CommandLexer,
            get_bottom_toolbar_tokens=toolbar.handler,
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
        self.key_manager = KeyManager(
            self.set_color,
            self.get_color,
            self.set_fuzzy_match,
            self.get_fuzzy_match,
            self.set_shortcut_match,
            self.get_shortcut_match,
            self.refresh_resources,
            self.handle_docs)
        style_factory = StyleFactory(self.theme)
        application = Application(
            style=style_factory.style,
            layout=layout,
            buffer=cli_buffer,
            key_bindings_registry=self.key_manager.manager.registry,
            on_exit=AbortAction.RAISE_EXCEPTION,
            ignore_case=True)
        eventloop = create_eventloop()
        self.aws_cli = CommandLineInterface(
            application=application,
            eventloop=eventloop)

    def run_cli(self):
        """Runs the main loop.

        Args:
            * None.

        Returns:
            None.
        """
        print('Version:', __version__)
        while True:
            document = self.aws_cli.run()
            self.process_command(document.text)
