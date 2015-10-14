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
import shutil
import os
try:
    from collections import OrderedDict
except:
    from ordereddict import OrderedDict
from configobj import ConfigObj


class Config(object):
    """Reads and writes the config file `sawsrc`.

    Attributes:
        * SHORTCUTS: A string that represents the start of shortcuts in
            the config file ~/.sawsrc.
        * MAIN: A string that represents the main set of configs in
            ~/.sawsrc.
        * THEME: A string that represents the config theme.
        * LOG_FILE: A string that represents the config log file location.
        * LOG_LEVEL: A string that represents the config default log
            file level.
        * COLOR: A string that represents the config color output mode.
        * FUZZY: A string that represents the config fuzzy matching mode.
        * SHORTCUT: A string that represents the config shortcut matching
             mode.
    """

    SHORTCUTS = 'shortcuts'
    MAIN = 'main'
    THEME = 'theme'
    LOG_FILE = 'log_file'
    LOG_LEVEL = 'log_level'
    COLOR = 'color_output'
    FUZZY = 'fuzzy_match'
    SHORTCUT = 'shortcut_match'

    def get_shortcuts(self, config_obj):
        """Gets the shortcuts from the specified config.

        Args:
            * config_obj: An instance of ConfigObj.

        Returns:
            An OrderedDict containing the shortcut commands as the keys and
            their corresponding full commands as the values.
        """
        shortcut_config_obj = self.read_configuration('saws.shortcuts',
                                                      '~/.saws.shortcuts')
        return OrderedDict(zip(shortcut_config_obj[self.SHORTCUTS].keys(),
                               shortcut_config_obj[self.SHORTCUTS].values()))

    def read_configuration(self, config_template=None, config_path=None):
        """Reads the config file if it exists, else reads the default config.

        Args:
            * config_template: A string representing the template file name.
            * config_path: A string representing the template file path.

        Returns:
            An instance of a ConfigObj.
        """
        if config_template is None:
            config_template = 'sawsrc'
        if config_path is None:
            config_path = '~/.sawsrc'
        config_template_path = os.path.join(os.path.dirname(__file__),
                                            config_template)
        self._copy_template_config(config_template_path, config_path)
        return self._read_configuration(config_path, config_template_path)

    def _read_configuration(self, usr_config, def_config=None):
        """Reads the config file if it exists, else reads the default config.

        Internal method, call read_configuration instead.

        Args:
            * usr_config: A string that specifies the config file name.
            * def_config: A string that specifies the config default file name.

        Returns:
            An instance of a ConfigObj.
        """
        usr_config_file = os.path.expanduser(usr_config)
        cfg = ConfigObj()
        cfg.filename = usr_config_file
        if def_config:
            cfg.merge(ConfigObj(def_config, interpolation=False))
        cfg.merge(ConfigObj(usr_config_file, interpolation=False))
        return cfg

    def _copy_template_config(self, source, destination, overwrite=False):
        """Writes the default config from a template.

        Args:
            * source: A string that specifies the path to the template.
            * destination: A string that specifies the path to write.
            * overwite: A boolean that specifies whether to overwite the file.

        Returns:
            None.
        """
        destination = os.path.expanduser(destination)
        if not overwrite and os.path.exists(destination):
            return
        shutil.copyfile(source, destination)
