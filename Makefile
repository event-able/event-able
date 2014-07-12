help:
	@echo 'Things you can do with this codebase:'
	@echo
	@echo '  make data    download all data sources'
	@echo '  make build   make html output'
	@echo '  make env     install sandboxed python dependencies'
	@echo '  make serve   run a local development server'
	@echo

data: \
	data/events_rss.xml \
	data/accessibility.json \

data/events_rss.xml:
	wget -O $@ http://www.eventsvictoria.com/distributionservice/rss.xml

data/accessibility.json:
	wget -O $@ 'http://data.melbourne.vic.gov.au/resource/pmhb-s6pn.json'

env:
	virtualenv env
	env/bin/pip install -r requirements.pip

build: env
	env/bin/python src/build.py

serve: build
	cd output; python -m SimpleHTTPServer

.PHONY: data build serve

.DELETE_ON_ERROR:

data/map.osm:
	wget -O $@ "http://www.openstreetmap.org/api/0.6/map?bbox=144.94258403778073,-37.82178544741225,144.97863292694092,-37.808529446909795"
