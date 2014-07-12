# -*- coding: utf-8 -*-
#
#  build.py
#  event-able
#

from __future__ import absolute_import, print_function, division

import os
from os import path

import sh
import jinja2

TEMPLATE_DIR = path.join(path.dirname(__file__), '..', 'templates')
OUTPUT_DIR = path.join(path.dirname(__file__), '..', 'output')


def build():
    copy_statics()
    build_templates()


def copy_statics():
    if path.isdir('output/static'):
        sh.rm('-rf', 'output/static')

    if not path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    sh.cp('-r', 'static', 'output/static')


def build_templates():
    base = path.abspath(TEMPLATE_DIR)
    for prefix, dirnames, filenames in os.walk(base):
        # ignore _ prefixed stuff
        dirnames[:] = [d for d in dirnames if not d.startswith('_')]
        filenames[:] = [f for f in filenames if not f.startswith('_')]

        for f in filenames:
            input_file = path.join(prefix[len(base) + 1:], f)
            output_file = path.join(OUTPUT_DIR, input_file)

            parent_dir = path.dirname(output_file)
            if not path.isdir(parent_dir):
                os.mkdir(parent_dir)

        gen_script(input_file, output_file, data={})


def gen_script(template_file, output_file, data=None):
    "Render a Jinja template for the given script to the given file."
    data = data or {}
    loader = jinja2.FileSystemLoader(TEMPLATE_DIR)
    env = jinja2.Environment(loader=loader, undefined=jinja2.StrictUndefined)
    template = env.get_template(template_file)

    with open(output_file, 'w') as ostream:
        ostream.write(template.render(**data))


if __name__ == '__main__':
    build()
