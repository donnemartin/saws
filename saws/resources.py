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
import os
import re
import subprocess
import traceback
from enum import Enum
from .commands import AwsCommands


class AwsResources(object):
    """Loads and stores AWS resources.

    Attributes:
        * instance_ids: A list of instance ids.
        * instance_tag_keys: A set of instance tag keys.
        * instance_tag_values: A set of isntance tag values.
        * bucket_names: A list of bucket names.
        * refresh_instance_ids: A boolean that determines whether to
            refresh instance ids by querying AWS.
        * refresh_instance_tags: A boolean that determines whether to
            refresh instance tags by querying AWS.
        * refresh_bucket_names: A boolean that determines whether to
            refresh bucket names by querying AWS.
        * INSTANCE_IDS_MARKER: A string marking the start of
            instance ids in data/RESOURCES.txt.
        * INSTANCE_TAG_KEYS_MARKER: A string marking the start of
            instance tag keys in data/RESOURCES.txt.
        * INSTANCE_TAG_VALUES_MARKER: A string marking the start of
            instance tag values in data/RESOURCES.txt.
        * BUCKET_NAMES_MARKER: A string marking the start of i
            bucket names in data/RESOURCES.txt.
        QUERY_INSTANCE_IDS_CMD: A string representing the AWS query to
            list all instance ids
        QUERY_INSTANCE_TAG_KEYS_CMD: A string representing the AWS query to
            list all instance tag keys
        QUERY_INSTANCE_TAG_VALUES_CMD: A string representing the AWS query to
            list all instance tag values
        QUERY_BUCKET_NAMES_CMD: A string representing the AWS query to
            list all bucket names
        * log_exception: A callable log_exception from SawsLogger.
    """

    class ResType(Enum):
        """Enum specifying the resource type.

        Attributes:
            * INSTANCE_IDS: An int representing instance ids.
            * INSTANCE_TAG_KEYS: An int representing instance tag keys.
            * INSTANCE_TAG_VALUES: An int representing instance tag values.
            * BUCKET_NAMES: An int representing bucket names.
        """

        INSTANCE_IDS, INSTANCE_TAG_KEYS, INSTANCE_TAG_VALUES, \
            BUCKET_NAMES = range(4)

    def __init__(self,
                 log_exception,
                 refresh_instance_ids=True,
                 refresh_instance_tags=True,
                 refresh_bucket_names=True):
        """Initializes AwsResources.

        Args:
            * log_exception: A callable log_exception from SawsLogger.
            * refresh_instance_ids: A boolean that determines whether to
                refresh instance ids by querying AWS.
            * refresh_instance_tags: A boolean that determines whether to
                refresh instance tags by querying AWS.
            * refresh_bucket_names: A boolean that determines whether to
                refresh bucket names by querying AWS.

        Returns:
            None.
        """
        self.RESOURCE_FILE = 'data/RESOURCES.txt'
        self.instance_ids = []
        self.instance_tag_keys = set()
        self.instance_tag_values = set()
        self.bucket_names = []  # TODO: Make this 'private'
        self.s3_uri_names = []  # TODO: Make this 'private'
        self.refresh_instance_ids = refresh_instance_ids
        self.refresh_instance_tags = refresh_instance_tags
        self.refresh_bucket_names = refresh_bucket_names
        self.INSTANCE_IDS_MARKER = '[instance ids]'
        self.INSTANCE_TAG_KEYS_MARKER = '[instance tag keys]'
        self.INSTANCE_TAG_VALUES_MARKER = '[instance tag values]'
        self.BUCKET_NAMES_MARKER = '[bucket names]'
        self.INSTANCE_IDS = '--instance-ids'
        self.EC2_TAG_KEY = '--ec2-tag-key'
        self.EC2_TAG_VALUE = '--ec2-tag-value'
        self.EC2_STATE = '--ec2-state'
        self.BUCKET = '--bucket'
        self.S3_URI = 's3:'
        self.QUERY_INSTANCE_IDS_CMD = 'aws ec2 describe-instances --query "Reservations[].Instances[].[InstanceId]" --output text'
        self.QUERY_INSTANCE_TAG_KEYS_CMD = 'aws ec2 describe-instances --filters "Name=tag-key,Values=*" --query Reservations[].Instances[].Tags[].Key --output text'
        self.QUERY_INSTANCE_TAG_VALUES_CMD = 'aws ec2 describe-instances --filters "Name=tag-value,Values=*" --query Reservations[].Instances[].Tags[].Value --output text'
        self.QUERY_BUCKET_NAMES_CMD = 'aws s3 ls'
        self.log_exception = log_exception

    def refresh(self, force_refresh=False):
        """Refreshes the AWS resources and caches them to a file.

        This function is called on startup.
        If no cache exists, it queries AWS to build the resource lists.
        Pressing the `F5` key will set force_refresh to True, which proceeds
        to refresh the list regardless of whether a cache exists.
        Before returning, it saves the resource lists to cache.

        Args:
            * force_refresh: A boolean determines whether to force a cache
                refresh.  This value is set to True when the user presses `F5`.

        Returns:
            None.
        """
        file_path = os.path.join(AwsCommands.SOURCES_DIR,
                                 self.RESOURCE_FILE)
        if not force_refresh:
            try:
                self.refresh_resources_from_file(file_path)
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
                self.query_instance_tag_keys()
                self.query_instance_tag_values()
            if self.refresh_bucket_names:
                print('  Refreshing bucket names...')
                self.query_bucket_names()
            print('Done refreshing')
        try:
            self.save_resources_to_file(file_path)
        except IOError as e:
            self.log_exception(e, traceback)

    def query_aws(self, command):
        try:
            return subprocess.check_output(command,
                                           universal_newlines=True,
                                           shell=True)
        except Exception as e:
            self.log_exception(e, traceback)

    def query_instance_ids(self):
        """Queries and stores instance ids from AWS.

        Args:
            * None.

        Returns:
            None.
        """
        output = self.query_aws(self.QUERY_INSTANCE_IDS_CMD)
        if output is not None:
            output = re.sub('\n', ' ', output)
            self.instance_ids = output.split()

    def query_instance_tag_keys(self):
        """Queries and stores instance tag keys from AWS.

        Args:
            * None.

        Returns:
            None.
        """
        output = self.query_aws(self.QUERY_INSTANCE_TAG_KEYS_CMD)
        if output is not None:
            self.instance_tag_keys = set(output.split('\t'))

    def query_instance_tag_values(self):
        """Queries and stores instance tag values from AWS.

        Args:
            * None

        Returns:
            None.
        """
        output = self.query_aws(self.QUERY_INSTANCE_TAG_VALUES_CMD)
        if output is not None:
            self.instance_tag_values = set(output.split('\t'))

    def query_bucket_names(self):
        """Queries and stores bucket names from AWS.

        Args:
            * None

        Returns:
            None
        """
        output = self.query_aws(self.QUERY_BUCKET_NAMES_CMD)
        if output is not None:
            self.clear_bucket_names()
            result_list = output.split('\n')
            for result in result_list:
                try:
                    result = result.split()[-1]
                    self.add_bucket_name(result)
                except:
                    # Ignore blank lines
                    pass

    def add_bucket_name(self, bucket_name):
        """Adds the bucket name to our bucket resources.

        Args:
            * bucket_name: A string representing the bucket name.

        Returns:
            None.
        """
        self.bucket_names.append(bucket_name)
        self.s3_uri_names.append(self.S3_URI + '//' + bucket_name)

    def clear_bucket_names(self):
        """Clears bucket all bucket names.

        Long description.

        Args:
            * None.

        Returns:
            None.
        """
        self.bucket_names = []
        self.s3_uri_names = []

    def refresh_resources_from_file(self, file_path):
        """Refreshes the AWS resources from data/RESOURCES.txt.

        Args:
            * file_path: A string representing the resource file path.

        Returns:
            None.
        """
        res_type = self.ResType.INSTANCE_IDS
        with open(file_path) as fp:
            self.instance_ids = []
            self.instance_tag_keys = set()
            self.instance_tag_values = set()
            self.clear_bucket_names()
            instance_tag_keys_list = []
            instance_tag_values_list = []
            for line in fp:
                line = re.sub('\n', '', line)
                if line.strip() == '':
                    continue
                elif self.INSTANCE_IDS_MARKER in line:
                    res_type = self.ResType.INSTANCE_IDS
                    continue
                elif self.INSTANCE_TAG_KEYS_MARKER in line:
                    res_type = self.ResType.INSTANCE_TAG_KEYS
                    continue
                elif self.INSTANCE_TAG_VALUES_MARKER in line:
                    res_type = self.ResType.INSTANCE_TAG_VALUES
                    continue
                elif self.BUCKET_NAMES_MARKER in line:
                    res_type = self.ResType.BUCKET_NAMES
                    continue
                if res_type == self.ResType.INSTANCE_IDS:
                    self.instance_ids.append(line)
                elif res_type == self.ResType.INSTANCE_TAG_KEYS:
                    instance_tag_keys_list.append(line)
                elif res_type == self.ResType.INSTANCE_TAG_VALUES:
                    instance_tag_values_list.append(line)
                elif res_type == self.ResType.BUCKET_NAMES:
                    self.add_bucket_name(line)
            self.instance_tag_keys = set(instance_tag_keys_list)
            self.instance_tag_values = set(instance_tag_values_list)

    def save_resources_to_file(self, file_path):
        """Saves the AWS resources to data/RESOURCES.txt.

        Args:
            * file_path: A string representing the resource file path.

        Returns:
            None.
        """
        with open(file_path, 'wt') as fp:
            fp.write(self.INSTANCE_IDS_MARKER + '\n')
            for instance_id in self.instance_ids:
                fp.write(instance_id + '\n')
            fp.write(self.INSTANCE_TAG_KEYS_MARKER + '\n')
            for instance_tag_key in self.instance_tag_keys:
                fp.write(instance_tag_key + '\n')
            fp.write(self.INSTANCE_TAG_VALUES_MARKER + '\n')
            for instance_tag_value in self.instance_tag_values:
                fp.write(instance_tag_value + '\n')
            fp.write(self.BUCKET_NAMES_MARKER + '\n')
            for bucket_name in self.bucket_names:
                fp.write(bucket_name + '\n')
