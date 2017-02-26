var luftdaten_storage = {
  default_center: [10.447683333333, 51.163375],
  default_zoom: 6
};

$( document ).ready(function() {
  if ($('#sensor-settings-map').length) {
    mapboxgl.accessToken = luftdaten_config.mapbox_token;
    if ($('#lat').val() && $('#lon').val()) {
      luftdaten_storage.default_center = [$('#lon').val(), $('#lat').val()];
      luftdaten_storage.default_zoom = 15;
    }
    luftdaten_storage.geojson = {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": luftdaten_storage.default_center
          }
        }
      ]
    };
    init_map('mapbox://styles/mapbox/streets-v9', luftdaten_storage.default_center, luftdaten_storage.default_zoom);
    
    luftdaten_storage.is_cursor_over_point = false;
    luftdaten_storage.is_dragging = false;
    luftdaten_storage.canvas = luftdaten_storage.map.getCanvasContainer();
    
    $('#sensor-setting-switch-style').click(function() {
      center = luftdaten_storage.map.getCenter();
      center = [center.lng, center.lat];
      zoom = luftdaten_storage.map.getZoom();
      luftdaten_storage.map.remove();
      if ($('#sensor-setting-switch-style').attr('data-style') == 'streets') {
        init_map('mapbox://styles/mapbox/satellite-streets-v9', center, zoom);
        $('#sensor-setting-switch-style').attr({'data-style': 'satellite'});
        $('#sensor-setting-switch-style').text('Straßen-Karte');
      }
      else {
        init_map('mapbox://styles/mapbox/streets-v9', center, zoom);
        $('#sensor-setting-switch-style').attr({'data-style': 'streets'});
        $('#sensor-setting-switch-style').text('Satelliten-Karte');
      }
    });
    $('#sensor-setting-use-address').click(function() {
      var location_string = $('#street_name').val();
      location_string += ' ' + $('#street_number').val();
      location_string += ', ' + $('#postalcode').val();
      location_string += ' ' + $('#city').val();
      geocode_url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/' + location_string+ '.json?access_token=' + luftdaten_config.mapbox_token;
      $.getJSON(geocode_url, function(data) {
        if (data.features.length) {
          luftdaten_storage.geojson.features[0].geometry.coordinates = data.features[0].center;
          luftdaten_storage.map.getSource('point').setData(luftdaten_storage.geojson);
          $('#lat').val(data.features[0].center[1]);
          $('#lon').val(data.features[0].center[0]);
          luftdaten_storage.map.flyTo({
            center: data.features[0].center,
            zoom: 17
          });
        }
      });
    });
    /*
    $('#sensor-setting-form').submit(function(event) {
      event.preventDefault();
      if (!$('#lat').val() || !$('#lon').val()) {
        if($('#city').val()) {
          var location_string = $('#street_name').val();
          location_string += ' ' + $('#street_number').val();
          location_string += ', ' + $('#postalcode').val();
          location_string += ' ' + $('#city').val();
          geocode_url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/' + location_string+ '.json?access_token=' + luftdaten_config.mapbox_token;
          $.getJSON(geocode_url, function(data) {
            if (data.features.length) {
              $('#lat').val(data.features[0].center[1]);
              $('#lon').val(data.features[0].center[0]);
            }
            $('#sensor-setting-form').trigger('submit');
          });
        }
        else {
          $('#sensor-setting-form').trigger('submit');
        }
      }
      else {
        $('#sensor-setting-form').trigger('submit');
      }
    });*/
  }
});


function init_map(style, center, zoom) {
  luftdaten_storage.map = new mapboxgl.Map({
    container: 'sensor-settings-map',
    style: style,
    center: center,
    zoom: zoom
  });
  luftdaten_storage.map.on('load', on_load);
}

function on_load() {
  if ($('#lat').val() && $('#lon').val())
    luftdaten_storage.geojson.features[0].geometry.coordinates = [$('#lon').val(), $('#lat').val()];
  else
    luftdaten_storage.geojson.features[0].geometry.coordinates = luftdaten_storage.default_center;
  
  luftdaten_storage.map.addSource('point', {
    type: "geojson",
    data: luftdaten_storage.geojson
  });
  
  luftdaten_storage.map.addLayer({
    "id": "point",
    "type": "circle",
    "source": "point",
    "paint": {
      "circle-radius": 10,
      "circle-color": "#3887be"
    }
  });
  luftdaten_storage.map.on('mousemove', on_mousemove);
  
  luftdaten_storage.map.on('mousedown', on_mousedown, true);
}

function on_mousemove(e) {
  var features = luftdaten_storage.map.queryRenderedFeatures(e.point, { layers: ['point'] });
  if (features.length) {
    luftdaten_storage.map.setPaintProperty('point', 'circle-color', '#3bb2d0');
    luftdaten_storage.canvas.style.cursor = 'move';
    luftdaten_storage.is_cursor_over_point = true;
    luftdaten_storage.map.dragPan.disable();
  }
  else {
    luftdaten_storage.map.setPaintProperty('point', 'circle-color', '#3887be');
    luftdaten_storage.canvas.style.cursor = '';
    luftdaten_storage.is_cursor_over_point = false;
    luftdaten_storage.map.dragPan.enable();
  }
}

function on_move(e) {
  if (!luftdaten_storage.is_dragging)
    return;
  var coords = e.lngLat;
  luftdaten_storage.canvas.style.cursor = 'grabbing';
  luftdaten_storage.geojson.features[0].geometry.coordinates = [coords.lng, coords.lat];
  luftdaten_storage.map.getSource('point').setData(luftdaten_storage.geojson);
}

function on_mousedown() {
  if (!luftdaten_storage.is_cursor_over_point)
    return;

  luftdaten_storage.is_dragging = true;
  luftdaten_storage.canvas.style.cursor = 'grab';
  luftdaten_storage.map.on('mousemove', on_move);
  luftdaten_storage.map.once('mouseup', on_up);
}

function on_up(e) {
  if (!luftdaten_storage.is_dragging)
    return;
  var coords = e.lngLat;
  $('#lat').val(coords.lat);
  $('#lon').val(coords.lng);
  luftdaten_storage.is_dragging = false;
  luftdaten_storage.map.off('mousemove', on_move);
}
