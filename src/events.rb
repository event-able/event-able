require 'nokogiri'
require 'rest-client'
require './src/cache'

api_base = "http://api.openstreetmap.org/api/0.6/map?bbox="
bbox_sizing = 0.002

cache = ResponseCache.new

e = Nokogiri::XML(File.read( 'data/events_rss.xml' ));
e.remove_namespaces!

e.css("item").each do |item|
  name = item.css("venue").attr("name").to_s.strip
  lat = item.css("latitude").text.to_f.round(3)
  lng = item.css("longitude").text.to_f.round(3)

  query = [
    format("%.3f", lng-bbox_sizing),
    format("%.3f", lat-bbox_sizing),
    format("%.3f", lng+bbox_sizing),
    format("%.3f", lat+bbox_sizing)
  ].join(",")

  nodes = Nokogiri::XML cache.fetch(name, api_base + query)
  matching_name_nodes = nodes.css("tag[k='name'][v='#{name}']")
  ids = matching_name_nodes.map {|n| n.parent.attr "id" }
  if ids.count > 1
    # TODO: Actually fetch each ID to remove bad matches.
    puts "Ambiguity matching #{name}: The following IDs match: #{ids.join " "}"
  elsif ids.count == 1
    puts "#{name}: http://wheelmap.org/en/nodes/#{ids.first}"
  else
    puts "No match for '#{name}'"
    # buildings = nodes.css("tag[k='building']").map(&:parent)
    # names = buildings.map {|b| b.css("tag[k='name']").first.attr 'v' rescue nil}.compact.sort
    # names.each do |name|
    #   puts " * #{name}"
    # end
  end
end
