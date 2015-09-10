# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import re
import sys
from collections import OrderedDict
from six.moves import cStringIO
from prompt_toolkit.completion import Completer
from .utils import TextUtils
from .commands import AWS_COMMAND, AWS_DOCS
from .resources import AwsResources


class AwsCompleter(Completer):
    """
    Completer for AWS commands and parameters.
    """

    def __init__(self,
                 aws_completer,
                 config,
                 fuzzy_match=False,
                 shortcut_match=False,
                 refresh_instance_ids=True,
                 refresh_instance_tags=True,
                 refresh_bucket_names=True):
        """
        Initialize the completer
        :return:
        """
        self.aws_completer = aws_completer
        self.aws_completions = set()
        self.text_utils = TextUtils()
        self.fuzzy_match = fuzzy_match
        self.shortcut_match = shortcut_match
        self.BASE_COMMAND = AWS_COMMAND[0]
        self.DOCS_COMMAND = AWS_DOCS[0]
        self.resources = AwsResources(refresh_instance_ids,
                                      refresh_instance_tags,
                                      refresh_bucket_names)
        self.resources.refresh()
        # TODO: Refactor to use config.get_shortcuts()
        self.shortcuts = OrderedDict(zip(config['shortcuts'].keys(),
                                         config['shortcuts'].values()))

    def handle_shortcuts(self, text):
        for key in self.shortcuts.keys():
            if key in text:
                # Replace shortcut with full command
                text = re.sub(key, self.shortcuts[key], text)
                text = self.handle_subs(text)
        return text

    def handle_subs(self, text):
        if '%s' in text:
            tokens = text.split()
            text = ' '.join(tokens[:-1])
            text = re.sub('%s', tokens[-1], text)
        return text

    def get_resource_completions(self, words, word_before_cursor,
                                 option_text, resource):
        if words[-1] == option_text or \
            (len(words) > 1 and
                (words[-2] == option_text and word_before_cursor != '')):
            return self.text_utils.find_matches(word_before_cursor,
                                                resource,
                                                self.fuzzy_match)

    def get_completions(self, document, _):
        """
        Get completions for the current scope.
        :param document:
        :param _: complete_event
        """
        # Capture the AWS CLI autocompleter and store it in a string
        old_stdout = sys.stdout
        sys.stdout = mystdout = cStringIO()
        try:
            text = self.handle_shortcuts(document.text)
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
                                          '--bucket',
                                          self.resources.bucket_names)
        if completions is None:
            completions = self \
                .text_utils.find_matches(word_before_cursor,
                                         self.aws_completions,
                                         self.fuzzy_match)
        return completions
