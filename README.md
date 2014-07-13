# event-able

Melbourne is a fantastic city, with rich cultural events happening every day of the week. Eventable makes discovering upcoming events easier, and annotates events with access information for people with limited mobility. It combines official accessibility data with crowd-sourced user ratings, providing a quick method for people to share their own experiences with venues.

## For comparison

- [That's Melbourne: Major Events](http://www.thatsmelbourne.com.au/Whatson/MajorEvents/Pages/MajorEvents.aspx)
- [City of Melbourne: Accessible amenities](http://www.melbourne.vic.gov.au/CommunityServices/DisabilityServices/AccessibleAmenities/Pages/AccessibleAmenities.aspx)

## Developing

Run `make build` to generate the static HTML, then `make serve` to start a local development server.

Add static files to the `static/` folder, and refer to them in `/static/` on the site. For HTML add to the `templates/` folder which uses Jinja2 syntax.

