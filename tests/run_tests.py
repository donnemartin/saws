#!/usr/bin/env python
from __future__ import unicode_literals

from buffer_tests import *
from document_tests import *
from inputstream_tests import *
from key_binding_tests import *
from screen_tests import *
from regular_languages_tests import *
from layout_tests import *

import unittest

# Import modules for syntax checking.
import iawscli
import iawscli.application
import iawscli.buffer
import iawscli.clipboard
import iawscli.completion
import iawscli.contrib.completers
import iawscli.contrib.regular_languages
import iawscli.contrib.telnet
import iawscli.contrib.validators
import iawscli.document
import iawscli.enums
import iawscli.eventloop.base
import iawscli.eventloop.inputhook
import iawscli.eventloop.posix
import iawscli.eventloop.posix_utils
import iawscli.eventloop.utils
import iawscli.focus_stack
import iawscli.history
import iawscli.input
import iawscli.interface
import iawscli.key_binding
import iawscli.keys
import iawscli.layout
import iawscli.libs
import iawscli.output
import iawscli.reactive
import iawscli.renderer
import iawscli.search_state
import iawscli.selection
import iawscli.shortcuts
import iawscli.styles
import iawscli.terminal
import iawscli.terminal.vt100_input
import iawscli.terminal.vt100_output
import iawscli.utils
import iawscli.validation

if __name__ == '__main__':
    unittest.main()
