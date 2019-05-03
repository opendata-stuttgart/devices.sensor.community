var luftdaten_storage = {
    default_center: [51.163375, 10.44768333333],
    default_zoom: 2
};

$( document ).ready(function() {
    if ($('#sensor-settings-map').length) {
        if ($('#location-latitude').val() == "" || $('#location-latitude').val() == "") {
            var mapCenter = luftdaten_storage.default_center;
        } else {
            var mapCenter = [$('#location-latitude').val(), $('#location-longitude').val()];
        }

      L.Icon.Default.imagePath = '/static/images/leaflet/';
        var map = L.map('sensor-settings-map', {center: mapCenter, zoom: luftdaten_storage.default_zoom});
        L.tileLayer('https://maps.luftdaten.info/tiles/{z}/{x}/{y}.png', {
            maxZoom: 18,
            attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
            '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
            id: 'examples.map-i875mjb7',
            noWrap: true
        }).addTo(map);
        var marker = L.marker(mapCenter).addTo(map);
        var updateMarker = function (lat, lng) {
            marker
                .setLatLng([lat, lng])
                .bindPopup("Your location :  " + marker.getLatLng().toString())
                .openPopup();
            return false;
        };

        map.on('click', function (e) {
            $('#location-latitude').val(e.latlng.lat);
            $('#location-longitude').val(e.latlng.lng);
            updateMarker(e.latlng.lat, e.latlng.lng);
        });

        function geocode_lookup() {
            var geocode = 'https://nominatim.openstreetmap.org/search'

            var location_string = $('#location-street_name').val();
            location_string += ' ' + $('#location-street_number').val();
            location_string += ', ' + $('#location-postalcode').val();
            location_string += ' ' + $('#location-city').val();

            $.getJSON(geocode, {
                'format': 'json',
                'limit': 1,
                'q': location_string
            }, function (data) {
                // get lat + lon from first match
                var latlng = [data[0].lat, data[0].lon];
                console.log(latlng);
                $('#location-latitude').val(data[0].lat);
                $('#location-longitude').val(data[0].lon);
                map.setView({lat: $('#location-latitude').val(), lng: $('#location-longitude').val()}, 18);
                updateMarker($('#location-latitude').val(), $('#location-longitude').val());
            });
        }

        $("#sensor-setting-use-address").click(function() {
            geocode_lookup();
        })
    }
});
