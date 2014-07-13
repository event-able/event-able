
function onLocationAvailable(position) {
  var latitude = position.coords.latitude;
  var longitude = position.coords.longitude;
  $(function() {
    window.latlng = [latitude, longitude]
    $("#location").val("Near me")
  })
}

navigator.geolocation.getCurrentPosition(onLocationAvailable)
