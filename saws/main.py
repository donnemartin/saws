#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import click
from .iawscli import IAwsCli


click.disable_unicode_literals_warning = True


@click.command()
def cli():
    """
    Create and call the CLI
    """
    try:
        iaws_cli = IAwsCli()
        iaws_cli.run_cli()
    except (EOFError, KeyboardInterrupt):
        iaws_cli.config.write()


if __name__ == "__main__":
    cli()
