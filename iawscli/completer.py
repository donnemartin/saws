# -*- coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function
from enum import Enum
import sys
import re
import os
import subprocess
from collections import OrderedDict
from six.moves import cStringIO
from prompt_toolkit.completion import Completer
from .utils import TextUtils
from .commands import AWS_COMMAND, AWS_DOCS, SOURCES_DIR


class AwsCompleter(Completer):
    """
    Completer for AWS commands and parameters.
    """

    def __init__(self, aws_completer,
                 config, fuzzy_match=False,
                 shortcut_match=False, refresh_instance_ids=True,
                 refresh_instance_tags=True, refresh_bucket_names=True):
        """
        Initialize the completer
        :return:
        """
        self.aws_completer = aws_completer
        self.aws_completions = set()
        self.text_utils = TextUtils()
        self.fuzzy_match = fuzzy_match
        self.shortcut_match = shortcut_match
        self.instance_ids = []
        self.instance_tags = set()
        self.bucket_names = []
        self.refresh_instance_ids = refresh_instance_ids
        self.refresh_instance_tags = refresh_instance_tags
        self.refresh_bucket_names = refresh_bucket_names
        self.BASE_COMMAND = AWS_COMMAND[0]
        self.DOCS_COMMAND = AWS_DOCS[0]
        self.instance_ids_marker = '[instance ids]'
        self.instance_tags_marker = '[instance tags]'
        self.bucket_names_marker = '[bucket names]'
        self.refresh_resources()
        # TODO: Refactor to use config.get_shortcuts()
        self.shortcuts = OrderedDict(zip(config['shortcuts'].keys(),
                                         config['shortcuts'].values()))

    def refresh_resources_from_file(self, f, p):
        class ResType(Enum):

            INSTANCE_IDS, INSTANCE_TAGS, BUCKET_NAMES = range(3)

        res_type = ResType.INSTANCE_IDS
        with open(f) as fp:
            self.instance_ids = []
            self.instance_tags = set()
            self.bucket_names = []
            instance_tags_list = []
            for line in fp:
                line = re.sub('\n', '', line)
                if line.strip() == '':
                    continue
                elif self.instance_ids_marker in line:
                    res_type = ResType.INSTANCE_IDS
                    continue
                elif self.instance_tags_marker in line:
                    res_type = ResType.INSTANCE_TAGS
                    continue
                elif self.bucket_names_marker in line:
                    res_type = ResType.BUCKET_NAMES
                    continue
                if res_type == ResType.INSTANCE_IDS:
                    self.instance_ids.append(line)
                elif res_type == ResType.INSTANCE_TAGS:
                    instance_tags_list.append(line)
                elif res_type == ResType.BUCKET_NAMES:
                    self.bucket_names.append(line)
            self.instance_tags = set(instance_tags_list)

    def save_resources_to_file(self, f, p):
        with open(f, 'w') as fp:
            fp.write(self.instance_ids_marker + '\n')
            for instance_id in self.instance_ids:
                fp.write(instance_id + '\n')
            fp.write(self.instance_tags_marker + '\n')
            for instance_tag in self.instance_tags:
                fp.write(instance_tag + '\n')
            fp.write(self.bucket_names_marker + '\n')
            for bucket_name in self.bucket_names:
                fp.write(bucket_name + '\n')

    def refresh_resources(self, force_refresh=False):
        """
        Refreshes the AWS resources
        :return: None
        """
        p = SOURCES_DIR
        f = os.path.join(p, 'data/RESOURCES.txt')
        if not force_refresh:
            try:
                self.refresh_resources_from_file(f, p)
                print('Loaded resources from cache')
            except IOError:
                print('No resource cache found')
                force_refresh = True
        if force_refresh:
            print('Refreshing resources...')
            if self.refresh_instance_ids:
                print('  Refreshing instance ids...')
                self.query_instance_ids()
            if self.refresh_instance_tags:
                print('  Refreshing instance tags...')
                self.query_instance_tags()
            if self.refresh_bucket_names:
                print('  Refreshing bucket names...')
                self.query_bucket_names()
            print('Done refreshing')
        try:
            self.save_resources_to_file(f, p)
        except IOError as e:
            print(e)

    def query_instance_ids(self):
        command = 'aws ec2 describe-instances --query "Reservations[].Instances[].[InstanceId]" --output text'
        try:
            result = subprocess.check_output(command, shell=True)
            result = re.sub('\n', ' ', result)
            self.instance_ids = result.split()
        except Exception as e:
            print(e)

    def query_instance_tags(self):
        command = 'aws ec2 describe-instances --filters "Name=tag-key,Values=*" --query Reservations[].Instances[].Tags[].Key --output text'
        try:
            result = subprocess.check_output(command, shell=True)
            self.instance_tags = set(result.split('\t'))
        except Exception as e:
            print(e)

    def query_bucket_names(self):
        command = 'aws s3 ls'
        try:
            output = subprocess.check_output(command, shell=True)
            result_list = output.split('\n')
            for result in result_list:
                try:
                    result = result.split()[-1]
                    self.bucket_names.append(result)
                except:
                    # Ignore blank lines
                    pass
        except Exception as e:
            print(e)

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
        completions = self.get_resource_completions(words,
                                                    word_before_cursor,
                                                    '--instance-ids',
                                                    self.instance_ids)
        if completions is None:
            completions = self.get_resource_completions(words,
                                                        word_before_cursor,
                                                        '--ec2-tags',
                                                        self.instance_tags)
        if completions is None:
            completions = self.get_resource_completions(words,
                                                        word_before_cursor,
                                                        '--bucket',
                                                        self.bucket_names)
        if completions is None:
            completions = self.text_utils.find_matches(word_before_cursor,
                                                       self.aws_completions,
                                                       self.fuzzy_match)
        return completions
