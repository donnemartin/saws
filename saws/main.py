#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import click
from .saws import Saws


# Disable Warning: Click detected the use of the unicode_literals
# __future__ import.
click.disable_unicode_literals_warning = True


@click.command()
def cli():
    """Creates and calls Saws.

    Args:
        * None.

    Returns:
        None.
    """
    try:
        saws = Saws()
        saws.run_cli()
    except (EOFError, KeyboardInterrupt):
        saws.config_obj.write()


if __name__ == "__main__":
    cli()
