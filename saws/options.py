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
from .commands import AwsCommands


class AwsOptions(object):
    """Encapsulates AWS command options such as ec2 running states.

    Attributes:
        * all_commands: A list of all commands, sub_commands, options, etc
            from data/SOURCES.txt.
        * EC2_STATE_OPT: A string representing the option for ec2 states
        * ec2_states: A list of the possible EC2 instance states.
        * options_map: A dict mapping of options keywords and
            options to complete
        * log_exception: A callable log_exception from SawsLogger.
    """

    def __init__(self,
                 all_commands,
                 log_exception):
        """Initializes AwsResources.

        Args:
            * all_commands: A list of all commands, sub_commands, options, etc
                from data/SOURCES.txt.
            * log_exception: A callable log_exception from SawsLogger.

        Returns:
            None.
        """
        self.all_commands = all_commands
        self.EC2_STATE_OPT = '--ec2-state'
        self.ec2_states = \
            self.all_commands[AwsCommands.CommandType.EC2_STATES.value]
        self.options_map = None
        self.log_exception = log_exception

    def create_options_map(self):
        """Creates a mapping of option keywords and options to complete.

        Example:
            Key:   '--ec2-state'.
            Value: A list of the possible instance states.

        Args:
            * None.

        Returns:
            None.
        """
        self.options_map = dict(zip([self.EC2_STATE_OPT],
                                    [self.ec2_states]))
