help:
	@echo 'Things you can do with this codebase:'
	@echo
	@echo '  make data    download all data sources'
	@echo '  make build   make html output'
	@echo '  make env     install sandboxed python dependencies'
	@echo '  make serve   run a local development server'
	@echo '  make watch   watch and rebuild on any changes'
	@echo '  make deploy  deploy current build to S3'
	@echo

DEST_BUCKET = s3://eventable.in/
TODAY = $(shell date +%Y-%m-%d)

data: \
	data/events-$(TODAY).xml \
	data/accessibility.json \
	static/data/melbourne.json \
	data/osm/events.list \
	data/osm/wheelchair.json \
	data/missing-wheelmap.txt \

data/events-$(TODAY).xml:
	wget -O $@ http://www.eventsvictoria.com/distributionservice/rss.xml

data/accessibility.json:
	wget -O $@ 'http://data.melbourne.vic.gov.au/resource/pmhb-s6pn.json'

static/data/melbourne.json: env data/events-$(TODAY).xml data/osm/wheelchair.json src/events.py
	mkdir -p static/data
	env/bin/python src/events.py data/events-$(TODAY).xml data/osm/wheelchair.json static/data

data/osm/events.list:
	# This one is *slow*
	bundle exec ruby src/events.rb | grep http > events.list | sort | uniq > events2.list

data/osm/wheelchair.json: data/osm/events.list src/wheelmap.py
	env/bin/python src/wheelmap.py data/osm/events.list $@

data/missing-wheelmap.txt: static/data/melbourne.json src/missing_wheelmap.py
	env/bin/python src/missing_wheelmap.py static/data/melbourne.json >$@

env: requirements.pip
	virtualenv env
	env/bin/pip install -r requirements.pip

build: env src/build.py static/data/melbourne.json
	env/bin/python src/build.py

watch: env
	env/bin/watchmedo shell-command --interval 2 --wait -c "make build" -R static templates

serve: build
	cd output; python -m SimpleHTTPServer

.s3cfg: env
	test -f .s3cfg || env/bin/s3cmd --configure -c .s3cfg

deploy: build .s3cfg
	env/bin/s3cmd sync -c .s3cfg --acl-public --recursive --delete-removed --exclude='*/.*' output/ $(DEST_BUCKET)

.PHONY: data build serve

.DELETE_ON_ERROR:

