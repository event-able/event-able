# -*- coding: utf-8 -*-
#
#  missing_wheelmap.py
#  event-able
#

"""
Find the venue name and address of each venue without a wheelmap link.
"""

from __future__ import absolute_import, print_function, division

import sys
import json
import urllib
from xml.sax.saxutils import unescape


def main(event_json):
    events = json.load(open(event_json))

    seen = set()

    no_match = set()
    for e in events:
        if 'acc_user_rating' in e.get('accessibility', no_match):
            continue

        name = e['venue']['name']
        if name not in seen and 'various' not in name.lower():
            _print_venue(e['venue'])
            seen.add(name)


def _print_venue(venue):
    print(_unquote(venue['name']).encode('utf8'))
    address = ', '.join(venue['address'] + [' '.join([venue['city'],
                                                      venue['postcode']])])
    address = _norm_address(address)
    print(address)
    print('http://maps.google.com.au/#/?q={0}'.format(urllib.quote(address)))
    print('http://wheelmap.org/en/map#/?q={0}'.format(urllib.quote(address)))
    print()


def _unquote(v):
    unescape_table = {
        '&quot;': '"',
        '&apos;': "'",
        '&#39;': "'",
    }
    return unescape(urllib.unquote(v), unescape_table)


def _norm_address(address):
    REMAP = [(u'\u2013', '-')]

    for from_, to_ in REMAP:
        address = address.replace(from_, to_)

    return address


if __name__ == '__main__':
    main(*sys.argv[1:])
