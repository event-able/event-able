# -*- coding: utf-8 -*-
#
#  print_coverage.py
#  event-able
#

from __future__ import absolute_import, print_function, division

import sys
import json


def check_coverage(input_file):
    events = json.load(open(input_file))
    total = len(events)

    n_official = sum(1 for e in events
                     if 'acc_official_rating' in e.get('accessibility', {}))
    n_wheelmap = sum(1 for e in events
                     if 'acc_user_link' in e.get('accessibility', {}))

    print('%d/%d (%.0f%%) official matches' % (
        n_official,
        total,
        100.0 * n_official / total
    ))

    print('%d/%d (%.0f%%) wheelmap matches' % (
        n_wheelmap,
        total,
        100.0 * n_official / total
    ))


if __name__ == '__main__':
    check_coverage(*sys.argv[1:])
