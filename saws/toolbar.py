# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
from pygments.token import Token


def create_toolbar_handler(color_cfg, fuzzy_cfg, shortcuts_cfg):
    """Creates the toolbar handler.

    Args:
        * color_cfg: A boolean that spedifies whether to color the output.
        * fuzzy_cfg: A boolean that spedifies whether to do fuzzy matching.
        * shortcuts_cfg: A boolean that spedifies whether to match shortcuts.

    Returns:
        A callable get_toolbar_items.
    """
    assert callable(color_cfg)
    assert callable(fuzzy_cfg)
    assert callable(shortcuts_cfg)

    def get_toolbar_items(_):
        """Returns bottom menu items.

        Args:
            * _: An instance of prompt_toolkit's Cli (not used).

        Returns:
            A list of Token.Toolbar.
        """
        if color_cfg():
            color_token = Token.Toolbar.On
            color = 'ON'
        else:
            color_token = Token.Toolbar.Off
            color = 'OFF'
        if fuzzy_cfg():
            fuzzy_token = Token.Toolbar.On
            fuzzy = 'ON'
        else:
            fuzzy_token = Token.Toolbar.Off
            fuzzy = 'OFF'
        if shortcuts_cfg():
            shortcuts_token = Token.Toolbar.On
            shortcuts = 'ON'
        else:
            shortcuts_token = Token.Toolbar.Off
            shortcuts = 'OFF'
        return [
            (Token.Toolbar, ' [F1] Docs '),
            (color_token, ' [F2] Color: {0} '.format(color)),
            (fuzzy_token, ' [F3] Fuzzy: {0} '.format(fuzzy)),
            (shortcuts_token, ' [F4] Shortcuts: {0} '.format(shortcuts)),
            (Token.Toolbar, ' [F5] Refresh '),
            (Token.Toolbar, ' [F10] Exit ')
        ]

    return get_toolbar_items
