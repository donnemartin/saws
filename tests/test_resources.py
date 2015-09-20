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
import sys
import mock
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
from saws.saws import Saws


class ResourcesTest(unittest.TestCase):

    NUM_INSTANCE_IDS = 7
    NUM_INSTANCE_TAG_KEYS = 3
    NUM_INSTANCE_TAG_VALUES = 6
    NUM_BUCKET_NAMES = 16
    RESOURCES = 'data/RESOURCES.txt'
    RESOURCES_SAMPLE = 'data/RESOURCES_SAMPLE.txt'

    def setUp(self):
        self.create_resources()

    @mock.patch('saws.resources.print')
    def create_resources(self, mock_print):
        self.saws = Saws()
        self.resources = self.saws.completer.resources
        self.resources.RESOURCE_FILE = self.RESOURCES_SAMPLE
        mock_print.assert_called_with('Loaded resources from cache')

    @mock.patch('saws.resources.print')
    def test_refresh(self, mock_print):
        self.resources.refresh(force_refresh=False)
        assert len(self.resources.instance_ids) == \
            self.NUM_INSTANCE_IDS
        assert len(self.resources.instance_tag_keys) == \
            self.NUM_INSTANCE_TAG_KEYS
        assert len(self.resources.instance_tag_values) == \
            self.NUM_INSTANCE_TAG_VALUES
        assert len(self.resources.bucket_names) == \
            self.NUM_BUCKET_NAMES
        assert len(self.resources.s3_uri_names) == \
            self.NUM_BUCKET_NAMES
        mock_print.assert_called_with('Loaded resources from cache')

    @mock.patch('saws.resources.subprocess')
    @mock.patch('saws.resources.print')
    def test_refresh_forced(self, mock_print, mock_subprocess):
        self.resources.RESOURCE_FILE = self.RESOURCES
        with self.assertRaises(TypeError):
            try:
                self.resources.refresh(force_refresh=True)
            except TypeError as e:
                # The subprocess mock will cause this function to
                # throw an exception.  Check the mock worked as
                # expected before satisfying assertRaises.
                mock_subprocess.check_output.assert_called_with(
                    self.resources.QUERY_INSTANCE_IDS_CMD,
                    universal_newlines=True,
                    shell=True)
                mock_print.assert_called_with('  Refreshing instance ids...')
                raise e
        self.resources.RESOURCE_FILE = self.RESOURCES_SAMPLE

    @mock.patch('saws.resources.subprocess')
    def test_query_aws_with_instance_ids(self, mock_subprocess):
        self.resources.query_aws(self.resources.QUERY_INSTANCE_IDS_CMD)
        mock_subprocess.check_output.assert_called_with(
            self.resources.QUERY_INSTANCE_IDS_CMD,
            universal_newlines=True,
            shell=True)

    @mock.patch('saws.resources.subprocess')
    def test_query_aws_with_instance_tag_keys(self, mock_subprocess):
        self.resources.query_aws(self.resources.QUERY_INSTANCE_TAG_KEYS_CMD)
        mock_subprocess.check_output.assert_called_with(
            self.resources.QUERY_INSTANCE_TAG_KEYS_CMD,
            universal_newlines=True,
            shell=True)

    @mock.patch('saws.resources.subprocess')
    def query_aws_with_instance_tag_values(self, mock_subprocess):
        self.resources.query_aws(self.resources.QUERY_INSTANCE_TAG_VALUES_CMD)
        mock_subprocess.check_output.assert_called_with(
            self.resources.QUERY_INSTANCE_TAG_VALUES_CMD,
            universal_newlines=True,
            shell=True)

    @mock.patch('saws.resources.subprocess')
    def test_query_aws_with_bucket_names(self, mock_subprocess):
        self.resources.query_aws(self.resources.QUERY_BUCKET_NAMES_CMD)
        mock_subprocess.check_output.assert_called_with(
            self.resources.QUERY_BUCKET_NAMES_CMD,
            universal_newlines=True,
            shell=True)

    def test_add_and_clear_bucket_name(self):
        BUCKET_NAME = 'test_bucket_name'
        self.resources.clear_bucket_names()
        self.resources.add_bucket_name(BUCKET_NAME)
        assert BUCKET_NAME in self.resources.bucket_names
        assert str(self.resources.S3_URI + '//' + BUCKET_NAME) in \
            self.resources.s3_uri_names
        self.resources.clear_bucket_names()
        assert len(self.resources.bucket_names) == 0
        assert len(self.resources.s3_uri_names) == 0
