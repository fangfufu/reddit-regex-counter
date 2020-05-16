#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reddit_regex_counter.redditRegexCounter import SubmissionCounter, CommentCounter
from datetime import timedelta, datetime

if __name__ == '__main__':
    # words with 3 capital letters
    pattern = r"\b[A-Z]{3}\b"
    e_time = datetime.now()
    s_time = e_time - timedelta(1)
    s_name = "news"
    # Count the number of occurrence in reddit posts
    s_counter = SubmissionCounter(s_name, s_time, e_time, pattern)
    s_counter.get_result()
    # Count the number of occurrence in comments
    c_counter = CommentCounter(s_name, s_time, e_time, pattern,
                               result=s_counter.result)
    c_counter.get_result()
    # Print out the final dictionary
    print(c_counter)