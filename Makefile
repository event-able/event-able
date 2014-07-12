
data/events_rss.xml:
	# Argh, invalid ssl cert.
	wget -O events_rss.xml http://www.eventsvictoria.com/distributionservice/rss.xml

data/accessibility.json:
	wget -O accessibility.json 'http://data.melbourne.vic.gov.au/resource/pmhb-s6pn.json'
