# -*- coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys


def get_key_manager(set_color, get_color,
                    set_fuzzy_match, get_fuzzy_match,
                    refresh_resources, handle_docs):
    """
    Create and initialize keybinding manager
    :return: KeyBindingManager
    """
    assert callable(set_color)
    assert callable(get_color)
    assert callable(set_fuzzy_match)
    assert callable(get_fuzzy_match)
    assert callable(refresh_resources)
    assert callable(handle_docs)
    manager = KeyBindingManager(enable_system_bindings=True)

    @manager.registry.add_binding(Keys.F2)
    def handle_f2(event):
        """
        When F2 has been pressed, fill in the "docs" command.
        """
        handle_docs(from_fkey=True)

    @manager.registry.add_binding(Keys.F3)
    def handle_f3(_):
        """
        Enable/Disable color output.
        """
        set_color(not get_color())

    @manager.registry.add_binding(Keys.F4)
    def handle_f4(_):
        """
        Enable/Disable fuzzy matching.
        """
        set_fuzzy_match(not get_fuzzy_match())

    @manager.registry.add_binding(Keys.F5)
    def handle_f5(_):
        """
        Refreshes AWS resources.
        """
        refresh_resources()

    @manager.registry.add_binding(Keys.F10)
    def handle_f10(event):
        """
        When F10 has been pressed, quit.
        """
        # Unused parameters for linter.
        raise EOFError

    @manager.registry.add_binding(Keys.ControlSpace)
    def handle_ctrl_space(event):
        """
        Initialize autocompletion at cursor.

        If the autocompletion menu is not showing, display it with the
        appropriate completions for the context.

        If the menu is showing, select the next completion.
        """
        b = event.cli.current_buffer
        if b.complete_state:
            b.complete_next()
        else:
            event.cli.start_completion(select_first=False)

    return manager
