#!/usr/bin/env python3
# -*- coding: utf-8 -*-

if __package__ is None or __package__ == '':
    # noinspection PyUnresolvedReferences
    from redditRegexCounter import RedditRegexCounter
else:
    from .redditRegexCounter import RedditRegexCounter

from datetime import timedelta, datetime
import click


@click.command()
@click.option("-s", "--start", type=str,
              help="The starting date of the search period, in the format of \
              %Y-%m-%d")
@click.option("-e", "--end", type=str,
              help="The starting date of the search period, in the format of \
              %Y-%m-%d")
@click.option("-n", "--name", type=str, required=True,
              help="The name of the subreddit")
@click.option("-p", "--pattern", type=str, required=True,
              help="The regular expression pattern for matching")
def main(start, end, name, pattern):
    """
    Count the number of regex appearances within a subreddit between a certain
    period of time
    """
    print(start)
    print(end)

    e_time = datetime.now()
    s_time = e_time - timedelta(1)
    counter = RedditRegexCounter(name, s_time, e_time, pattern)
    print(counter)


if __name__ == "__main__":
    main()
