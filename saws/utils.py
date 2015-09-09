# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import six
import shlex
import fuzzyfinder
from prompt_toolkit.completion import Completion


class TextUtils(object):

    def shlex_split(self, text):
        """
        Wrapper for shlex, because it does not seem to handle unicode in 2.6.
        :param text: string
        :return: list
        """
        if six.PY2:
            text = text.encode('utf-8')
        return shlex.split(text)

    def find_collection_matches(self, word, lst, fuzzy):
        """
        Yield all matching names in list
        :param lst: collection
        :param word: string user typed
        :param fuzzy: boolean
        :return: iterable
        """
        if fuzzy:
            for suggestion in fuzzyfinder.fuzzyfinder(word, lst):
                yield Completion(suggestion, -len(word))
        else:
            for name in sorted(lst):
                if name.startswith(word) or not word:
                    yield Completion(name, -len(word))

    def find_matches(self, text, collection, fuzzy):
        """
        Find all matches for the current text
        :param text: text before cursor
        :param collection: collection to suggest from
        :param fuzzy: boolean
        :return: iterable
        """
        text = self.last_token(text).lower()
        for suggestion in self.find_collection_matches(
                text, collection, fuzzy):
            yield suggestion

    def get_tokens(self, text):
        """
        Parse out all tokens.
        :param text:
        :return: list
        """
        if text is not None:
            text = text.strip()
            words = self.safe_split(text)
            return words
        return []

    def last_token(self, text):
        """
        Find last word in a sentence
        :param text:
        :return:
        """
        if text is not None:
            text = text.strip()
            if len(text) > 0:
                word = self.safe_split(text)[-1]
                word = word.strip()
                return word
        return ''

    def safe_split(self, text):
        """
        Shlex can't always split. For example, "\" crashes the completer.
        """
        try:
            words = self.shlex_split(text)
            return words
        except:
            return text
