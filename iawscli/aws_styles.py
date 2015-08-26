"""
Aws styling.
This contains the default style from Pygments, but adds the styling for
Aws specific Tokens on top.
"""
from __future__ import unicode_literals
from pygments.token import Token
from pygments.styles.default import DefaultStyle


__all__ = (
    'default_style_extensions',
    'DefaultStyle',
)


class AwsStyle(DefaultStyle):
    styles = {
        Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
    }
    styles.update(DefaultStyle.styles)
