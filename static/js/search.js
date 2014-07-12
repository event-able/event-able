var searchResultTemplate = _.template($("#searchresult_template").html())

$(function() {
  $(".search-form").submit(function() {
    from = $("#datasrc").attr("href")
    $.getJSON(from).then(function(data) {
      var container = $(".results-container .search-results")
      container.empty()
      _.each(data, function(ev) {
        if (Math.random() > 0.9) {
          container.append(searchResultTemplate(ev))
        }
      })
      $(".results-container").show()
    })
    return false
  })
})
