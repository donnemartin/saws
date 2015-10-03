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
import traceback
from enum import Enum
from .data_util import DataUtil
from .resource.instance_ids import InstanceIds
from .resource.instance_tag_keys import InstanceTagKeys
from .resource.instance_tag_values import InstanceTagValues
from .resource.bucket_names import BucketNames
from .resource.bucket_uris import BucketUris


class AwsResources(object):
    """Encapsulates AWS resources such as ec2 tags and buckets.

    Attributes:
        * resources_path: A string representing the full file path of
            data/RESOURCES.txt.
        * log_exception: A callable log_exception from SawsLogger.
        * resource_lists: A list where each element is a list of completions
            for each resource.
        * resources_headers_map: A dict mapping resource headers to
            resources to complete.  Headers denote the start of each
            set of resources in the RESOURCES.txt file.
        * resources_options_map: A dict mapping resource options to
            resources to complete.
        * resource_headers: A list of headers that denote the start of each
            set of resources in the RESOURCES.txt file.
        * data_util: An instance of DataUtil().
        * header_to_type_map: A dict mapping headers as they appear in the
            RESOURCES.txt file to their corresponding ResourceType.
    """

    class ResourceType(Enum):
        """Enum specifying the resource type.

        Append new resource class instances here and increment NUM_TYPES.
        Note: Order is important, new resources should be added to the end.

        Attributes:
            * INSTANCE_IDS: An int representing instance ids.
            * INSTANCE_TAG_KEYS: An int representing instance tag keys.
            * INSTANCE_TAG_VALUES: An int representing instance tag values.
            * BUCKET_NAMES: An int representing bucket names.
            * BUCKET_URIS: An int representing bucket uris.
            * NUM_TYPES: An int representing the number of resource types.
        """
        NUM_TYPES = 5
        INSTANCE_IDS, INSTANCE_TAG_KEYS, INSTANCE_TAG_VALUES, \
            BUCKET_NAMES, BUCKET_URIS = range(NUM_TYPES)

    def __init__(self,
                 log_exception):
        """Initializes AwsResources.

        Args:
            * log_exception: A callable log_exception from SawsLogger.

        Returns:
            None.
        """
        # TODO: Use a file version instead of a new file
        self._set_resources_path('data/RESOURCES_v2.txt')
        self.log_exception = log_exception
        self.resource_lists = self._create_resource_lists()
        self.resources_headers_map = None
        self.resources_options_map = None
        self.resource_headers = self._get_resource_headers()
        self.resource_options = self._get_resource_options()
        self.data_util = DataUtil()
        self.header_to_type_map = self.data_util.create_header_to_type_map(
            headers=self.resource_headers,
            data_type=self.ResourceType)

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
        self.clear_resources()
        if not force_refresh:
            try:
                self._refresh_resources_from_file()
                print('Loaded resources from cache')
            except IOError:
                print('No resource cache found')
                force_refresh = True
        if force_refresh:
            self._query_resources()
        try:
            self.resources_headers_map = self._create_resources_map(
                self.resource_headers)
            self.resources_options_map = self._create_resources_map(
                self.resource_options)
            self._save_resources_to_file()
        except IOError as e:
            self.log_exception(e, traceback)

    def clear_resources(self):
        """Clears all resources.

        Args:
            * None.

        Returns:
            None.
        """
        for resource_list in self.resource_lists:
            resource_list.clear_resources()

    def _create_resource_lists(self):
        """Create the resource lists.

        Append new resource class instances here.
        Note: Order is important, new resources should be added to the end.

        Args:
            * None.

        Returns:
            None.
        """
        return [InstanceIds(),
                InstanceTagKeys(),
                InstanceTagValues(),
                BucketNames(),
                BucketUris()]

    def _get_resource_headers(self):
        """Builds a list of resource headers found in the resource file.

        Each header denotes the start of each set of resources in the
        RESOURCES.txt file

        Args:
            * None.

        Returns:
            A list of headers that denote the start of each set of resources
                in the RESOURCES.txt file.
        """
        resource_headers = []
        for resource_list in self.resource_lists:
            resource_headers.append(resource_list.HEADER)
        return resource_headers

    def _get_resource_options(self):
        """Builds a list of resource options that kick off option completions.

        Args:
            * None.

        Returns:
            A list of options that kick off option completions.
        """
        resource_options = []
        for resource_list in self.resource_lists:
            resource_options.append(resource_list.OPTION)
        return resource_options

    def _create_resources_map(self, resource_key):
        """Creates a mapping of resource keywords and resources to complete.

        Requires self.resource_headers to already contain all headers.

        Example with resource_key == resource_headers:
            Key:   '[--instance-ids]'.
            Value: List of instance ids.

        Example with resource_key == resource_options:
            Key:   '--instance-ids'.
            Value: List of instance ids.

        Args:
            * resource_key: One of the two attributes:
                resource_headers or resource_options.

        Returns:
            An OrderedDict resource keywords and resources to complete.
        """
        resources = []
        for resource_list in self.resource_lists:
            resources.append(resource_list.resources)
        resources_map = OrderedDict(zip(resource_key, resources))
        return resources_map

    def _query_resources(self):
        """Runs queries for all resources.

        Args:
            * None.

        Returns:
            None.
        """
        print('Refreshing resources...')
        for resource_list in self.resource_lists:
            try:
                resource_list.query_resource()
            except Exception as e:
                self.log_exception(e, traceback)
        print('Done refreshing')

    def _get_all_resources(self):
        """Gets all resources from the data/RESOURCES.txt file.

        Args:
            * None.

        Returns:
            A list, where each element is a list of completions for each
                ResourceType
        """
        return DataUtil().get_data(self.resources_path,
                                   self.header_to_type_map,
                                   self.ResourceType)

    def _set_resources_path(self, resources_file):
        """Sets the path of where to load the resources.

        Args:
            * resources_file: A string representing the resource file
                path relative to the saws package.

        Returns:
            None.
        """
        RESOURCES_DIR = os.path.dirname(os.path.realpath(__file__))
        self.resources_path = os.path.join(RESOURCES_DIR, resources_file)

    def _refresh_resources_from_file(self):
        """Refreshes the AWS resources from data/RESOURCES.txt.

        Args:
            * file_path: A string representing the resource file path.

        Returns:
            None.
        """
        all_resources = self._get_all_resources()
        for index, resources in enumerate(all_resources):
            self.resource_lists[index].resources = resources

    def _save_resources_to_file(self):
        """Saves the AWS resources to data/RESOURCES.txt.

        Args:
            * None.

        Returns:
            None.
        """
        with open(self.resources_path, 'wt') as fp:
            for key, resources in self.resources_headers_map.items():
                fp.write(key + ': ' + str(len(resources)) + '\n')
                for resource in resources:
                    fp.write(resource + '\n')
