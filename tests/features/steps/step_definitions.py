# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pip
import pexpect
from behave import given, when, then


@given('we have iawscli installed')
def step_cli_installed(context):
    """
    Make sure iawscli is in installed packages.
    """
    dists = set([di.key for di in pip.get_installed_distributions()])
    assert 'iawscli' in dists


@when('we run iawscli')
def step_run_cli(context):
    """
    Run the process using pexpect.
    """
    context.cli = pexpect.spawnu('iawscli')


@when('we wait for prompt')
def step_expect_prompt(context):
    """
    Expect to see prompt.
    """
    context.cli.expect('iawscli> ')


@when('we send "ctrl + d"')
def step_send_ctrld(context):
    """
    Send Ctrl + D to exit.
    """
    context.cli.sendcontrol('d')
    context.exit_sent = True


@then('iawscli exits')
def step_expect_exit(context):
    """
    Expect cli to exit.
    """
    context.cli.expect(pexpect.EOF)


@then('we see iawscli prompt')
def step_see_prompt(context):
    """
    Expect to see prompt.
    """
    context.cli.expect('iawscli> ')
