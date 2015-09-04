# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import os
import pexpect
import fixture_utils as fixutils


def before_all(context):
    """
    Set env parameters.
    """
    os.environ['LINES'] = "50"
    os.environ['COLUMNS'] = "120"
    os.environ['PAGER'] = 'cat'
    context.exit_sent = False


def after_scenario(context, _):
    """
    Cleans up after each test complete.
    """
    if hasattr(context, 'cli') and not context.exit_sent:
        # Send Ctrl + D into cli
        context.cli.sendcontrol('d')
        context.cli.expect(pexpect.EOF)
