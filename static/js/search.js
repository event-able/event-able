var searchResultTemplate = _.template($("#searchresult_template").html())

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

  if ($("#location").val() === "Near me") {
    ok = ok && eventMatchesMyLocation(event)
  } else {
    throw "No idea what to do now..."
  }
  if ($("#category").val() != "any") {
    ok = ok && $("#category").val() === event.category
  }
  // if ($("#data").val() != "any") {
  //   today = new Date()
  //   date = parseDate(event.when)
  //   if ($("#data").val() === "today") {
  //     today.getDate()
  //     today.getMonth()
  //   }

  //   ok = ok && $("#date").val() === parseDate(event.when)

  // }
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

