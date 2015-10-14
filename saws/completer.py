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
import re
import sys
import traceback
from six.moves import cStringIO
from prompt_toolkit.completion import Completer
from .utils import TextUtils
from .commands import AwsCommands
from .options import AwsOptions
from .resources import AwsResources


class AwsCompleter(Completer):
    """Completer for AWS commands, subcommands, options, and parameters.

    Attributes:
        * aws_completer: An instance of the official awscli Completer.
        * aws_completions: A set of completions to show the user.
        * all_commands: A list of all commands, sub_commands, options, etc
            from data/SOURCES.txt.
        * config: An instance of Config.
        * config_obj: An instance of ConfigObj, reads from ~/.sawsrc.
        * log_exception: A callable log_exception from SawsLogger.
        * text_utils: An instance of TextUtils.
        * fuzzy_match: A boolean that determines whether to use fuzzy matching.
        * shortcut_match: A boolean that determines whether to match shortcuts.
        * BASE_COMMAND: A string representing the 'aws' command.
        * shortcuts: An OrderedDict containing shortcuts commands as keys
            and their corresponding full commands as values.
        * resources: An instance of AwsResources.
        * options: An instance of AwsOptions
    """

    def __init__(self,
                 aws_completer,
                 all_commands,
                 config,
                 config_obj,
                 log_exception,
                 fuzzy_match=False,
                 shortcut_match=False):
        """Initializes AwsCompleter.

        Args:
            * aws_completer: The official aws cli completer module.
            * all_commands: A list of all commands, sub_commands, options, etc
                from data/SOURCES.txt.
            * config: An instance of Config.
            * config_obj: An instance of ConfigObj, reads from ~/.sawsrc.
            * log_exception: A callable log_exception from SawsLogger.
            * fuzzy_match: A boolean that determines whether to use
                fuzzy matching.
            * shortcut_match: A boolean that determines whether to
                match shortcuts.

        Returns:
            None.
        """
        self.aws_completer = aws_completer
        self.aws_completions = set()
        self.all_commands = all_commands
        self.config = config
        self.config_obj = config_obj
        self.log_exception = log_exception
        self.text_utils = TextUtils()
        self.fuzzy_match = fuzzy_match
        self.shortcut_match = shortcut_match
        self.BASE_COMMAND = AwsCommands.AWS_COMMAND
        self.shortcuts = self.config.get_shortcuts(config_obj)
        self.resources = AwsResources(self.log_exception)
        self.options = AwsOptions(self.all_commands)

    def get_completions(self, document, _):
        """Get completions for the current scope.

        Args:
            * document: An instance of prompt_toolkit's Document.
            * _: An instance of prompt_toolkit's CompleteEvent (not used).

        Returns:
            A generator of prompt_toolkit's Completion objects, containing
            matched completions.
        """
        # Get completions from the official AWS CLI
        aws_completer_results_list = self._get_aws_cli_completions(document)
        self.aws_completions = set()
        if len(document.text) < len(self.BASE_COMMAND):
            # Autocomplete 'aws' at the beginning of the command
            self.aws_completions.update([self.BASE_COMMAND])
        else:
            self.aws_completions.update(aws_completer_results_list)
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        words = self.text_utils.get_tokens(document.text)
        if len(words) == 0:
            return []
        # Determine if we should insert shortcuts
        elif len(words) == 2 and \
            words[0] == self.BASE_COMMAND and \
                word_before_cursor != '':
            # Insert shortcuts if the user typed 'aws' as the first
            # command and is inputting the subcommand
            if self.shortcut_match:
                self.aws_completions.update(self.shortcuts.keys())
        # Try to get completions for enabled AWS resources
        completions = self._get_custom_completions(
            words, word_before_cursor, self.resources.resources_options_map)
        # Try to get completions for global options, filter options, etc
        if completions is None:
            completions = self._get_custom_completions(
                words, word_before_cursor, self.options.options_map)
        # Try to get completions from the official AWS CLI
        if completions is None:
            fuzzy_aws_completions = self.fuzzy_match
            if self.fuzzy_match and word_before_cursor in \
                    self.all_commands[AwsCommands.CommandType.COMMANDS.value]:
                # Fuzzy completion currently only works with resources, options
                # and shortcuts.  If we have just completed a top-level
                # command (ie. ec2, elb, s3) then disable fuzzy completions,
                # otherwise the corresponding subcommands will be fuzzy
                # completed and incorrectly shown.
                # See: https://github.com/donnemartin/saws/issues/14
                fuzzy_aws_completions = False
            completions = self.text_utils.find_matches(word_before_cursor,
                                                       self.aws_completions,
                                                       fuzzy_aws_completions)
        return completions

    def refresh_resources_and_options(self, force_refresh=False):
        """Convenience function to refresh resources for completion.

        Args:
            * force_refresh: A boolean determines whether to force a cache
                refresh.  This value is set to True when the user presses `F5`.

        Returns:
            None.
        """
        self.resources.refresh(force_refresh)

    def replace_shortcut(self, text):
        """Replaces matched shortcut commands with their full command.

        Currently, only one shortcut is replaced before shortcut replacement
        terminates, although this function could potentially be extended
        to replace mutliple shortcuts.

        Args:
            * text: A string representing the input command text to replace.

        Returns:
            A string representing input command text with a shortcut
                replaced, if one has been found.
        """
        for key, value in self.shortcuts.items():
            if key in text:
                text = re.sub(key, value, text)
                text = self.replace_substitution(text)
                break
        return text

    def replace_substitution(self, text):
        """Replaces a `%s` with the word immediately following it.

        Currently, only one substitution is done before replacement terminates,
        although this function could potentially be extended to do multiple
        substitutions.

        Args:
            * text: A string representing the input command text to replace.

        Returns:
            A string representing input command text with a substitution,
            if one has been found.
        """
        substitution_marker = '%s'

        if substitution_marker in text:
            tokens = text.split()
            replacement_index = self.text_utils.get_token_index(
                substitution_marker, tokens) + 1
            try:
                replacement_text = tokens.pop(replacement_index)
                text = ' '.join(tokens)
                text = re.sub(substitution_marker, replacement_text, text)
            except:
                return text
        return text

    def _get_resource_completions(self, words, word_before_cursor,
                                  option_text, resource):
        """Get completions for the specified AWS resource.

        Args:
            * words: A list of words that represent the input command text.
            * word_before_cursor: A string representing the word before the
                cursor.
            * option_text: A string to match that represents the resource's
                option text, such as '--ec2-state'.  For example, if
                option_text is '--ec2-state' and it is the word before the
                cursor, then display associated resource completions found
                in the resource parameter such as pending, running, etc.
            * resource: A list that represents the resource completions to
                display if option_text is matched.  For example, instance ids,
                instance tags, etc.

        Returns:
            A generator of prompt_toolkit's Completion objects, containing
            matched completions.
        """
        if len(words) <= 1:
            return
        # Example: --bucket
        option_text_match = (words[-1] == option_text)
        # Example: --bucket prod
        completing_with_space = \
            (words[-2] == option_text and word_before_cursor != '')
        # Example: s3://prod
        completing_no_space = \
            (option_text in words[-1] and word_before_cursor != '')
        if option_text_match or completing_with_space or completing_no_space:
            return self.text_utils.find_matches(word_before_cursor,
                                                resource,
                                                self.fuzzy_match)

    def _get_aws_cli_completions(self, document):
        """Get completions from the official AWS CLI for the current scope.

        Args:
            * document: An instance of prompt_toolkit's Document.

        Returns:
            A list of string completions.
        """
        text = self.replace_shortcut(document.text)
        # Redirect stdout to a string so we can capture the AWS CLI
        # autocompleter results
        # See: http://stackoverflow.com/a/1218951
        old_stdout = sys.stdout
        sys.stdout = mystdout = cStringIO()
        try:
            self.aws_completer.complete(text, len(text))
        except Exception as e:
            self.log_exception(e, traceback)
        sys.stdout = old_stdout
        aws_completer_results = mystdout.getvalue()
        # Tidy up the completions and store it in a list
        aws_completer_results = re.sub('\n', '', aws_completer_results)
        aws_completer_results_list = aws_completer_results.split()
        return aws_completer_results_list

    def _get_custom_completions(self, words, word_before_cursor, mapping):
        """Get custom completions resources, options, etc.

        Completions for all enabled AWS resources, global options,
        filter options, etc.

        Args:
            * words: A list of strings for each word in the command text.
            * word_before_cursor: A string representing the word before
                the cursor.
            * mapping: A dict mapping of keyword triggers to completions
                Example:
                    key: --bucket,    value: list of bucket names
                    key: --ec2-state, value: list of ec2 states

        Returns:
            A generator of prompt_toolkit's Completion objects, containing
            matched completions.
        """
        completions = None
        for key, value in mapping.items():
            if completions is None:
                completions = self \
                    ._get_resource_completions(words,
                                               word_before_cursor,
                                               key,
                                               value)
            else:
                break
        return completions
