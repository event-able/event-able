function onLocationAvailable(position) {
  var latitude = position.coords.latitude;
  var longitude = position.coords.longitude;
  $(function() {
    window.latlng = [latitude, longitude]
    $("#location [value='near_me']").attr('disabled', false)
    $("#location").val("near_me")
  })
}


$(function() {
  $("#location").val("anywhere")
})
navigator.geolocation.getCurrentPosition(onLocationAvailable)
