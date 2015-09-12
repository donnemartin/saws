# -*- coding: utf-8
from pygments.token import Token
from pygments.style import Style
from pygments.util import ClassNotFound
from prompt_toolkit.styles import default_style_extensions
import pygments.styles


def style_factory(name):
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

    class CliStyle(Style):
        """Custom Saws Style.

        Provides styles for the completions menu and toolbar.

        Attributes:
            * styles: A dictionary that contains pygments style information.
        """

        styles = {}
        styles.update(style.styles)
        styles.update(default_style_extensions)
        styles.update({
            Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
            Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
            Token.Menu.Completions.ProgressButton: 'bg:#003333',
            Token.Menu.Completions.ProgressBar: 'bg:#00aaaa',
            Token.Toolbar: 'bg:#222222 #cccccc',
            Token.Toolbar.Off: 'bg:#222222 #004444',
            Token.Toolbar.On: 'bg:#222222 #ffffff',
            Token.Toolbar.Search: 'noinherit bold',
            Token.Toolbar.Search.Text: 'nobold',
            Token.Toolbar.System: 'noinherit bold',
            Token.Toolbar.Arg: 'noinherit bold',
            Token.Toolbar.Arg.Text: 'nobold'
        })

    return CliStyle
