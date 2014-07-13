# -*- coding: utf-8 -*-
#
#  venues.py
#  event-able
#

"""
Parse accessibility data about potential venues.
"""

import csv
import sys
import json


def parse_venue_info(input_csv, wheelmap_json, output_json):
    wheelmap = _load_wheelmap_venues(wheelmap_json)

    buildings = _load_buildings(input_csv)
    venues = map(_transform_building, buildings)
    _add_wheelmap(venues, wheelmap)

    # only keep ones with accessibility ratings
    venues = [v for v in venues
              if v['acc_official_rating'] > 0 or 'acc_user_rating' in v]

    _dump_venues(venues, output_json)


def _add_wheelmap(venues, wheelmap):
    for v in venues:
        if 'name' in v:
            name = v['name']
            if name in wheelmap:
                v.update(wheelmap[name])


def _load_wheelmap_venues(input_file):
    venues = json.load(open(input_file))
    by_name = {
        v['name']: {
            'acc_user_link': v['link'],
            'acc_user_rating': v['wheelchair'],
        }
        for v in venues
    }
    return by_name


def _load_buildings(input_csv):
    with open(input_csv) as istream:
        return list(csv.DictReader(istream))


def _transform_building(b):
    v = {}
    v['acc_official_rating'] = int(b['Accessibility rating'])
    v['acc_official_type'] = b['Accessibility type']
    v['acc_official_desc'] = b['Accessibility type description']
    v['latitude'] = b['Latitude']
    v['longitude'] = b['Longitude']
    v['address'] = "{0}, {1} {2}".format(
        b['Street address'].strip().title(),
        b['Suburb'].strip().title(),
        b['Postcode'].strip(),
    )
    name = b['Building name'].strip()
    if name:
        v['name'] = name

    return v


def _dump_venues(venues, output_file):
    with open(output_file, 'w') as ostream:
        json.dump(venues, ostream, sort_keys=True, indent=2,
                  separators=(',', ': '))


if __name__ == '__main__':
    parse_venue_info(*sys.argv[1:])
