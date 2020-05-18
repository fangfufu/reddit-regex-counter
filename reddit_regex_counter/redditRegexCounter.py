#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" count the number of regex matches in a subreddit

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

if __package__ is None or __package__ == '':
    # noinspection PyUnresolvedReferences
    from redditDownloader import SubmissionGenerator, CommentGenerator
else:
    from .redditDownloader import SubmissionGenerator, CommentGenerator

from datetime import timedelta, datetime
import pickle
import re


class Counter:
    def __init__(self, result=None):
        if result is None:
            result = {}
        self.result = result

    def __repr__(self):
        s = "match:\tcount:\n"
        for i in self.result.items():
            s += str(i[0]) + "\t" + str(i[1]) + "\n"
        return s

    def save_result(self, fn):
        with open(fn, "wb") as f:
            pickle.dump(self.result, f)

    def load_result(self, fn):
        with open(fn, "rb") as f:
            self.result = pickle.load(f)


class RegexCounter(Counter):
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
        self._gen = gen
        self.attr = attr
        self.pattern = pattern
        self.case = case
        super().__init__(result)

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
        return self

    def get_result(self):
        """ Iterate through the generator, and obtain the final result """
        for i in self:
            pass
        self.result = dict(sorted(self.result.items(), key=lambda x: x[1],
                                  reverse=True))
        return self.result

class SubmissionCounter(RegexCounter):
    """ Class for counting regex in Reddit submissions """

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
        :param result: the optional result dictionary which contains previous
        results
        :param download_deleted: whether to download deleted posts
        """
        super().__init__(SubmissionGenerator(s_name, s_time, e_time,
                                             download_deleted),
                         ["title", "selftext"], pattern, case, result)


class CommentCounter(RegexCounter):
    """ Class for counting regex in Reddit comments"""

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
        :param result: the optional result dictionary which contains previous
        results
        """
        super().__init__(CommentGenerator(s_name, s_time, e_time),
                         ["body"], pattern, case, result)


class RedditRegexCounter(Counter):
    """ Class for counting regex in both submissions and comments """

    def __init__(self, s_name, s_time, e_time, pattern, case=0,
                 result=None, download_deleted=False):
        """

        :param s_name: subreddit name
        :param s_time: start time as a datetime object
        :param e_time: end time as a datetime object
        :param pattern: the regex pattern to search
        :param case: whether we want to perform case conversion:
            - -1, convert to lower caser
            - 0, does not perform case conversion
            - 1, convert to upper case
        :param result: the optional result dictionary which contains previous
        results
        :param download_deleted: whether to download deleted posts
        """
        # Count the number of occurrence in reddit posts
        s_counter = SubmissionCounter(s_name, s_time, e_time, pattern,
                                      result=result,
                                      download_deleted=download_deleted)
        s_counter.get_result()
        # Count the number of occurrence in comments
        c_counter = CommentCounter(s_name, s_time, e_time, pattern,
                                   result=s_counter.result)
        c_counter.get_result()
        super().__init__(c_counter.result)