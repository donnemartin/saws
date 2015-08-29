# -*- coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function

import os
import logging


def create_logger(name, log_file, log_level):
    """
    Create and return logger for package.
    :param name: string logger name
    :param log_file: string log file name
    :param log_level: string
    :return: logger
    """
    logger = logging.getLogger(name)

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

    root_logger = logging.getLogger('iawscli')
    root_logger.addHandler(handler)
    root_logger.setLevel(level_map[log_level.upper()])

    root_logger.debug('Initializing iawscli logging.')
    root_logger.debug('Log file %r.', log_file)

    return logger
