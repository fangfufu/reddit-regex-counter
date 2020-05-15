#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" redditRegexCounter.py - count the number of regex matches in a subreddit

Copyright (C) 2020  Fufu Fang
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; w\without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

__author__ = "Fufu Fang"
__copyright__ = "The GNU General Public License v3.0"

from redditDownloader import SubmissionGenerator, CommentGenerator
import pickle
import re


class RegexCounter:
    """Class for counting the number of regex appearance from a generator
    """

    def __init__(self, gen, attr, pattern, case=0, result=None):
        """
        :param gen: the generator for the items
        :param attr: the attributes within the item which contain the text
        :param pattern: the regex pattern to search
        :param case: whether we want to perform case conversion:
            - -1, convert to lower caser
            - 0, does not perform case conversion
            - 1, convert to upper case
        :param result: the optional resultionary which contains previous results
        """
        if result is None:
            result = {}
        self._gen = gen
        self.attr = attr
        self.pattern = pattern
        self.case = case
        self.result = result

    def __iter__(self):
        return self

    def __next__(self):
        item = next(self._gen)
        for attr in self.attr:
            extracted = re.findall(self.pattern, getattr(item, attr))
            for word in extracted:
                if self.case == 0:
                    pass
                elif self.case == -1:
                    word = word.lower()
                elif self.case == 1:
                    word = word.upper()
                else:
                    raise ValueError("case must be either -1, 0, or 1")

                if word in self.result:
                    self.result[word] += 1
                else:
                    self.result[word] = 1
        self.result = dict(sorted(self.result.items(), key=lambda x:x[1],
                             reverse=True))
        return self

    def save_result(self, fn):
        with open(fn, "wb") as f:
            pickle.dump(self.result, f)

    def load_result(self, fn):
        with open(fn, "rb") as f:
            self.result = pickle.load(f)

    def get_result(self):
        for i in self:
            pass
        return self.result

    def __repr__(self):
        s = "word:\tcount:\n"
        for i in self.result.items():
            s += str(i[0]) + "\t" + str(i[1]) + "\n"
        return s


class SubmissionCounter(RegexCounter):
    """ Class for counting regex in a Reddit submission """

    def __init__(self, s_name, s_time, e_time, pattern, case=0, result=None,
                 download_deleted=False):
        """
        :param s_name: subreddit name
        :param s_time: start time as a datetime object
        :param e_time: end time as a datetime object
        :param pattern: the regex pattern to search
        :param case: whether we want to perform case conversion:
            - -1, convert to lower caser
            - 0, does not perform case conversion
            - 1, convert to upper case
        :param result: the optional resultionary which contains previous results
        :param download_deleted: whether to download deleted posts
        """
        if result is None:
            result = {}
        super().__init__(SubmissionGenerator(s_name, s_time, e_time,
                                             download_deleted),
                         ["title", "selftext"], pattern, case, result)


class CommentCounter(RegexCounter):
    """ Class for counting regex in a Reddit comment"""

    def __init__(self, s_name, s_time, e_time, pattern, case=0, result=None):
        """
        :param s_name: subreddit name
        :param s_time: start time as a datetime object
        :param e_time: end time as a datetime object
        :param pattern: the regex pattern to search
        :param case: whether we want to perform case conversion:
            - -1, convert to lower caser
            - 0, does not perform case conversion
            - 1, convert to upper case
        :param result: the optional resultionary which contains previous results
        """
        if result is None:
            result = {}
        super().__init__(CommentGenerator(s_name, s_time, e_time),
                         ["body"], pattern, case, result)
