# reddit-regex-counter
Count the number of regular expression appearances within a subreddit within 
a certain period of time

## Description
This package is a wrapper for [psaw](https://github.com/dmarx/psaw). It allows
the user to easily count the number of matches of a regular expression within
a certain period of time within a subreddit. The regular expression matches 
are stored in a dictionary, with the matches themselves being the keys, and 
the number of occurrences as the values.

## Installation
To download and install directly from [pypi](https://pypi.org/), run the 
following command: 

    pip3 install reddit-regex-counter
    
Alternatively, to directly install from the Github resource repository, 
please first clone this repository, then run:

    pip3 install .

## Usage

    Usage: reddit-regex-counter [OPTIONS]

    Count the number of regex appearances within a subreddit between a certain
    period of time

    Options:
    -s, --start TEXT    The starting date of the search period, in the format of
                        %Y-%m-%d (e.g. 2020-01-31)
    -e, --end TEXT      The starting date of the search period, in the format of
                        %Y-%m-%d (e.g. 2020-02-01)
    -n, --name TEXT     The name of the subreddit  [required]
    -p, --pattern TEXT  The regular expression pattern for matching  [required]
    --help              Show this message and exit.
    
## Example Output

    $ reddit-regex-counter \
        -s 2020-05-17 \
        -e 2020-05-18 \
        -n news \
        -p "\b[A-Z]{3}\b"
    Match:  Count:
    USA     59
    PPP     58
    NOT     52
    AND     40
    CEO     35
    YOU     32
    GOP     32
    THE     31
    WHO     29
    CNN     28
    CCP     27
    PPE     27
    CIA     23
    ALL     22
    LOL     19
    FBI     18
    ...
 
## License

reddit-regix-counter - count the number of regex appearance within a
subreddit during a certain period. 

Copyright (C) 2020  Fufu Fang

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
