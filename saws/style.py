# -*- coding: utf-8

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

from pygments.util import ClassNotFound
from prompt_toolkit.styles import merge_styles, style_from_pygments_cls, Style
import pygments.styles


class StyleFactory(object):
    """Creates a custom saws style.

    Provides styles for the completions menu and toolbar.

    Attributes:
        * style: An instance of a Pygments Style.
    """

    def __init__(self, name):
        """Initializes StyleFactory.

        Args:
            * name: A string representing the pygments style.

        Returns:
            An instance of CliStyle.
        """
        self.style = self.style_factory(name)

    def style_factory(self, name):
        """Retrieves the specified pygments style.

        If the specified style is not found, the native style is returned.

        Args:
            * name: A string representing the pygments style.

        Returns:
            An instance of CliStyle.
        """
        try:
            style = pygments.styles.get_style_by_name(name)
        except ClassNotFound:
            style = pygments.styles.get_style_by_name('native')

        # Create styles dictionary.
        return merge_styles([
            style_from_pygments_cls(style),
            Style.from_dict({
                'scrollbar': 'bg:#00aaaa',
                'scrollbar.button': 'bg:#003333',
                'completion-menu.completion': 'bg:#008888 #ffffff',
                'completion-menu.completion.current': 'bg:#00aaaa #000000',
                'system-toolbar': 'noinherit bold',
                'search-toolbar': 'noinherit bold',
                'search-toolbar.text': 'nobold',
                'arg-toolbar': 'noinherit bold',
                'arg-toolbar.text': 'nobold',
                'bottom-toolbar': 'bg:#222222 #cccccc',
                'toolbar.off': 'bg:#222222 #696969',
                'toolbar.on': 'bg:#222222 #ffffff',
            })
        ])
