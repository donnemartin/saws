# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import re
import sys
from collections import OrderedDict
from six.moves import cStringIO
from prompt_toolkit.completion import Completer
from .utils import TextUtils
from .commands import AwsCommands
from .resources import AwsResources


class AwsCompleter(Completer):
    """Completer for AWS commands, subcommands, options, and parameters.

    Attributes:
        * aws_completer: An instance of the official awscli Completer.
        * aws_completions: A set of completions to show the user.
        * config_obj: An instance of ConfigObj, reads from ~/.sawsrc
        * ec2_states: A list of the possible instance states.
        * text_utils: An instance of TextUtils.
        * fuzzy_match: A boolean that determines whether to use fuzzy matching.
        * shortcut_match: A boolean that determines whether to match shortcuts.
        * BASE_COMMAND: A string representing the 'aws' command.
        * DOCS_COMMAND: A string representing the 'docs' command.
        * resources: An instance of AwsResources.
        * shortcuts: An OrderedDict containing shortcuts commands as keys
            and their corresponding full commands as values.
    """

    def __init__(self,
                 aws_completer,
                 config_obj,
                 ec2_states=[],
                 fuzzy_match=False,
                 shortcut_match=False):
        """Initializes AwsCompleter.

        Args:
            * aws_completer: The official aws cli completer module.
            * config_obj: An instance of ConfigObj, reads from ~/.sawsrc
            * fuzzy_match: A boolean that determines whether to use
                fuzzy matching.
            * shortcut_match: A boolean that determines whether to
                match shortcuts.

        Returns:
            None.
        """
        self.aws_completer = aws_completer
        self.aws_completions = set()
        self.config_obj = config_obj
        self.ec2_states = ec2_states
        self.text_utils = TextUtils()
        self.fuzzy_match = fuzzy_match
        self.shortcut_match = shortcut_match
        self.BASE_COMMAND = AwsCommands.AWS_COMMAND
        self.DOCS_COMMAND = AwsCommands.AWS_DOCS
        # TODO: Refactor to use config_obj.get_shortcuts()
        self.shortcuts = OrderedDict(zip(self.config_obj['shortcuts'].keys(),
                                         self.config_obj['shortcuts'].values()))
        self.resources = \
            AwsResources(
                self.config_obj['main'].as_bool('refresh_instance_ids'),
                self.config_obj['main'].as_bool('refresh_instance_tags'),
                self.config_obj['main'].as_bool('refresh_bucket_names'))
        self.resources.refresh()

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
        for key in self.shortcuts.keys():
            if key in text:
                text = re.sub(key, self.shortcuts[key], text)
                text = self.replace_substitution(text)
                break
        return text

    def replace_substitution(self, text):
        """Replaces a `%s` with the word immediately following it.

        Currently, only one substitution is done before replacement terminates,
        although this function could potentially be extended to do multiple
        subsitutions.

        Args:
            * text: A string representing the input command text to replace.

        Returns:
            A string representing input command text with a substitution,
            if one has been found.
        """
        if '%s' in text:
            tokens = text.split()
            text = ' '.join(tokens[:-1])
            text = re.sub('%s', tokens[-1], text)
        return text

    def get_resource_completions(self, words, word_before_cursor,
                                 option_text, resource):
        """Get completions for enabled AWS resources.

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
        # Show the matching resources in the following scenarios:
        # ... --instance-ids
        # ... --instance-ids [user is now completing the instance id]
        option_text_match = (words[-1] == option_text)
        completing_res = (words[-2] == option_text and word_before_cursor != '')
        if option_text_match or completing_res:
            return self.text_utils.find_matches(word_before_cursor,
                                                resource,
                                                self.fuzzy_match)

    def get_completions(self, document, _):
        """Get completions for the current scope.

        Args:
            * document: An instance of prompt_toolkit's Document.
            * _: An instance of prompt_toolkit's CompleteEvent (not used).

        Returns:
            A generator of prompt_toolkit's Completion objects, containing
            matched completions.
        """
        # Capture the AWS CLI autocompleter and store it in a string
        old_stdout = sys.stdout
        sys.stdout = mystdout = cStringIO()
        try:
            text = self.replace_shortcut(document.text)
            self.aws_completer.complete(text, len(text))
        except Exception as e:
            print('Exception: ', e)
        sys.stdout = old_stdout
        aws_completer_results = mystdout.getvalue()
        # Tidy up the completions and store it in a list
        aws_completer_results = re.sub('\n', '', aws_completer_results)
        aws_completer_results_list = aws_completer_results.split()
        # Build the list of completions
        self.aws_completions = set()
        if len(document.text) < len(self.BASE_COMMAND):
            # Autocomplete 'aws' at the beginning of the command
            self.aws_completions.update([self.BASE_COMMAND,
                                         self.DOCS_COMMAND])
        else:
            self.aws_completions.update(aws_completer_results_list)
        self.aws_completions.update([self.DOCS_COMMAND])
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        words = self.text_utils.get_tokens(document.text)
        if len(words) == 0:
            return []
        elif len(words) == 2 and words[0] == self.BASE_COMMAND:
            # Insert shortcuts if the user typed 'aws' as the first
            # command and is inputting the subcommand
            if self.shortcut_match:
                self.aws_completions.update(self.shortcuts.keys())
        completions = None
        completions = self \
            .get_resource_completions(words,
                                      word_before_cursor,
                                      '--instance-ids',
                                      self.resources.instance_ids)
        if completions is None:
            completions = self \
                .get_resource_completions(words,
                                          word_before_cursor,
                                          '--ec2-tag-key',
                                          self.resources.instance_tag_keys)
        if completions is None:
            completions = self \
                .get_resource_completions(words,
                                          word_before_cursor,
                                          '--ec2-tag-value',
                                          self.resources.instance_tag_values)
        if completions is None:
            completions = self \
                .get_resource_completions(words,
                                          word_before_cursor,
                                          '--ec2-state',
                                          self.ec2_states)
        if completions is None:
            completions = self \
                .get_resource_completions(words,
                                          word_before_cursor,
                                          '--bucket',
                                          self.resources.bucket_names)
        if completions is None:
            completions = self \
                .text_utils.find_matches(word_before_cursor,
                                         self.aws_completions,
                                         self.fuzzy_match)
        return completions
