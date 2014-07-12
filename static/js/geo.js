
function onLocationAvailable(position) {
  var latitude = position.coords.latitude;
  var longitude = position.coords.longitude;
  $(function() {
    // Figure out what happens now...
    console.log(latitude);
    console.log(longitude);
  })
}

navigator.geolocation.getCurrentPosition(onLocationAvailable)
