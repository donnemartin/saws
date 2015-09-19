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
        * None
    """

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

    def write_default_config(self, source, destination, overwrite=False):
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

    def read_configuration(self):
        """Reads the config file if it exists, else reads the default config.

        Args:
            * None.

        Returns:
            An instance of a ConfigObj.
        """
        config_template = 'sawsrc'
        config_name = '~/.sawsrc'
        default_config = os.path.join(os.path.dirname(__file__), config_template)
        self.write_default_config(default_config, config_name)
        return self._read_configuration(config_name, default_config)

    def get_shortcuts(self, config):
        """Gets the shortcuts from the specified config.

        Args:
            * config: An instance of ConfigObj.

        Returns:
            An OrderedDict containing the shortcut commands as the keys and their
            corresponding full commands as the values.
        """
        return OrderedDict(zip(config['shortcuts'].keys(),
                               config['shortcuts'].values()))
