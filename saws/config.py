# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import shutil
import os
from collections import OrderedDict
from configobj import ConfigObj


def _read_config(usr_config, def_config=None):
    """
    Read config file (if not exists, read default config).
    :param usr_config: string: config file name
    :param def_config: string: default name
    :return: ConfigParser
    """
    usr_config_file = os.path.expanduser(usr_config)
    cfg = ConfigObj()
    cfg.filename = usr_config_file
    if def_config:
        cfg.merge(ConfigObj(def_config, interpolation=False))
    cfg.merge(ConfigObj(usr_config_file, interpolation=False))
    return cfg


def write_default_config(source, destination, overwrite=False):
    """
    Write default config (from template).
    :param source: string: path to template
    :param destination: string: path to write
    :param overwrite: boolean
    """
    destination = os.path.expanduser(destination)
    if not overwrite and os.path.exists(destination):
        return
    shutil.copyfile(source, destination)


def get_package_path():
        """
        Find out pakage root path.
        :return: string: path
        """
        return os.path.dirname(__file__)


def read_configuration():
    config_template = 'sawsrc'
    config_name = '~/.sawsrc'
    default_config = os.path.join(get_package_path(), config_template)
    write_default_config(default_config, config_name)
    return _read_config(config_name, default_config)


def get_shortcuts(config):
    return OrderedDict(zip(config['shortcuts'].keys(),
                           config['shortcuts'].values()))
