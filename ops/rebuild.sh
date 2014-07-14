#!/bin/bash
#
#  rebuild.sh
#

cd /root/event-able

# remove previous day's data
make clean

# fetch data, rebuild data + site, deploy
make deploy
