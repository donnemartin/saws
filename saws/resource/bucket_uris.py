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
from .resource import Resource


class BucketUris(Resource):
    """Encapsulates the S3 bucket uri resources.

    Attributes:
        * OPTION: A string representing the option for bucket uri.
        * QUERY: A string representing the AWS query to list all bucket uri.
        * resources: A list of bucket uri.
        * log_exception: A callable log_exception from SawsLogger.
    """

    OPTION = 's3:'
    QUERY = 'aws s3 ls'
    PREFIX = OPTION + '//'

    def __init__(self, log_exception):
        """Initializes BucketNames.

        Args:
            * log_exception: A callable log_exception from SawsLogger.

        Returns:
            None.
        """
        self.resources = []
        self.log_exception = log_exception

    def query_resource(self):
        """Queries and stores bucket uris from AWS.

        Special case for S3:
            We have two ways to invoke S3 completions:
                Option: --bucket  Completion: foo
                Option: s3:       Completion: s3://foo
        BucketName.query_resource will load the bucket names for both options.

        Args:
            * None.

        Returns:
            None.
        """
        output = []

    def add_bucket_name(self, bucket_name):
        """Adds the bucket name to our bucket resources.

        Args:
            * bucket_name: A string representing the bucket name.

        Returns:
            None.
        """
        self.resources.extend([self.PREFIX + bucket_name])
