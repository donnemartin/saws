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
import platform
import subprocess
import traceback
import webbrowser
from prompt_toolkit import AbortAction, Application, CommandLineInterface
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.filters import Always, HasFocus, IsDone
from prompt_toolkit.interface import AcceptAction
from prompt_toolkit.layout.processors import \
    HighlightMatchingBracketProcessor, ConditionalProcessor
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.shortcuts import create_default_layout, create_eventloop
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding.input_processor import KeyPress
from prompt_toolkit.keys import Keys
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
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
        * key_manager: An instance of KeyManager.
        * config: An instance of Config.
        * config_obj: An instance of ConfigObj, reads from ~/.sawsrc.
        * theme: A string representing the lexer theme.
        * logger: An instance of SawsLogger.
        * all_commands: A list of all commands, sub_commands, options, etc
            from data/SOURCES.txt.
        * commands: A list of commands from data/SOURCES.txt.
        * sub_commands: A list of sub_commands from data/SOURCES.txt.
        * completer: An instance of AwsCompleter.
    """

    PYGMENTS_CMD = ' | pygmentize -l json'

    def __init__(self, refresh_resources=True):
        """Inits Saws.

        Args:
            * refresh_resources: A boolean that determines whether to
                refresh resources.

        Returns:
            None.
        """
        self.aws_cli = None
        self.key_manager = None
        self.config = Config()
        self.config_obj = self.config.read_configuration()
        self.theme = self.config_obj[self.config.MAIN][self.config.THEME]
        self.logger = SawsLogger(
            __name__,
            self.config_obj[self.config.MAIN][self.config.LOG_FILE],
            self.config_obj[self.config.MAIN][self.config.LOG_LEVEL]).logger
        self.all_commands = AwsCommands().all_commands
        self.commands = \
            self.all_commands[AwsCommands.CommandType.COMMANDS.value]
        self.sub_commands = \
            self.all_commands[AwsCommands.CommandType.SUB_COMMANDS.value]
        self.completer = AwsCompleter(
            awscli_completer,
            self.all_commands,
            self.config,
            self.config_obj,
            self.log_exception,
            fuzzy_match=self.get_fuzzy_match(),
            shortcut_match=self.get_shortcut_match())
        if refresh_resources:
            self.completer.refresh_resources_and_options()
        self._create_cli()

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
        self.config_obj[self.config.MAIN][self.config.COLOR] = color

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
        return self.config_obj[self.config.MAIN].as_bool(self.config.COLOR)

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
        self.config_obj[self.config.MAIN][self.config.FUZZY] = fuzzy
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
        return self.config_obj[self.config.MAIN].as_bool(self.config.FUZZY)

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
        self.config_obj[self.config.MAIN][self.config.SHORTCUT] = shortcut
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
        return self.config_obj[self.config.MAIN].as_bool(self.config.SHORTCUT)

    def refresh_resources_and_options(self):
        """Convenience function to refresh resources and options for completion.

        Used by prompt_toolkit's KeyBindingManager.

        Args:
            * None.

        Returns:
            None.
        """
        self.completer.refresh_resources_and_options(force_refresh=True)

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

    def _handle_cd(self, text):
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

    def _colorize_output(self, text):
        """Highlights output with pygments.

        Only highlights the output if all of the following conditions are True:

        * The color option is enabled
        * The command will be handled by the `aws-cli`
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
        stripped_text = text.strip()
        if not self.get_color() or stripped_text == '':
            return text
        if AwsCommands.AWS_COMMAND not in stripped_text.split():
            return text
        excludes = [AwsCommands.AWS_CONFIGURE,
                    AwsCommands.AWS_HELP,
                    '|']
        if not any(substring in stripped_text for substring in excludes):
            return text.strip() + self.PYGMENTS_CMD
        else:
            return text

    def _handle_keyboard_interrupt(self, e, platform):
        """Handles keyboard interrupts more gracefully on Mac/Unix/Linux.

        Allows Mac/Unix/Linux to continue running on keyboard interrupt,
        as the user might interrupt a long-running AWS command with Control-C
        while continuing to work with Saws.

        On Windows, the "Terminate batch job (Y/N)" confirmation makes it
        tricky to handle this gracefully.  Thus, we re-raise KeyboardInterrupt.

        Args:
            * e: A KeyboardInterrupt.
            * platform: A string that denotes platform such as
                'Windows', 'Darwin', etc.

        Returns:
            None

        Raises:
            Exception: A KeyboardInterrupt if running on Windows.
        """
        if platform == 'Windows':
            raise e
        else:
            # Clear the renderer and send a carriage return
            self.aws_cli.renderer.clear()
            self.aws_cli.input_processor.feed_key(KeyPress(Keys.ControlM, ''))

    def _process_command(self, text):
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
        try:
            if not self._handle_cd(text):
                text = self._colorize_output(text)
                # Pass the command onto the shell so aws-cli can execute it
                subprocess.call(text, shell=True)
            print('')
        except KeyboardInterrupt as e:
            self._handle_keyboard_interrupt(e, platform.system())
        except Exception as e:
            self.log_exception(e, traceback, echo=True)

    def _create_cli(self):
        """Creates the prompt_toolkit's CommandLineInterface.

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
            auto_suggest=AutoSuggestFromHistory(),
            enable_history_search=True,
            completer=self.completer,
            complete_while_typing=Always(),
            accept_action=AcceptAction.RETURN_DOCUMENT)
        self.key_manager = KeyManager(
            self.set_color,
            self.get_color,
            self.set_fuzzy_match,
            self.get_fuzzy_match,
            self.set_shortcut_match,
            self.get_shortcut_match,
            self.refresh_resources_and_options,
            self.handle_docs)
        style_factory = StyleFactory(self.theme)
        application = Application(
            mouse_support=False,
            style=style_factory.style,
            layout=layout,
            buffer=cli_buffer,
            key_bindings_registry=self.key_manager.manager.registry,
            on_exit=AbortAction.RAISE_EXCEPTION,
            on_abort=AbortAction.RETRY,
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
        print('Theme:', self.theme)
        while True:
            document = self.aws_cli.run()
            self._process_command(document.text)
