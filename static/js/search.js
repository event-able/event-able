var searchResultTemplate = _.template($("#searchresult_template").html())
var ONE_DAY_IN_MS = 86400000
var MAX_LATLNG_DISTANCE = 1


$(function() {
  // Populate results container
  from = $("#datasrc").attr("href")
  loadData = $.getJSON(from)

  loadData.then(function(data) {
    var container = $(".results-container .search-results")
    _.each(data, function(ev) {
      container.append(searchResultTemplate(ev))
    })
  })

  var doSearch = function() {
    loadData.then(function(data) {
      _.each(data, function(ev) {
        if (searchMatches(ev)) {
          $("#event_" + ev.guid).show()
        } else {
          $("#event_" + ev.guid).hide()
        }
      })
      $(".results-container").show()
    })
    return false
  }
  $(".search-form").submit(doSearch)
  $(".search-form").change(function() { $(".results-container").hide()})
})

function searchMatches(event) {
  var ok = true

  // Check location
  if ($("#location").val() === "anywhere") {
    // Nothing to see here
  } else if ($("#location").val() === "near_me") {
    ok = ok && eventMatchesMyLocation(event)
  } else if ($("#location").val() === "melbourne") {
    ok = ok && ((event.venue.city === "Melbourne") || (event.venue.city === "Docklands") || (event.venue.city === "Southbank "))
  } else if ($("#location").val() === "northern") {
    ok = ok && ((event.venue.city === "Kensington") || (event.venue.city === "Ascot Vale") || (event.venue.city === "Flemington") || (event.venue.city === "Sunbury") || (event.venue.city === "Carlton" ) || (event.venue.city === "Greenvale") || (event.venue.city === "North Melbourne") || (event.venue.city === "Parkville") || (event.venue.city === "Carlton North") || (event.venue.city === "Keilor") || (event.venue.city === "Collingwood"))
  } else if ($("#location").val() === "eastern") {
    ok = ok && ((event.venue.city === "Mount Waverley") || (event.venue.city === "Brunswick") || (event.venue.city === "Brunswick East") || (event.venue.city === "Warrandyte") || (event.venue.city === "East Melbourne") || (event.venue.city === "Ivanhoe") || (event.venue.city === "Ivanhoe East") || (event.venue.city === "Richmond") || (event.venue.city === "Hawthorn") || (event.venue.city === "Box Hill") || (event.venue.city === "Malvern") || (event.venue.city === "Kooyong") || (event.venue.city ===  "Surrey Hills North") || (event.venue.city ===  "Surrey Hills") || (event.venue.city === "Kew") || (event.venue.city === "Box Hill"))
  } else if ($("#location").val() === "southern") {
    ok = ok && ((event.venue.city === "South Melbourne") || (event.venue.city === "St Kilda") || (event.venue.city === "Moorabbin") || (event.venue.city === "Mordialloc") || (event.venue.city === "Bentleigh East") || (event.venue.city === "Springvale") || (event.venue.city === "Port Melbourne") || (event.venue.city === "Albert Park") || (event.venue.city === "Cheltenham East") || (event.venue.city === "Cheltenham") || (event.venue.city === "Clayton South") || (event.venue.city === "Clayton") || (event.venue.city === "Dandenong"))
  } else if ($("#location").val() === "western") {
    ok = ok && ((event.venue.city === "Williamstown") || (event.venue.city === "Bacchus Marsh") || (event.venue.city === "Laverton") || (event.venue.city === "Werribee South") || (event.venue.city === "Werribee"))
  }

  // Check accessibility
  if ($("#access").val() !== "any") {
    user_rating = event.accessibility.acc_user_rating
    official_rating = event.accessibility.acc_official_rating

    very_accessible = (user_rating === "yes") || (official_rating > 2)
    somewhat_accessible = (user_rating === "limited") || (official_rating > 1)

    if ($("#access").val() === "very") {
      ok = ok && very_accessible
    }
    if ($("#access").val() === "limited") {
      ok = ok && (somewhat_accessible || very_accessible)
    }
  }

  // Check cost
  if ($("#cost").val() != "any") {
    ok = ok && ($("#cost").val() === "free") === (event.isfree === "true")
  }

  // Check date :-(
  if ($("#date").val() != "any") {
    window.today = new Date()
    window.date = parseDate(event.date)
    days_apart = (date - today) / ONE_DAY_IN_MS

    if (days_apart < -1) {
      return false; // Happened in the past
    }

    if ($("#date").val() === "today") {
      ok = ok && days_apart < 1
    }

    if ($("#date").val() === "soon") {
      ok = ok && days_apart < 4
    }

    if ($("#date").val() === "later") {
      ok = ok && days_apart < 14
    }
  }
  return ok
}

// Javascript dates: literally the worst.
function parseDate(input) {
  var parts = input.split('-');
  // Note: months are 0-based but years and days are not.
  return new Date(parts[0], parts[1]-1, parts[2]);
}

function eventMatchesMyLocation(event) {
  if (window.latlng) {
    var dx = Math.abs(parseFloat(event.venue.latitude) - window.latlng[0])
    var dy = Math.abs(parseFloat(event.venue.longitude) - window.latlng[1])
    return Math.pow(dx, 2) + Math.pow(dy, 2) < 0.0001
  }
  return false;
}
