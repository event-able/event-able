
function onLocationAvailable(position) {
  var latitude = position.coords.latitude;
  var longitude = position.coords.longitude;
  $(function() {
    window.latlng = [latitude, longitude]
    $("#location").val("Near me")
  })
}

$("#location").val("anywhere")
navigator.geolocation.getCurrentPosition(onLocationAvailable)
