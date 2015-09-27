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
    """Encapsulates AWS resources such as ec2 tags and buckets.

    Attributes:
        * instance_ids: A list of instance ids.
        * instance_tag_keys: A set of instance tag keys.
        * instance_tag_values: A set of isntance tag values.
        * bucket_names: A list of bucket names.
        * resources_map: A dict mapping of resource keywords and
            resources to complete
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
        * INSTANCE_IDS_OPT: A string representing the option for instance ids
        * EC2_TAG_KEY_OPT: A string representing the option for ec2 tag keys
        * EC2_TAG_VALUE_OPT: A string representing the option for ec2 tag values
        * BUCKET_OPT: A string representing the option for buckets
        * S3_URI_OPT: A string representing the option for s3 uris
        * QUERY_INSTANCE_IDS_CMD: A string representing the AWS query to
            list all instance ids
        * QUERY_INSTANCE_TAG_KEYS_CMD: A string representing the AWS query to
            list all instance tag keys
        * QUERY_INSTANCE_TAG_VALUES_CMD: A string representing the AWS query to
            list all instance tag values
        * QUERY_BUCKET_NAMES_CMD: A string representing the AWS query to
            list all bucket names
        * config_obj: An instance of ConfigObj, reads from ~/.sawsrc.
        * log_exception: A callable log_exception from SawsLogger.
    """

    RESOURCE_FILE = 'data/RESOURCES.txt'
    INSTANCE_IDS_MARKER = '[instance ids]'
    INSTANCE_TAG_KEYS_MARKER = '[instance tag keys]'
    INSTANCE_TAG_VALUES_MARKER = '[instance tag values]'
    BUCKET_NAMES_MARKER = '[bucket names]'
    INSTANCE_IDS_OPT = '--instance-ids'
    EC2_TAG_KEY_OPT = '--ec2-tag-key'
    EC2_TAG_VALUE_OPT = '--ec2-tag-value'
    BUCKET_OPT = '--bucket'
    S3_URI_OPT = 's3:'
    QUERY_INSTANCE_IDS_CMD = 'aws ec2 describe-instances --query "Reservations[].Instances[].[InstanceId]" --output text'
    QUERY_INSTANCE_TAG_KEYS_CMD = 'aws ec2 describe-instances --filters "Name=tag-key,Values=*" --query Reservations[].Instances[].Tags[].Key --output text'
    QUERY_INSTANCE_TAG_VALUES_CMD = 'aws ec2 describe-instances --filters "Name=tag-value,Values=*" --query Reservations[].Instances[].Tags[].Value --output text'
    QUERY_BUCKET_NAMES_CMD = 'aws s3 ls'

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
                 config_obj,
                 log_exception):
        """Initializes AwsResources.

        Args:
            * config_obj: An instance of ConfigObj, reads from ~/.sawsrc.
            * log_exception: A callable log_exception from SawsLogger.

        Returns:
            None.
        """
        self.instance_ids = []
        self.instance_tag_keys = set()
        self.instance_tag_values = set()
        self.bucket_names = []  # TODO: Make this 'private'
        self.s3_uri_names = []  # TODO: Make this 'private'
        self.config_obj = config_obj
        self.refresh_instance_ids = \
            self.config_obj['main'].as_bool('refresh_instance_ids')
        self.refresh_instance_tags = \
            self.config_obj['main'].as_bool('refresh_instance_tags')
        self.refresh_bucket_names = \
            self.config_obj['main'].as_bool('refresh_bucket_names')
        self.resources_map = None
        self.log_exception = log_exception

    def create_resources_map(self):
        """Creates a mapping of resource keywords and resources to complete.

        Example:
            Key:   '--instance-ids'.
            Value: List of instance ids.

        Args:
            * None.

        Returns:
            None.
        """
        self.resources_map = dict(zip([self.INSTANCE_IDS_OPT,
                                       self.EC2_TAG_KEY_OPT,
                                       self.EC2_TAG_VALUE_OPT,
                                       self.BUCKET_OPT,
                                       self.S3_URI_OPT],
                                      [self.instance_ids,
                                       self.instance_tag_keys,
                                       self.instance_tag_values,
                                       self.bucket_names,
                                       self.s3_uri_names]))

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
        self.s3_uri_names.append(self.S3_URI_OPT + '//' + bucket_name)

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
