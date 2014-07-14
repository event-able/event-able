#!/bin/bash
#
#  bootstrap.sh
#
#  Sets up all necessary dependencies on Ubuntu 14.04.
#

set -e
set -x

sudo apt-get install -y \
  python-dev \
  python-pip \
  python-virtualenv \
  build-essential \

