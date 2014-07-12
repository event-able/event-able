
events_rss.xml:
	# Argh, invalid ssl cert.
	wget -O events_rss.xml http://www.eventsvictoria.com/distributionservice/rss.xml

accessibility.csv:
	wget -X POST -O accessibility.csv "https://data.melbourne.vic.gov.au/api/views/INLINE/rows.csv?accessType=DOWNLOAD"
