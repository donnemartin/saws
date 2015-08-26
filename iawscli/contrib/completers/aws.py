from __future__ import unicode_literals
import subprocess
import os
from cStringIO import StringIO
import sys
import re
from six import string_types
from iawscli.completion import Completer, Completion
from iawscli.contrib.completers import WordCompleter


__all__ = (
    'AwsCliCompleter',
)


class AwsCliCompleter(WordCompleter):
    def __init__(self, words, aws_driver, aws_completer, ignore_case=False, meta_dict=None, WORD=False,
                 match_middle=False):
        self.words = list(words)
        self.ignore_case = ignore_case
        self.meta_dict = meta_dict or {}
        self.WORD = WORD
        self.match_middle = match_middle
        self.aws_driver = aws_driver
        self.aws_completer = aws_completer
        assert all(isinstance(w, string_types) for w in self.words)

    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=self.WORD)
        if self.ignore_case:
            word_before_cursor = word_before_cursor.lower()
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        self.aws_completer.complete(document.text, len(document.text))
        sys.stdout = old_stdout
        res = mystdout.getvalue()
        res = re.sub('\n', '', res)
        res_list = res.split()
        self.words = []
        if len(document.text) < 3:
            self.words = ['aws']
        self.words.extend(res_list)
        word_before_cursor2 = document.get_word_before_cursor(empty_on_space=False, WORD=self.WORD)

        def word_matches(word):
            """ True when the word before the cursor matches. """
            if self.match_middle:
                return word_before_cursor in word
            else:
                return word.startswith(word_before_cursor)

        for a in self.words:
            if word_matches(a.lower()):
                display_meta = self.meta_dict.get(a, '')
                yield Completion(a, -len(word_before_cursor), display_meta=display_meta)
