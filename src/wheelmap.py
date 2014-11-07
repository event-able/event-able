#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  wheelmap.py
#  event-able
#

"""
Given a list of venue-to-wheelmap links, cache their accessibility status.
"""

from __future__ import absolute_import, print_function, division

import os
import sys
import optparse
import json

import requests

API_ENDPOINT = 'http://wheelmap.org/api/nodes/{node_id}.json'
TOKEN = os.environ['WHEELMAP_API_TOKEN']


def check_wheelmap(input_file, output_file):
    print('Checking wheelmap for accessibility...')
    venues = _load_venues(input_file)
    _detect_accessibility(venues)
    _save_venues_as_json(venues, output_file)


def _load_venues(input_file):
    venues = []
    with open(input_file) as istream:
        for l in istream:
            name, link = l.rstrip().split(': ', 1)
            venues.append({'name': name,
                           'acc_user_link': link})

    return venues


def _detect_accessibility(venues):
    for i, v in enumerate(venues):
        link = v['acc_user_link']
        print('({0}/{1}) {2}'.format(i + 1, len(venues), link))
        v['acc_user_rating'] = _check_wheelmap(link)

    print()


def _check_wheelmap(link):
    node_id = link.split('/')[-1]
    return _api_request(node_id)


def _api_request(node_id):
    resp = requests.get(API_ENDPOINT.format(node_id=node_id),
                        headers={'X-API-KEY': TOKEN})
    assert resp.status_code == 200
    node = resp.json()['node']
    wheelchair = node['wheelchair']

    assert wheelchair in ('yes', 'unknown', 'limited', 'no')

    return wheelchair


def _save_venues_as_json(venues, output_file):
    with open(output_file, 'w') as ostream:
        json.dump(venues, ostream, sort_keys=True, indent=2,
                  separators=(',', ': '))


def _create_option_parser():
    usage = \
"""%prog [options] input.list output.json

Add wheelmap accessibility information to the venue listing."""  # nopep8

    parser = optparse.OptionParser(usage)

    return parser


def main(argv):
    parser = _create_option_parser()
    (options, args) = parser.parse_args(argv)

    if len(args) != 2:
        parser.print_help()
        sys.exit(1)

    check_wheelmap(*args)


if __name__ == '__main__':
    main(sys.argv[1:])
