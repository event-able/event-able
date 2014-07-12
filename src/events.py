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

import json

from xml.etree import ElementTree
import characteristic as ch


def build_event_json(input_file, output_file):
    events = parse_events(input_file)

    dicts = [e.to_dict() for e in events
             if not e.is_historical()]

    with open(output_file, 'w') as ostream:
        json.dump(dicts, ostream)


@ch.attributes(['guid', 'link', 'category', 'title', 'description',
                'region', 'venue', 'isfree', 'date', 'tags'])
class Event(object):
    @staticmethod
    def parse(node):
        return Event(
            guid=node.find('guid').text,
            link=node.find('link').text,
            category=node.find('category').text,
            title=node.find('title').text,
            description=node.find('description').text,
            region=node.find('{myEvents}marketingRegion').text,
            venue=Venue.parse(node.find('{myEvents}venue')),
            isfree=node.find('{myEvents}freeEntry').text,
            date=parse_date(node.find('{myEvents}eventDate').text),
            tags=[t.text for t in node.findall('{myEvents}tags')],
        )

    def is_historical(self):
        return self.date < datetime.date.today()

    def to_dict(self):
        d = self.__dict__.copy()
        d['venue'] = d['venue'].to_dict()
        d['date'] = str(d['date'])
        return d


@ch.attributes(['address', 'area', 'suburb', 'city', 'state', 'postcode'])
class Venue(object):
    @staticmethod
    def parse(node):
        return Venue(
            address=[l.text for l in node.findall('address')],
            area=node.find('area').text,
            suburb=node.find('suburb').text,
            city=node.find('city').text,
            state=node.find('state').text,
            postcode=node.find('postcode').text,
        )

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


def _create_option_parser():
    usage = \
"""%prog [options] input_file.xml output_file.json

Turn the event feed into JSON."""  # nopep8

    parser = optparse.OptionParser(usage)

    return parser


def main(argv):
    parser = _create_option_parser()
    (options, args) = parser.parse_args(argv)

    if len(args) != 2:
        parser.print_help()
        sys.exit(1)

    build_event_json(*args)


if __name__ == '__main__':
    main(sys.argv[1:])
