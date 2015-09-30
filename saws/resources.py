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
try:
    from collections import OrderedDict
except:
    from ordereddict import OrderedDict
import re
import subprocess
import traceback
from enum import Enum
from .commands import AwsCommands
from .data_util import DataUtil


class AwsResources(object):
    """Encapsulates AWS resources such as ec2 tags and buckets.

    Attributes:
        * instance_ids: A list of instance ids.
        * instance_tag_keys: A set of instance tag keys.
        * instance_tag_values: A set of isntance tag values.
        * bucket_names: A list of bucket names.
        * resources_map: A dict mapping of resource keywords and
            resources to complete
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
        * log_exception: A callable log_exception from SawsLogger.
    """

    INSTANCE_IDS_OPT = '--instance-ids'
    EC2_TAG_KEY_OPT = '--ec2-tag-key'
    EC2_TAG_VALUE_OPT = '--ec2-tag-value'
    BUCKET_OPT = '--bucket'
    S3_URI_OPT = 's3:'
    QUERY_INSTANCE_IDS_CMD = 'aws ec2 describe-instances --query "Reservations[].Instances[].[InstanceId]" --output text'
    QUERY_INSTANCE_TAG_KEYS_CMD = 'aws ec2 describe-instances --filters "Name=tag-key,Values=*" --query Reservations[].Instances[].Tags[].Key --output text'
    QUERY_INSTANCE_TAG_VALUES_CMD = 'aws ec2 describe-instances --filters "Name=tag-value,Values=*" --query Reservations[].Instances[].Tags[].Value --output text'
    QUERY_BUCKET_NAMES_CMD = 'aws s3 ls'

    class ResourceType(Enum):
        """Enum specifying the resource type.

        Attributes:
            * INSTANCE_IDS: An int representing instance ids.
            * INSTANCE_TAG_KEYS: An int representing instance tag keys.
            * INSTANCE_TAG_VALUES: An int representing instance tag values.
            * BUCKET_NAMES: An int representing bucket names.
        """
        NUM_TYPES = 4
        INSTANCE_IDS, INSTANCE_TAG_KEYS, INSTANCE_TAG_VALUES, \
            BUCKET_NAMES = range(NUM_TYPES)

    def __init__(self,
                 log_exception):
        """Initializes AwsResources.

        Args:
            * log_exception: A callable log_exception from SawsLogger.

        Returns:
            None.
        """
        # TODO: Use a file version instead
        self.set_resources_path('data/RESOURCES_v2.txt')
        self.instance_ids = set()
        self.instance_tag_keys = set()
        self.instance_tag_values = set()
        self.bucket_names = set()  # TODO: Make this 'private'
        self.s3_uri_names = set()  # TODO: Make this 'private'
        self.resources_map = None
        self.resource_headers = [self.INSTANCE_IDS_OPT,
                                 self.EC2_TAG_KEY_OPT,
                                 self.EC2_TAG_VALUE_OPT,
                                 self.BUCKET_OPT]
        self.data_util = DataUtil()
        self.header_to_type_map = self.data_util.create_header_to_type_map(
            headers=self.resource_headers,
            data_type=self.ResourceType)
        self.log_exception = log_exception

    def set_resources_path(self, resources_file):
        """Sets the path of where to load the resources.

        Args:
            * resources_file: A string representing the resource file
                path relative to the saws package.

        Returns:
            None.
        """
        RESOURCES_DIR = os.path.dirname(os.path.realpath(__file__))
        self.resources_path = os.path.join(RESOURCES_DIR,
                                           resources_file)

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
        self.resources_map = OrderedDict(zip([self.INSTANCE_IDS_OPT,
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
        if not force_refresh:
            try:
                self.refresh_resources_from_file()
                print('Loaded resources from cache')
            except IOError:
                print('No resource cache found')
                force_refresh = True
        if force_refresh:
            print('Refreshing resources...')
            self.query_instance_ids()
            self.query_instance_tag_keys()
            self.query_instance_tag_values()
            self.query_bucket_names()
            print('Done refreshing')
        try:
            self.create_resources_map()
            self.save_resources_to_file()
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
        print('  Refreshing instance ids...')
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
        print('  Refreshing instance tags...')
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
        print('  Refreshing bucket names...')
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
        self.bucket_names.update([bucket_name])
        self.s3_uri_names.update([self.S3_URI_OPT + '//' + bucket_name])

    def clear_bucket_names(self):
        """Clears bucket all bucket names.

        Args:
            * None.

        Returns:
            None.
        """
        self.bucket_names = set()
        self.s3_uri_names = set()

    def _get_all_resources(self):
        """Gets all resources from the data/RESOURCES.txt file.

        Args:
            * None.

        Returns:
            A list, where each element is a list of completions for each
                ResourceType
        """
        self.instance_ids = set()
        self.instance_tag_keys = set()
        self.instance_tag_values = set()
        self.clear_bucket_names()
        return DataUtil().get_data(self.resources_path,
                                   self.header_to_type_map,
                                   self.ResourceType)

    def refresh_resources_from_file(self):
        """Refreshes the AWS resources from data/RESOURCES.txt.

        Args:
            * file_path: A string representing the resource file path.

        Returns:
            None.
        """
        self.instance_ids, self.instance_tag_keys, self.instance_tag_values, \
            bucket_names, = self._get_all_resources()
        self.instance_ids = set(self.instance_ids)
        self.instance_tag_keys = set(self.instance_tag_keys)
        self.instance_tag_values = set(self.instance_tag_values)
        bucket_names = set(bucket_names)
        for bucket_name in bucket_names:
            self.add_bucket_name(bucket_name)

    def save_resources_to_file(self):
        """Saves the AWS resources to data/RESOURCES.txt.

        Args:
            * None.

        Returns:
            None.
        """
        with open(self.resources_path, 'wt') as fp:
            excludes = self.S3_URI_OPT
            for key, resources in self.resources_map.items():
                if key in excludes:
                    continue
                fp.write(key + ': ' + str(len(resources)) + '\n')
                for resource in resources:
                    fp.write(resource + '\n')
