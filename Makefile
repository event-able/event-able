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
	static/data/events.json \

data/events_rss.xml:
	wget -O $@ http://www.eventsvictoria.com/distributionservice/rss.xml

data/accessibility.json:
	wget -O $@ 'http://data.melbourne.vic.gov.au/resource/pmhb-s6pn.json'

static/data/events.json: env data/events_rss.xml src/events.py
	mkdir -p static/data
	env/bin/python src/events.py data/events_rss.xml $@

env: requirements.pip
	virtualenv env
	env/bin/pip install -r requirements.pip

build: env src/build.py static/data/events.json
	env/bin/python src/build.py

serve: build
	cd output; python -m SimpleHTTPServer

.PHONY: data build serve

.DELETE_ON_ERROR:
