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
from .bucket import Bucket


class BucketNames(Bucket):
    """Encapsulates the S3 bucket names resources.

    Attributes:
        * OPTION: A string representing the option for bucket names.
        * QUERY: A string representing the AWS query to list all bucket names.
        * resources: A list of bucket names.
    """

    OPTION = '--bucket'
    QUERY = 'aws s3 ls'

    def __init__(self):
        """Initializes BucketNames.

        Args:
            * None.

        Returns:
            None.
        """
        super(BucketNames, self).__init__()

    def query_resource(self):
        """Queries and stores bucket names from AWS.

        Args:
            * None.

        Returns:
            None.

        Raises:
            A subprocess.CalledProcessError if check_output returns a non-zero
                exit status, which is called by self._query_aws.
        """
        print('  Refreshing bucket names...')
        super(BucketNames, self).query_resource()

    def add_bucket_name(self, bucket_name):
        """Adds the bucket name to our bucket resources.

        Args:
            * bucket_name: A string representing the bucket name.

        Returns:
            None.
        """
        self.resources.extend([bucket_name])
