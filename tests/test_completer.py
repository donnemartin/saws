# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import unittest
from mock import Mock
from prompt_toolkit.document import Document
from awscli import completer as awscli_completer
from saws.completer import AwsCompleter
from saws.commands import AWS_COMMAND, AWS_DOCS
from saws.main import Saws


class CompleterTest(unittest.TestCase):

    def setUp(self):
        self.iaws_cli = Saws()
        self.completer = self.create_completer()
        self.completer_event = self.create_completer_event()

    def create_completer(self):
        return AwsCompleter(awscli_completer,
                            self.iaws_cli.config,
                            refresh_instance_ids=False,
                            refresh_instance_tags=False,
                            refresh_bucket_names=False)

    def create_completer_event(self):
        return Mock()

    def _get_completions(self, command):
        position = len(command)
        result = set(self.completer.get_completions(
            Document(text=command, cursor_position=position),
            self.completer_event))
        return result

    def verify_completions(self, commands, expected):
        result = set()
        for command in commands:
            # Call the AWS CLI autocompleter
            result.update(self._get_completions(command))
        result_texts = []
        for item in result:
            # Each result item is a Completion object,
            # we are only interested in the text portion
            result_texts.append(item.text)
        assert result_texts
        if len(expected) == 1:
            assert expected[0] in result_texts
        else:
            for item in expected:
                assert item in result_texts

    def test_aws_command_completion(self):
        commands = ['a', 'aw']
        expected = AWS_COMMAND
        self.verify_completions(commands, expected)

    def test_docs_command_completion(self):
        commands = ['d', 'do', 'doc']
        expected = AWS_DOCS
        self.verify_completions(commands, expected)

    def test_global_options(self):
        commands = ['aws -', 'aws --']
        expected = self.iaws_cli.global_options
        self.verify_completions(commands, expected)

    def test_resource_options(self):
        commands = ['aws ec2 describe-instances --',
                    'aws s3api get-bucket-acl --',
                    'aws elb describe-instance-health --']
        expected = self.iaws_cli.resource_options
        self.verify_completions(commands, expected)

    def test_shortcuts(self):
        commands = ['aws ec2 ls --']
        expected = ['--instance-ids']
        self.verify_completions(commands, expected)

    def test_instance_ids(self):
        commands = ['aws ec2 ls --instance-ids i-a']
        expected = ['i-a875ecc3', 'i-a51d05f4', 'i-a3628153']
        self.completer.resources.instance_ids.extend(expected)
        self.verify_completions(commands, expected)

    def test_instance_tags(self):
        commands = ['aws ec2 ls --ec2-tags prod']
        expected = ['production', 'production-blue', 'production-green']
        self.completer.resources.instance_tags.update(expected)
        self.verify_completions(commands, expected)

    def test_bucket_names(self):
        commands = ['aws s3pi get-bucket-acl --bucket web-']
        expected = ['web-server-logs', 'web-server-images']
        self.completer.resources.bucket_names.extend(expected)
        self.verify_completions(commands, expected)

    def test_fuzzy_matching(self):
        commands = ['aws ec2 ls --instance-ids a5']
        expected = ['i-a875ecc3', 'i-a41d55f4', 'i-a3628153']
        self.completer.fuzzy_match = True
        self.completer.resources.instance_ids.extend(expected)
        self.verify_completions(commands, expected)

    def test_substitutions(self):
        command = 'aws ec2 ls --filters "Name=tag-key,Values=%s prod"'
        expected = 'aws ec2 ls --filters "Name=tag-key,Values=prod"'
        result = self.completer.handle_subs(command)
        assert result == expected
