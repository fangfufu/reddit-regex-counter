#!/usr/bin/env python3
# -*- coding: utf-8 -*-

if __package__ is None or __package__ == '':
    # noinspection PyUnresolvedReferences
    from redditRegexCounter import RedditRegexCounter
else:
    from .redditRegexCounter import RedditRegexCounter

from datetime import datetime
import click


@click.command()
@click.option("-s", "--start", type=str,
              help="The starting date of the search period, in the format of \
              %Y-%m-%d (e.g. 2020-01-31)")
@click.option("-e", "--end", type=str,
              help="The starting date of the search period, in the format of \
              %Y-%m-%d (e.g. 2020-02-01)")
@click.option("-n", "--name", type=str, required=True,
              help="The name of the subreddit")
@click.option("-p", "--pattern", type=str, required=True,
              help="The regular expression pattern for matching")
def main(start, end, name, pattern):
    """
    Count the number of regular expression appearances within a subreddit
    within a certain period of time.
    """
    s_time = datetime.strptime(start, "%Y-%m-%d")
    e_time = datetime.strptime(end, "%Y-%m-%d")
    counter = RedditRegexCounter(name, s_time, e_time, pattern)
    print(counter)


if __name__ == "__main__":
    main()
