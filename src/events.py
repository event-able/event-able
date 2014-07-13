# -*- coding: utf-8 -*-
#
#  events.py
#  event-able
#

"""
Parsing the XML event feed.
"""

import sys
import optparse
import datetime
import urllib
from xml.sax.saxutils import unescape

import json

from xml.etree import ElementTree
import characteristic as ch

DEFAULT_IMAGE = 'http://my.visitvictoria.com/Multimedia/WLS_Thumb__9441161_TVIC_Generic_image__calendar_iStock_000021269370.jpg'  # noqa

ALIASES = {
    "Shrine of Remembrance": "Shrine of Remembrance Reserve",
    "Royal Exhibition Building": "Exhibition Building & Melbourne Museum",
    "Royal Exhibition Building and Carlton Gardens South": "Exhibition Building & Melbourne Museum"
}

def build_event_json(input_file, venues_file, output_dir):
    events = parse_events(input_file)
    events = _prune_historical_events(events)
    events = sorted(events, key=lambda e: e.date)

    venues = _load_venue_accessibility(venues_file)
    _add_venue_accessibility(venues, events)

    melbourne, regional = _split_by_region(events)

    _save_events(melbourne, output_dir + '/melbourne.json')
    _save_events(regional, output_dir + '/regional.json')
    _save_events(events, output_dir + '/all.json')


def _prune_historical_events(events):
    return [e for e in events if not e.is_historical()]


def _split_by_region(events):
    melbourne = []
    regional = []
    for e in events:
        if e.region == 'Melbourne':
            melbourne.append(e)
        else:
            regional.append(e)

    return melbourne, regional


def _load_venue_accessibility(venues_file):
    return json.load(open(venues_file))


def _add_venue_accessibility(venues, events):
    by_name = {v['name']: v for v in venues
               if 'name' in v}
    by_address = {v['address']: v for v in venues
                  if 'address' in v}

    for e in events:
        v = _match_venue(e, by_name, by_address)
        if v:
            e.set_accessibility({
                a: b
                for a, b in v.iteritems()
                if a.startswith('acc_')
            })


def _match_venue(e, by_name, by_address):
    venue = e.venue
    if venue.name in by_name:
        return by_name[venue.name]

    if venue.name in ALIASES:
        return by_name[ALIASES.get(venue.name)]

    address = u'{0}, {1} {2}'.format(
        venue.address[0].title(),
        venue.city.title(),
        venue.postcode
    )
    if address in by_address:
        return by_address[address]


def _save_events(events, filename):
    dicts = [e.to_dict() for e in events]
    with open(filename, 'w') as ostream:
        json.dump(dicts, ostream, sort_keys=True, indent=2,
                  separators=(',', ': '))


@ch.attributes(['guid', 'link', 'category', 'title', 'description',
                'region', 'venue', 'isfree', 'date', 'tags',
                'accessibility', 'image'])
class Event(object):
    @classmethod
    def parse(cls, node):
        return Event(
            guid=node.find('guid').text,
            link=node.find('link').text,
            category=node.find('category').text,
            title=_unquote(node.find('title').text),
            description=_unquote(node.find('description').text),
            region=node.find('{myEvents}marketingRegion').text or 'Melbourne',
            venue=Venue.parse(node.find('{myEvents}venue')),
            isfree=node.find('{myEvents}freeEntry').text,
            date=parse_date(node.find('{myEvents}eventDate').text),
            tags=[t.text for t in node.findall('{myEvents}tags')],
            image=cls._get_first_image(node),
            accessibility=None,
        )

    @staticmethod
    def _get_first_image(node):
        query = '{myEvents}multimedia/image/serverPath'
        images = [l.text for l in node.findall(query)]
        if images:
            return images[0]

        return DEFAULT_IMAGE

    def set_accessibility(self, v):
        self.accessibility = v

    def is_historical(self):
        return self.date < datetime.date.today()

    def to_dict(self):
        d = self.__dict__.copy()
        d['venue'] = d['venue'].to_dict()
        d['date'] = str(d['date'])
        if not d['accessibility']:
            d['accessibility'] = {}
        return d


@ch.attributes(['name', 'address', 'latitude', 'longitude', 'city', 'state',
                'postcode'])
class Venue(object):
    @classmethod
    def parse(cls, node):
        address, latitude, longitude = cls.parse_address(
            node.find('address'),
        )
        return Venue(
            name=_unquote(node.attrib['name'].strip()),
            address=address,
            latitude=latitude,
            longitude=longitude,
            city=node.find('city').text,
            state=node.find('state').text,
            postcode=node.find('postcode').text,
        )

    @staticmethod
    def parse_address(node):
        lines = [node.find('address1').text,
                 node.find('address2').text,
                 node.find('address3').text]
        lines = filter(None, lines)
        lat = node.find('latitude').text
        lon = node.find('longitude').text
        return lines, lat, lon

    def to_dict(self):
        return self.__dict__.copy()


def parse_date(d):
    return datetime.date(int(d[:4]), int(d[4:6]), int(d[6:8]))


def parse_events(input_file):
    with open(input_file) as istream:
        data = istream.read()

    root = ElementTree.fromstring(data)
    channel = root.getchildren()[0]

    events = []
    for node in channel.getchildren():
        if node.tag == 'item':
            events.append(Event.parse(node))

    return events


def _unquote(v):
    unescape_table = {
        '&quot;': '"',
        '&apos;': "'",
        '&#39;': "'",
        '&#233;': u'é',
        '&#232;': u'è',
        '&#246;': u'ö',
    }
    return unescape(urllib.unquote(v), unescape_table)


def _create_option_parser():
    usage = \
"""%prog [options] input_file.xml venues.json output_file.json

Turn the event feed into JSON."""  # nopep8

    parser = optparse.OptionParser(usage)

    return parser


def main(argv):
    parser = _create_option_parser()
    (options, args) = parser.parse_args(argv)

    if len(args) != 3:
        parser.print_help()
        sys.exit(1)

    build_event_json(*args)


if __name__ == '__main__':
    main(sys.argv[1:])
