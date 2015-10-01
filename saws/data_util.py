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
import re
try:
    from collections import OrderedDict
except:
    from ordereddict import OrderedDict


class DataUtil(object):
    """Utility class to read from the data folder.

    Attributes:
        * None.
    """

    def create_header_to_type_map(self, headers, data_type):
        """Creates a dict mapping headers to ResourceTypes.

        Headers are the resource headers as they appear in the RESOURCES.txt.
        Headers are mapped to their corresponding ResourceType.

        Args:
            * headers: A string that represents the header.
            * data_type: An Enum specifying the data type.

        Returns:
            An OrderedDict mapping headers to ResourceTypes.
        """
        command_types = []
        for item in data_type:
            if item != data_type.NUM_TYPES:
                command_types.append(item)
        return OrderedDict(zip(headers, command_types))

    def get_data(self, data_file_path, header_to_type_map, data_type):
        """Gets all data from the specified data file.

        Args:
            * data_file_path: A string representing the full file path of
                the data file.
            * header_to_type_map: A dictionary mapping the data header labels
                 to the data types.
            * data_type: An Enum specifying the data type.

        Returns:
            A list, where each element is a list of completions for each
                data_type
        """
        data_lists = [[] for x in range(data_type.NUM_TYPES.value)]
        with open(data_file_path) as f:
            for line in f:
                line = re.sub('\n', '', line)
                parsing_header = False
                # Check if we are reading in a data header to determine
                # which set of data we are parsing
                for key, value in header_to_type_map.items():
                    if key in line:
                        data_type = value
                        parsing_header = True
                        break
                if not parsing_header:
                    # Store the data in its associated list
                    if line.strip() != '':
                        data_lists[data_type.value].append(line)
            for data_list in data_lists:
                data_list.sort()
        return data_lists
