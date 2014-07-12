
function onLocationAvailable(position) {
  var latitude = position.coords.latitude;
  var longitude = position.coords.longitude;
  $(function() {
    window.latlng = [latitude, longitude]
    $("#location").val("My Location")
  })
}

navigator.geolocation.getCurrentPosition(onLocationAvailable)
