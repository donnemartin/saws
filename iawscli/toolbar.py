# -*- coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function
from pygments.token import Token


def create_toolbar_handler(is_color, is_fuzzy, is_shortcuts):

    assert callable(is_color)
    assert callable(is_fuzzy)
    assert callable(is_shortcuts)

    def get_toolbar_items(_):
        """
        Return bottom menu items
        :param _: cli instance
        :return: list of Token.Toolbar
        """
        if is_color():
            color_token = Token.Toolbar.On
            color = 'ON'
        else:
            color_token = Token.Toolbar.Off
            color = 'OFF'
        if is_fuzzy():
            fuzzy_token = Token.Toolbar.On
            fuzzy = 'ON'
        else:
            fuzzy_token = Token.Toolbar.Off
            fuzzy = 'OFF'
        if is_shortcuts():
            shortcuts_token = Token.Toolbar.On
            shortcuts = 'ON'
        else:
            shortcuts_token = Token.Toolbar.Off
            shortcuts = 'OFF'
        return [
            (Token.Toolbar, ' [F1] Help '),
            (Token.Toolbar, ' [F2] Docs '),
            (color_token, ' [F3] Color: {0} '.format(color)),
            (fuzzy_token, ' [F4] Fuzzy: {0} '.format(fuzzy)),
            (shortcuts_token, ' [F5] Shortcuts: {0} '.format(shortcuts)),
            (Token.Toolbar, ' [F6] Refresh '),
            (Token.Toolbar, ' [F10] Exit ')
        ]
    return get_toolbar_items
