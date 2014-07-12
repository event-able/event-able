help:
	@echo 'Things you can do with this codebase:'
	@echo
	@echo '  make data    download all data sources'
	@echo

data: \
	data/events_rss.xml \
	data/accessibility.json \

data/events_rss.xml:
	wget -O $@ http://www.eventsvictoria.com/distributionservice/rss.xml

data/accessibility.json:
	wget -O $@ 'http://data.melbourne.vic.gov.au/resource/pmhb-s6pn.json'

.PHONY: data

.DELETE_ON_ERROR:
