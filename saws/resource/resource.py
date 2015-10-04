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
import subprocess
from abc import ABCMeta, abstractmethod


class Resource():
    """Encapsulates an AWS resource.

    Abstract base class for resources.

    Attributes:
        * OPTION: A string representing the option that will cause the resource
            completions to be displayed when typed.
        * HEADER: A string representing the header in the RESOURCES.txt file
            that denote the start of the given resources.
        * QUERY: A string representing the AWS query to list all resources
        * resources: A list of resources.
    """

    __metaclass__ = ABCMeta

    OPTION = ''
    HEADER = ''
    QUERY = ''

    def __init__(self):
        """Initializes Resource.

        Args:
            * None.

        Returns:
            None.
        """
        self.resources = []
        self.HEADER = '[' + self.OPTION + ']'

    def clear_resources(self):
        """Clears the resource.

        Args:
            * None.

        Returns:
            None.
        """
        self.resources[:] = []

    @abstractmethod
    def query_resource(self):
        """Queries and stores resources from AWS.

        Abstract method.

        Args:
            * None.

        Raises:
            A subprocess.CalledProcessError if check_output returns a non-zero
                exit status, which is called by self._query_aws.
        """
        pass

    def _query_aws(self, query):
        """Sends the given query to the shell for processing.

        The awscli will process the command and output its results.  The
        results are captured and returned.

        Args:
            * command: A string representing the given query.

        Returns:
            A string representing the awscli output.

        Raises:
            A subprocess.CalledProcessError if check_output returns a non-zero
                exit status.
        """
        return subprocess.check_output(query,
                                       universal_newlines=True,
                                       shell=True)
