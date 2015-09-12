#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import click
from .saws import Saws


click.disable_unicode_literals_warning = True


@click.command()
def cli():
    """
    Create and call the CLI
    """
    try:
        saws = Saws()
        saws.run_cli()
    except (EOFError, KeyboardInterrupt):
        saws.config.write()


if __name__ == "__main__":
    cli()
