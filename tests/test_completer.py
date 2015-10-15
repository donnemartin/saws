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
import unittest
import mock
import re
from prompt_toolkit.document import Document
from awscli import completer as awscli_completer
from saws.completer import AwsCompleter
from saws.commands import AwsCommands
from saws.saws import Saws


class CompleterTest(unittest.TestCase):

    @mock.patch('saws.resources.print')
    def setUp(self, mock_print):
        self.saws = Saws(refresh_resources=False)
        self.completer = self.create_completer()
        self.completer.resources._set_resources_path(
            'data/RESOURCES_SAMPLE.txt')
        self.completer.refresh_resources_and_options()
        self.completer_event = self.create_completer_event()
        mock_print.assert_called_with('Loaded resources from cache')

    def create_completer(self):
        # TODO: Fix duplicate creation of AwsCompleter, which is already
        # created by Saws init
        self.aws_commands = AwsCommands()
        self.all_commands = self.aws_commands.all_commands
        self.commands, self.sub_commands, self.global_options, \
            self.resource_options = self.all_commands
        return AwsCompleter(awscli_completer,
                            self.all_commands,
                            self.saws.config,
                            self.saws.config_obj,
                            self.saws.logger)

    def create_completer_event(self):
        return mock.Mock()

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

    def test_no_completions(self):
        command = 'aws ec2'
        expected = set([])
        assert expected == self._get_completions(command)
        command = 'aws elb'
        assert expected == self._get_completions(command)
        command = 'aws elasticache'
        assert expected == self._get_completions(command)

    def test_ec2_commands(self):
        commands = ['aws e']
        expected = ['ec2',
                    'ecs',
                    'efs',
                    'elasticache',
                    'elasticbeanstalk',
                    'elastictranscoder',
                    'elb',
                    'emr']
        self.verify_completions(commands, expected)

    def test_ec2_subcommands(self):
        commands = ['aws ec2 c']
        expected = ['cancel-bundle-task',
                    'cancel-conversion-task',
                    'cancel-export-task',
                    'cancel-import-task',
                    'cancel-reserved-instances-listing',
                    'cancel-spot-fleet-requests',
                    'cancel-spot-instance-requests']
        self.verify_completions(commands, expected)

    def test_aws_command(self):
        commands = ['a', 'aw']
        expected = [AwsCommands.AWS_COMMAND]
        self.verify_completions(commands, expected)

    def test_global_options(self):
        commands = ['aws -', 'aws --']
        expected = self.saws \
            .all_commands[AwsCommands.CommandType.GLOBAL_OPTIONS.value]
        self.verify_completions(commands, expected)

    def test_resource_options(self):
        commands = ['aws ec2 describe-instances --',
                    'aws s3api get-bucket-acl --',
                    'aws emr list-clusters --']
        expected = self.saws \
            .all_commands[AwsCommands.CommandType.RESOURCE_OPTIONS.value]
        self.verify_completions(commands, expected)

    def test_shortcuts(self):
        commands = ['aws ec2 ls',
                    'aws emr ls',
                    'aws elb ls',
                    'aws dynamodb ls']
        expected = ['aws ec2 describe-instances',
                    'aws emr list-clusters',
                    'aws elb describe-load-balancers',
                    'aws dynamodb list-tables']
        shortcuts = dict(zip(commands, expected))
        for command, expect in shortcuts.items():
            result = self.completer.replace_shortcut(command)
            assert result == expect

    def test_shortcuts_fuzzy(self):
        self.completer.fuzzy_match = True
        self.completer.shortcut_match = True
        commands = ['aws ec2ls']
        expected = ['ec2 ls --instance-ids']
        self.verify_completions(commands, expected)
        commands = ['aws ec2start']
        expected = ['ec2 start-instances --instance-ids']
        self.verify_completions(commands, expected)
        commands = ['aws ec2stop']
        expected = ['ec2 stop-instances --instance-ids']
        self.verify_completions(commands, expected)
        commands = ['aws ec2tagk']
        expected = ['ec2 ls --ec2-tag-key']
        self.verify_completions(commands, expected)
        commands = ['aws ec2tagv']
        expected = ['ec2 ls --ec2-tag-value']
        self.verify_completions(commands, expected)

    def test_substitutions(self):
        command = 'aws ec2 ls --filters "Name=tag-key,Values=%s prod"'
        expected = 'aws ec2 ls --filters "Name=tag-key,Values=prod"'
        result = self.completer.replace_substitution(command)
        assert result == expected
        command = 'aws ec2 ls --ec2-tag-key Stack'
        expected = \
            'aws ec2 describe-instances --filters "Name=tag-key,Values=Stack"'
        result = self.completer.replace_shortcut(command)
        assert result == expected
        command = 'aws ec2 ls --ec2-tag-value prod'
        expected = \
            'aws ec2 describe-instances --filters "Name=tag-value,Values=prod"'
        result = self.completer.replace_shortcut(command)
        assert result == expected

    def test_substitutions_with_more_tokens(self):
        command = 'aws ec2 ls --filters "Name=tag-key,Values=%s prod" ' \
                  '| grep IpAddress'
        expected = 'aws ec2 ls --filters "Name=tag-key,Values=prod" ' \
                   '| grep IpAddress'
        result = self.completer.replace_substitution(command)
        assert result == expected
        command = 'aws ec2 ls --ec2-tag-key Stack | grep IpAddress'
        expected = 'aws ec2 describe-instances --filters ' \
                   '"Name=tag-key,Values=Stack" | grep IpAddress'
        result = self.completer.replace_shortcut(command)
        assert result == expected
        command = 'aws ec2 ls --ec2-tag-value prod | grep IpAddress'
        expected = 'aws ec2 describe-instances --filters ' \
                   '"Name=tag-value,Values=prod" | grep IpAddress'
        result = self.completer.replace_shortcut(command)
        assert result == expected

    @mock.patch('saws.resources.print')
    def test_refresh_resources_and_options(self, mock_print):
        self.completer.refresh_resources_and_options(force_refresh=False)
        mock_print.assert_called_with('Loaded resources from cache')

    def test_instance_ids(self):
        commands = ['aws ec2 ls --instance-ids i-b']
        expected = ['i-b875ecc3', 'i-b51d05f4', 'i-b3628153']
        instance_ids = self.completer.resources.resource_lists[
            self.completer.resources.ResourceType.INSTANCE_IDS.value]
        instance_ids.resources.extend(expected)
        self.verify_completions(commands, expected)
        commands = ['aws ec2 ls --instance-ids i-a']
        expected = ['i-a51d05f4', 'i-a71bd617', 'i-a1637b56']
        instance_ids.resources.extend(expected)
        self.verify_completions(commands, expected)

    def test_instance_ids_fuzzy(self):
        self.completer.fuzzy_match = True
        commands = ['aws ec2 ls --instance-ids a5']
        expected = ['i-a875ecc3', 'i-a41d55f4', 'i-a3628153']
        instance_ids = self.completer.resources.resource_lists[
            self.completer.resources.ResourceType.INSTANCE_IDS.value]
        instance_ids.resources.extend(expected)
        self.verify_completions(commands, expected)

    def test_instance_keys(self):
        commands = ['aws ec2 ls --ec2-tag-key na']
        expected = ['name', 'namE']
        instance_tag_keys = self.completer.resources.resource_lists[
            self.completer.resources.ResourceType.INSTANCE_TAG_KEYS.value]
        instance_tag_keys.resources.extend(expected)
        self.verify_completions(commands, expected)
        commands = ['aws ec2 ls --ec2-tag-key Sta']
        expected = ['Stack']
        instance_tag_keys.resources.extend(expected)
        self.verify_completions(commands, expected)

    def test_instance_tag_values(self):
        commands = ['aws ec2 ls --ec2-tag-value prod']
        expected = ['production', 'production-blue', 'production-green']
        instance_tag_values = self.completer.resources.resource_lists[
            self.completer.resources.ResourceType.INSTANCE_TAG_VALUES.value]
        instance_tag_values.resources.extend(expected)
        self.verify_completions(commands, expected)
        commands = ['aws ec2 ls --ec2-tag-value test']
        expected = ['testing']
        instance_tag_values.resources.extend(expected)
        self.verify_completions(commands, expected)

    def test_bucket_names(self):
        commands = ['aws s3pi get-bucket-acl --bucket web-']
        expected = ['web-server-logs', 'web-server-images']
        bucket_names = self.completer.resources.resource_lists[
            self.completer.resources.ResourceType.BUCKET_NAMES.value]
        for bucket_name in expected:
            bucket_names.add_bucket_name(bucket_name)
        self.verify_completions(commands, expected)

    def test_s3_uri(self):
        commands = ['aws s3 ls s3:']
        expected = ['s3://web-server-logs', 's3://web-server-images']
        bucket_uris = self.completer.resources.resource_lists[
            self.completer.resources.ResourceType.BUCKET_URIS.value]
        for s3_uri in expected:
            bucket_name = re.sub('s3://', '', s3_uri)
            bucket_uris.add_bucket_name(bucket_name)
        self.verify_completions(commands, expected)
        commands = ['aws s3 ls s3://web']
        self.verify_completions(commands, expected)

    def test_ec2_states(self):
        commands = ['aws ec2 ls --ec2-state pend']
        expected = ['pending']
        self.verify_completions(commands, expected)
        commands = ['aws ec2 ls --ec2-state run']
        expected = ['running']
        self.verify_completions(commands, expected)
        commands = ['aws ec2 ls --ec2-state shut']
        expected = ['shutting-down']
        self.verify_completions(commands, expected)
        commands = ['aws ec2 ls --ec2-state term']
        expected = ['terminated']
        self.verify_completions(commands, expected)
        commands = ['aws ec2 ls --ec2-state stop']
        expected = ['stopping',
                    'stopped']
        self.verify_completions(commands, expected)

    def test_cluster_states(self):
        self.verify_cluster_states()

    def test_cluster_states_fuzzy(self):
        self.completer.fuzzy_match = True
        self.verify_cluster_states()

    def verify_cluster_states(self):
        commands = ['aws emr ls --cluster-states star']
        expected = ['STARTING']
        self.verify_completions(commands, expected)
        commands = ['emr ls --cluster-states BOOT']
        expected = ['BOOTSTRAPPING']
        self.verify_completions(commands, expected)
        commands = ['emr ls --cluster-states run']
        expected = ['RUNNING']
        self.verify_completions(commands, expected)
        commands = ['emr ls --cluster-states WAIT']
        expected = ['WAITING']
        self.verify_completions(commands, expected)
        commands = ['emr ls --cluster-states term']
        expected = ['TERMINATING',
                    'TERMINATED',
                    'TERMINATED_WITH_ERRORS']
        self.verify_completions(commands, expected)
