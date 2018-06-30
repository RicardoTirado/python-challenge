var mymap = L.map('map').setView([30, 0], 3);

mymap.options.minZoom = 3;
mymap.options.maxZoom = 8;


L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    noWrap: true,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.satellite',
    accessToken: 'pk.eyJ1Ijoic2luYW5jZW5naXoiLCJhIjoiY2ppZHVwMXZnMGZqaTNxcWw0NWxhN3YwNSJ9.RVV5UmzSmoeu4xd1Wh4iHA'
}).addTo(mymap);

var southWest = L.latLng(-89.98155760646617, -190),
northEast = L.latLng(89.99346179538875, 190);
var bounds = L.latLngBounds(southWest, northEast);

mymap.setMaxBounds(bounds);
mymap.on('drag', function() {
    mymap.panInsideBounds(bounds, { animate: false });
});

var url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson";

d3.json(url, function(data) {
    useData(data);
    console.log(data)
});
function getColor(d) {
    return d > 5 ? '#800026' :
           d > 4.5  ? '#BD0026' :
           d > 4  ? '#E31A1C' :
           d > 3.5  ? '#FC4E2A' :
           d > 3   ? '#FD8D3C' :
           d > 2   ? '#FEB24C' :
           d > 1   ? '#FED976' :
                      '#FFEDA0';
}

function createCircleMarker( feature, latlng ){
    // Change the values of these options to change the symbol's appearance
    console.log(latlng);
    console.log(feature);
    var mag = feature.properties.mag;

    var options = {
        
      radius:(feature.properties.mag) * 5,
      fillColor:getColor(feature.properties.mag),
      color: 'white',
      weight: 1,
      opacity: 1,
      fillOpacity: 0.7
    }


    return L.circleMarker( latlng, options ).bindPopup("<h1> Place : " + feature.properties.place + "</h1> <hr> <h3>Magnitude : " + feature.properties.mag + "</h3>");
  }

function useData(newData){
    
   geojson =  L.geoJson(newData,{
        pointToLayer: createCircleMarker 
    }).addTo(mymap)

 }
   
var info = L.control();

info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.update();
    return this._div;
};

info.update = function (props) {
    this._div.innerHTML = '<h4>World Earthquake Map</h4>' +  (props ?
        '<b>' + props.mag + '</b><br />' + props.mag + ' people / mi<sup>2</sup>'
        : 'Click on a Circle to See Details');
};

info.addTo(mymap);


var legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 1, 2, 3, 3.5, 4, 4.5, 5],
        labels = [];

    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] +' Mag'+ '<br>' : '+');
    }

    return div;
};

legend.addTo(mymap);
