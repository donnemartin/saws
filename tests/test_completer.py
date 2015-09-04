from __future__ import unicode_literals
import unittest
from mock import Mock
from prompt_toolkit.document import Document
from awscli import completer as awscli_completer
from iawscli.completer import AwsCompleter
from iawscli.commands import AWS_COMMAND, AWS_DOCS, \
    GLOBAL_OPTIONS, RESOURCE_OPTIONS


class CompleterTest(unittest.TestCase):

    def setUp(self):
        self.completer = self.create_completer()
        self.completer_event = self.create_completer_event()

    def create_completer(self):
        return AwsCompleter(awscli_completer,
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
        expected = GLOBAL_OPTIONS
        self.verify_completions(commands, expected)

    def test_resource_options(self):
        commands = ['aws ec2 describe-instances --',
                    'aws s3api get-bucket-acl --',
                    'aws elb describe-instance-health --']
        expected = RESOURCE_OPTIONS
        self.verify_completions(commands, expected)

    def test_shortcuts(self):
        commands = ['aws ec2 ls --']
        expected = ['--instance-ids']
        self.verify_completions(commands, expected)
