#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Download posts and comments  from a subreddit

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

from psaw import PushshiftAPI
import pickle


class RedditRecord:
    def __init__(self, subreddit, author, permalink, score, created_utc):
        self.subreddit = subreddit
        self.author = author
        self.permalink = permalink
        self.score = score
        self.created_utc = created_utc

    def __repr__(self):
        return "subreddit: " + str(self.subreddit) + "\n" + \
               "author: " + str(self.author) + "\n" + \
               "permalink: " + str(self.permalink) + "\n" + \
               "score: " + str(self.score) + "\n" + \
               "created_utc: " + str(self.created_utc) + "\n"


class RedditSubmission(RedditRecord):
    def __init__(self, subreddit, author, permalink, score, created_utc,
                 title, selftext, upvote_ratio, removed_by_category):
        super().__init__(subreddit, author, permalink, score, created_utc)
        self.title = title
        self.selftext = selftext
        self.upvote_ratio = upvote_ratio
        self.removed_by_category = removed_by_category

    def __repr__(self):
        return super().__repr__() + \
               "title: " + str(self.title) + "\n" + \
               "selftext: " + str(self.selftext) + "\n" + \
               "upvote_ratio: " + str(self.upvote_ratio) + "\n" + \
               "removed_by_category: " + str(self.removed_by_category) + "\n"


class RedditComment(RedditRecord):
    def __init__(self, subreddit, author, permalink, score, created_utc, body):
        super().__init__(subreddit, author, permalink, score, created_utc)
        self.body = body

    def __repr__(self):
        return super().__repr__() + \
               "body: " + str(self.body) + "\n"


class RedditGenerator:
    def __init__(self, s_name, s_time, e_time):
        """
        :param s_name: subreddit name
        :param s_time: start time as a datetime object
        :param e_time: end time as a datetime object
        """
        self.s_name = s_name
        self.s_time = int(s_time.timestamp())
        self.e_time = int(e_time.timestamp())
        self._api = PushshiftAPI()

    def __iter__(self):
        return self

    def save_all(self, fn):
        """ save the content of the generator as a picked list """
        with open(fn, "wb") as f:
            pickle.dump(list(self), f)


class SubmissionGenerator(RedditGenerator):
    """ Class for download Reddit posts """

    def __init__(self, s_name, s_time, e_time, download_deleted=False):
        """
        :param s_name: subreddit name
        :param s_time: start time as a datetime object
        :param e_time: end time as a datetime object
        :param download_deleted: whether to download deleted posts
        """
        super().__init__(s_name, s_time, e_time)
        self.download_deleted = download_deleted
        self._gen = self._api.search_submissions(
            subreddit=self.s_name, after=self.s_time, before=self.e_time,
            filter=["subreddit", "author", "permalink", "score", "created_utc",
                    "title", "selftext", "upvote_ratio", "removed_by_category"])

    def __next__(self):
        while True:
            p = next(self._gen)
            if hasattr(p, "removed_by_category"):
                if self.download_deleted:
                    return self._formatter(p)
                else:
                    # skip deleted items if not needed
                    continue
            return self._formatter(p)

    @staticmethod
    def _formatter(p):
        if not hasattr(p, "removed_by_category"):
            rm = "None"
        else:
            rm = p.removed_by_category
        r = RedditSubmission(subreddit=p.subreddit,
                             author=p.author,
                             permalink=p.permalink,
                             score=p.score,
                             created_utc=p.created_utc,
                             title=p.title,
                             selftext=p.selftext,
                             upvote_ratio=p.upvote_ratio,
                             removed_by_category=rm)
        return r


class CommentGenerator(RedditGenerator):
    """ Class for download Reddit comments """

    def __init__(self, s_name, s_time, e_time):
        """
        :param s_name: subreddit name
        :param s_time: start time as a datetime object
        :param e_time: end time as a datetime object
        """
        super().__init__(s_name, s_time, e_time)
        self._gen = self._api.search_comments(
            subreddit=self.s_name, after=self.s_time, before=self.e_time,
            filter=["subreddit", "author", "permalink", "score", "created_utc",
                    "body"])

    def __next__(self):
        while True:
            p = next(self._gen)
            if p.body == "[removed]":
                # skip empty item
                continue
            return self._formatter(p)

    @staticmethod
    def _formatter(p):
        r = RedditComment(subreddit=p.subreddit,
                          author=p.author,
                          permalink=p.permalink,
                          score=p.score,
                          created_utc=p.created_utc,
                          body=p.body)
        return r
