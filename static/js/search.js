var searchResultTemplate = _.template($("#searchresult_template").html())
var ONE_DAY_IN_MS = 86400000
var MAX_LATLNG_DISTANCE = 1


$(function() {
  $(".search-form").submit(function() {
    from = $("#datasrc").attr("href")
    $.getJSON(from).then(function(data) {
      var container = $(".results-container .search-results")
      container.empty()
      _.each(_.filter(data, searchMatches), function(ev) {
        container.append(searchResultTemplate(ev))
      })
      $(".results-container").show()
      $(".search").hide()
    })
    return false
  })

  $("#back_to_search").on('click', function(){
    $(".results-container").hide()
    $(".search").show()
  })

})

function searchMatches(event) {
  var ok = true

  // Check location
  if ($("#location").val() === "Anywhere") {
    // Nothing to see here
  } else if ($("#location").val() === "Near me") {
    ok = ok && eventMatchesMyLocation(event)
  } else {
    throw "No idea what to do now..."
  }

  if ($("#access").val() !== "any") {
    if ($("#access").val() === "very") {
      ok = ok && event.accessibility.wheelchair === "yes"
    }
    if ($("#access").val() === "very") {
      ok = ok && event.accessibility.wheelchair === "yes"
    }
    if ($("#access").val() === "limited") {
      wc = event.accessibility.wheelchair
      ok = ok && ((wc === "yes") || (wc === "limited"))
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
    // Shortcut: We can skip pythagoras here since we're comparing to 1.
    return dx + dy < 0.06
  }
  return false;
}

