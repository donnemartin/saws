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
import mock
from tests.compat import unittest
from saws.saws import Saws


class ResourcesTest(unittest.TestCase):

    NUM_SAMPLE_INSTANCE_IDS = 7
    NUM_SAMPLE_INSTANCE_TAG_KEYS = 3
    NUM_SAMPLE_INSTANCE_TAG_VALUES = 6
    NUM_SAMPLE_BUCKET_NAMES = 16
    NUM_SAMPLE_BUCKET_URIS = 16

    def setUp(self):
        self.create_resources()
        self.sample_resource_counts = [
            self.NUM_SAMPLE_INSTANCE_IDS,
            self.NUM_SAMPLE_INSTANCE_TAG_KEYS,
            self.NUM_SAMPLE_INSTANCE_TAG_VALUES,
            self.NUM_SAMPLE_BUCKET_NAMES,
            self.NUM_SAMPLE_BUCKET_URIS
        ]

    def create_resources(self):
        self.saws = Saws(refresh_resources=False)
        self.resources = self.saws.completer.resources
        self.resources._set_resources_path('data/RESOURCES_SAMPLE.txt')

    def verify_resources(self):
        for resource_list, sample_resource_count in zip(
                self.resources.resource_lists,
                self.sample_resource_counts):
            assert len(resource_list.resources) == sample_resource_count

    # TODO: Silence output
    @mock.patch('saws.resources.print')
    def test_refresh_forced(self, mock_print):
        self.resources._set_resources_path('data/RESOURCES_FORCED.txt')
        self.resources.clear_resources()
        self.resources.refresh(force_refresh=True)
        mock_print.assert_called_with('Done refreshing')

    # TODO: Silence output
    @mock.patch('saws.resources.print')
    def test_refresh(self, mock_print):
        self.resources.refresh(force_refresh=False)
        self.verify_resources()
        mock_print.assert_called_with('Loaded resources from cache')

    # TODO: Fix mocks
    @unittest.skip('')
    @mock.patch('saws.resources.subprocess')
    def test_query_aws_instance_ids(self, mock_subprocess):
        instance_ids = self.resources.resource_lists[
            self.resources.ResourceType.INSTANCE_IDS.value]
        instance_ids._query_aws(instance_ids.QUERY)
        mock_subprocess.check_output.assert_called_with(
            instance_ids.QUERY,
            universal_newlines=True,
            shell=True)

    # TODO: Fix mocks
    @unittest.skip('')
    @mock.patch('saws.resources.subprocess')
    def test_query_aws_instance_tag_keys(self, mock_subprocess):
        instance_tag_keys = self.resources.resource_lists[
            self.resources.ResourceType.INSTANCE_TAG_KEYS.value]
        instance_tag_keys._query_aws(instance_tag_keys.QUERY)
        mock_subprocess.check_output.assert_called_with(
            instance_tag_keys.QUERY,
            universal_newlines=True,
            shell=True)

    # TODO: Fix mocks
    # @unittest.skip('')
    @mock.patch('saws.resources.subprocess')
    def query_aws_instance_tag_values(self, mock_subprocess):
        instance_tag_values = self.resources.resource_lists[
            self.resources.ResourceType.INSTANCE_TAG_VALUES.value]
        instance_tag_values._query_aws(instance_tag_values.QUERY)
        mock_subprocess.check_output.assert_called_with(
            instance_tag_values.QUERY,
            universal_newlines=True,
            shell=True)

    # TODO: Fix mocks
    @unittest.skip('')
    @mock.patch('saws.resources.subprocess')
    def test_query_aws_bucket_names(self, mock_subprocess):
        bucket_names = self.resources.resource_lists[
            self.resources.ResourceType.BUCKET_NAMES.value]
        bucket_names._query_aws(bucket_names.QUERY)
        mock_subprocess.check_output.assert_called_with(
            bucket_names.QUERY,
            universal_newlines=True,
            shell=True)

    def test_add_and_clear_bucket_name(self):
        BUCKET_NAME = 'test_bucket_name'
        bucket_names = self.resources.resource_lists[
            self.resources.ResourceType.BUCKET_NAMES.value]
        bucket_uris = self.resources.resource_lists[
            self.resources.ResourceType.BUCKET_URIS.value]
        bucket_names.clear_resources()
        bucket_names.add_bucket_name(BUCKET_NAME)
        assert BUCKET_NAME in bucket_names.resources
        bucket_uris.add_bucket_name(BUCKET_NAME)
        BUCKET_URI = bucket_uris.PREFIX + BUCKET_NAME
        assert BUCKET_URI in bucket_uris.resources
        bucket_names.clear_resources()
        bucket_uris.clear_resources()
        assert len(bucket_names.resources) == 0
        assert len(bucket_uris.resources) == 0
