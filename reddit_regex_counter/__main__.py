#!/usr/bin/env python3
# -*- coding: utf-8 -*-

if __package__ is None or __package__ == '':
    # noinspection PyUnresolvedReferences
    from redditRegexCounter import RedditRegexCounter
else:
    from .redditRegexCounter import RedditRegexCounter

from argparse import ArgumentParser
from datetime import datetime


def parse_args():
    parser=ArgumentParser(description="Count the number of regex matches within\
                          a subreddit")
    parser.add_argument("-s", "--start", type=str,
              help="The starting date of the search period, in the format of \
              %%Y-%%m-%%d (e.g. 2020-01-31)")
    parser.add_argument("-e", "--end", type=str,
              help="The starting date of the search period, in the format of \
              %%Y-%%m-%%d (e.g. 2020-02-01)")
    parser.add_argument("-n", "--name", type=str, required=True,
              help="The name of the subreddit")
    parser.add_argument("-p", "--pattern", type=str, required=True,
              help="The regular expression pattern for matching")
    return parser.parse_args()

def main():
    args = parse_args()
    s_time = datetime.strptime(args.start, "%Y-%m-%d")
    e_time = datetime.strptime(args.end, "%Y-%m-%d")
    counter = RedditRegexCounter(args.name, s_time, e_time, args.pattern)
    print(counter)

if __name__ == "__main__":
    main()
