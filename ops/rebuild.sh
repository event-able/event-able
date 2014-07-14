#!/bin/bash
#
#  rebuild.sh
#

set -e
set -x

cd /root/event-able

# update the code
git fetch
git reset --hard origin/master

# remove previous day's data
make clean

# fetch data, rebuild data + site, deploy
make deploy
