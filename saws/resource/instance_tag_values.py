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


class InstanceTagValues(Resource):
    """Encapsulates the EC2 instance tag values resources.

    Attributes:
        * OPTION: A string representing the option for instance tag values.
        * QUERY: A string representing the AWS query to list all instance
            tag values.
        * resources: A list of instance tag values.
        * log_exception: A callable log_exception from SawsLogger.
    """

    OPTION = '--ec2-tag-value'
    QUERY = 'aws ec2 describe-instances --filters "Name=tag-value,Values=*" --query Reservations[].Instances[].Tags[].Value --output text'

    def __init__(self, log_exception):
        """Initializes InstanceTagValues.

        Args:
            * log_exception: A callable log_exception from SawsLogger.

        Returns:
            None.
        """
        self.resources = []
        self.log_exception = log_exception

    def query_resource(self):
        """Queries and stores instance ids from AWS.

        Args:
            * None.

        Returns:
            The list of resources.
        """
        print('  Refreshing instance tag values...')
        output = self._query_aws(self.QUERY)
        if output is not None:
            self.resources = set(output.split('\t'))
