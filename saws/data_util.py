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


class DataUtil(object):
    """Utility class to read from the data folder.

    Attributes:
        * None.
    """

    def get_data(self, data_file_path, header_to_type_map,
                 data_type, data_lists):
        """Gets all data from the specified data file.

        Args:
            * data_file_path: A xxx that does xxx.
            * header_to_type_map: A dictionary mapping the data header labels
                 to the data types.
            * data_type: A xxx that does xxx.
                This must be initialized to the first data type encountered
                when reading the data file.
            * data_lists: A list of lists.  Each list element contains
                completions for each data type.

        Returns:
            A list, where each element is a list of completions for each
                data_type
        """
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
