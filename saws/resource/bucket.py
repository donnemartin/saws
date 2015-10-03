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
from .resource import Resource
from abc import ABCMeta, abstractmethod


class Bucket(Resource):
    """Encapsulates the S3 bucket resources.

    Base class for BucketNames and BucketUris

    Attributes:
        * OPTION: A string representing the option for bucket uri.
        * QUERY: A string representing the AWS query to list all bucket uri.
        * resources: A list of bucket uri.
    """

    __metaclass__ = ABCMeta

    OPTION = ''
    QUERY = ''

    def __init__(self):
        """Initializes BucketNames.

        Args:
            * None.

        Returns:
            None.
        """
        super(Bucket, self).__init__()

    def query_resource(self):
        """Queries and stores bucket names from AWS.

        Special case for S3:
            We have two ways to invoke S3 completions:
                Option: --bucket  Completion: foo
                Option: s3:       Completion: s3://foo

        Args:
            * None.

        Returns:
            None.

        Raises:
            A subprocess.CalledProcessError if check_output returns a non-zero
                exit status, which is called by self._query_aws.
        """
        output = self._query_aws(self.QUERY)
        if output is not None:
            self.clear_resources()
            result_list = output.split('\n')
            for result in result_list:
                try:
                    result = result.split()[-1]
                    self.add_bucket_name(result)
                except:
                    # Ignore blank lines
                    pass

    @abstractmethod
    def add_bucket_name(self, bucket_name):
        """Adds the bucket name to our bucket resources.

        Abstract method.

        Args:
            * bucket_name: A string representing the bucket name.

        Returns:
            None.
        """
        pass
