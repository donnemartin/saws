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
import logging


class SawsLogger(object):
    """Handles Saws logging.

    Attributes:
        * logger: An instance of Logger.
    """

    def __init__(self, name, log_file, log_level):
        """Initializes a Logger for Saws.

        Args:
            * name: A string that represents the logger's name.
            * log_file: A string that represents the log file name.
            * log_level: A string that represents the logging level.

        Returns:
            None.
        """
        self.logger = logging.getLogger(name)
        level_map = {
            'CRITICAL': logging.CRITICAL,
            'ERROR': logging.ERROR,
            'WARNING': logging.WARNING,
            'INFO': logging.INFO,
            'DEBUG': logging.DEBUG
        }
        handler = logging.FileHandler(os.path.expanduser(log_file))
        formatter = logging.Formatter(
            '%(asctime)s (%(process)d/%(threadName)s) '
            '%(name)s %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root_logger = logging.getLogger('saws')
        root_logger.addHandler(handler)
        root_logger.setLevel(level_map[log_level.upper()])
        root_logger.debug('Initializing saws logging.')
        root_logger.debug('Log file %r.', log_file)
