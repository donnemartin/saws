# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
import mock
from saws.saws import Saws


class ResourcesTest(unittest.TestCase):

    def setUp(self):
        self.create_resources()
        self.NUM_INSTANCE_IDS = 7
        self.NUM_INSTANCE_TAG_KEYS = 3
        self.NUM_INSTANCE_TAG_VALUES = 6
        self.NUM_BUCKET_NAMES = 16

    def create_resources(self):
        self.saws = Saws()
        self.resources = self.saws.completer.resources
        self.resources.RESOURCE_FILE = 'data/RESOURCES_SAMPLE.txt'

    def test_refresh(self):
        self.resources.refresh(force_refresh=False)
        assert len(self.resources.instance_ids) == \
            self.NUM_INSTANCE_IDS
        assert len(self.resources.instance_tag_keys) == \
            self.NUM_INSTANCE_TAG_KEYS
        assert len(self.resources.instance_tag_values) == \
            self.NUM_INSTANCE_TAG_VALUES
        assert len(self.resources.bucket_names) == \
            self.NUM_BUCKET_NAMES

    @unittest.skip('TODO: Does not properly test a force refresh')
    def test_refresh_forced(self):
        self.resources.refresh(force_refresh=True)
        assert len(self.resources.instance_ids) == \
            self.NUM_INSTANCE_IDS
        assert len(self.resources.instance_tag_keys) == \
            self.NUM_INSTANCE_TAG_KEYS
        assert len(self.resources.instance_tag_values) == \
            self.NUM_INSTANCE_TAG_VALUES
        assert len(self.resources.bucket_names) == \
            self.NUM_BUCKET_NAMES

    @mock.patch('saws.resources.subprocess')
    def test_query_instance_ids(self, mock_subprocess):
        self.resources.query_instance_ids()
        mock_subprocess.check_output.assert_called_with(
            self.resources.QUERY_INSTANCE_IDS_CMD,
            universal_newlines=True,
            shell=True)

    @mock.patch('saws.resources.subprocess')
    def test_query_instance_tag_keys(self, mock_subprocess):
        self.resources.query_instance_tag_keys()
        mock_subprocess.check_output.assert_called_with(
            self.resources.QUERY_INSTANCE_TAG_KEYS_CMD,
            universal_newlines=True,
            shell=True)

    @mock.patch('saws.resources.subprocess')
    def query_instance_tag_values(self, mock_subprocess):
        self.resources.query_instance_tag_values()
        mock_subprocess.check_output.assert_called_with(
            self.resources.QUERY_INSTANCE_TAG_VALUES_CMD,
            universal_newlines=True,
            shell=True)

    @mock.patch('saws.resources.subprocess')
    def test_query_bucket_names(self, mock_subprocess):
        self.resources.query_bucket_names()
        mock_subprocess.check_output.assert_called_with(
            self.resources.QUERY_BUCKET_NAMES_CMD,
            universal_newlines=True,
            shell=True)
