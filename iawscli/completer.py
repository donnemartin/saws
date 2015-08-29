# -*- coding: utf-8
from __future__ import unicode_literals

import sys
import re
import os
import fuzzyfinder
import subprocess

from cStringIO import StringIO
from itertools import chain
from prompt_toolkit.completion import Completer, Completion
from .utils import shlex_split, shlex_first_token


class AwsCompleter(Completer):
    """
    Completer for AWS commands and parameters.
    """

    def __init__(self, aws_completer, fuzzy_match=False,
                 refresh_instance_ids=True, refresh_bucket_names=True):
        """
        Initialize the completer
        :return:
        """
        self.aws_completer = aws_completer
        self.aws_completions = set()
        self.fuzzy_match = fuzzy_match
        self.commands = []
        self.sub_commands = []
        self.instance_ids = []
        self.bucket_names = []
        self.refresh_instance_ids = refresh_instance_ids
        self.refresh_bucket_names = refresh_bucket_names
        self.BASE_COMMAND = 'aws'

        self.generate_commands()
        self.refresh_resources()

    def refresh_resources(self):
        """
        Refreshes the AWS resources
        :return: None
        """
        print('Refreshing resources...')
        if self.refresh_instance_ids:
            print('  Refreshing instance ids...')
            self.generate_instance_ids()
        if self.refresh_bucket_names:
            print('  Refreshing bucket names...')
            self.generate_bucket_names()
        print('Done refreshing')

    def generate_commands(self):
        p = os.path.dirname(os.path.realpath(__file__))
        f = os.path.join(p, 'data/SOURCES.txt')
        COMMANDS_INDEX = 2
        SUB_COMMANDS_INDEX = 3
        with open(f) as fp:
            for line in fp:
                if 'awscli/examples/' in line:
                    line = re.sub('.rst\n', '', line)
                    tokens = line.split('/')
                    self.commands.append(tokens[COMMANDS_INDEX])
                    self.sub_commands.append(tokens[SUB_COMMANDS_INDEX])

    def generate_instance_ids(self):
        command = "aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId]' --output text"
        try:
            result = subprocess.check_output([command], shell=True)
            result = re.sub('\n', ' ', result)
            self.instance_ids = result.split()
        except Exception as e:
            print(e)

    def generate_bucket_names(self):
        command = "aws s3 ls"
        try:
            output = subprocess.check_output([command], shell=True)
            result_list = output.split('\n')
            for result in result_list:
                try:
                    result = result.split()[-1]
                    self.bucket_names.append(result)
                except:
                    pass
        except Exception as e:
            print(e)

    def get_completions(self, document, _):
        """
        Get completions for the current scope.
        :param document:
        :param _: complete_event
        """

        # Capture the AWS CLI autocompleter and store it in a string
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        try:
            self.aws_completer.complete(document.text, len(document.text))
        except Exception as ex:
            pass
        sys.stdout = old_stdout
        completions = mystdout.getvalue()

        # Tidy up the completions and store it in a list
        completions = re.sub('\n', '', completions)
        completions_list = completions.split()

        # Build the list of completions
        self.aws_completions = set()
        if len(document.text) < len(self.BASE_COMMAND):
            # Autocomplete 'aws' at the beginning of the command
            self.aws_completions = [self.BASE_COMMAND]
        else:
            self.aws_completions.update(completions_list)

        word_before_cursor = document.get_word_before_cursor(WORD=True)
        first_word = AwsCompleter.first_token(document.text).lower()
        words = AwsCompleter.get_tokens(document.text)

        if len(words) == 0:
            return []

        if words[-1] == '--instance-ids' or \
            (len(words) > 1 and (words[-2] == '--instance-ids' and word_before_cursor != '')):
            completions = AwsCompleter.find_matches(
                word_before_cursor,
                self.instance_ids,
                self.fuzzy_match)
        elif words[-1] == '--bucket' or \
            (len(words) > 1 and (words[-2] == '--bucket' and word_before_cursor != '')):
            completions = AwsCompleter.find_matches(
                word_before_cursor,
                self.bucket_names,
                self.fuzzy_match)
        else:
            completions = AwsCompleter.find_matches(
                word_before_cursor,
                self.aws_completions,
                self.fuzzy_match)

        return completions

    @staticmethod
    def find_collection_matches(word, lst, fuzzy):
        """
        Yield all matching names in list
        :param lst: collection
        :param word: string user typed
        :param fuzzy: boolean
        :return: iterable
        """

        if fuzzy:
            for suggestion in fuzzyfinder.fuzzyfinder(word, lst):
                yield Completion(suggestion, -len(word))
        else:
            for name in sorted(lst):
                if name.startswith(word) or not word:
                    yield Completion(name, -len(word))

    @staticmethod
    def find_matches(text, collection, fuzzy):
        """
        Find all matches for the current text
        :param text: text before cursor
        :param collection: collection to suggest from
        :param fuzzy: boolean
        :return: iterable
        """
        text = AwsCompleter.last_token(text).lower()

        for suggestion in AwsCompleter.find_collection_matches(
                text, collection, fuzzy):
            yield suggestion

    @staticmethod
    def get_tokens(text):
        """
        Parse out all tokens.
        :param text:
        :return: list
        """
        if text is not None:
            text = text.strip()
            words = AwsCompleter.safe_split(text)
            return words
        return []

    @staticmethod
    def first_token(text):
        """
        Find first word in a sentence
        :param text:
        :return:
        """
        if text is not None:
            text = text.strip()
            if len(text) > 0:
                try:
                    word = shlex_first_token(text)
                    word = word.strip()
                    return word
                except:
                    # no error, just do not complete
                    pass
        return ''

    @staticmethod
    def last_token(text):
        """
        Find last word in a sentence
        :param text:
        :return:
        """
        if text is not None:
            text = text.strip()
            if len(text) > 0:
                word = AwsCompleter.safe_split(text)[-1]
                word = word.strip()
                return word
        return ''

    @staticmethod
    def safe_split(text):
        """
        Shlex can't always split. For example, "\" crashes the completer.
        """
        try:
            words = shlex_split(text)
            return words
        except:
            return text
