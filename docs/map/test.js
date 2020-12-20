var gsi_map;
var point_layer;

function add_gsi_layer() {
  var pale = new L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
      attribution:
        '© <a href="http://osm.org/copyright">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
    }
  );
  pale.addTo(gsi_map);
}

function onEachFeature(feature, layer) {
  let p = feature.properties;
  let content =
    '<p class="iw">[ <a href="' +
    p.url +
    '">' +
    p.id +
    "</a> ]<br/>地名" +
    p.name +
    "<br/>分類" +
    p.type +
    "</p>";
  layer.bindPopup(content);
}

function pointToLayer(feature, latlng) {
  let p = feature.properties;
  let icon = new L.Icon({
    iconUrl: "http://codh.rois.ac.jp/edo-maps/icons/" + p.icon,
    iconSize: [22, 33],
    iconAnchor: [11, 33],
    popupAnchor: [0, -25],
  });
  return L.marker(latlng, { icon: icon });
}

function add_point_layer() {
  var point_layer = L.featureGroup();
  point_layer.addTo(gsi_map);

  point_layer.on("layeradd", function () {
    gsi_map.fitBounds(point_layer.getBounds());
  });

  jsonUrl.forEach((j) => {
    $.getJSON(j, function (data) {
      let layer = L.geoJSON(data, {
        onEachFeature: onEachFeature,
        pointToLayer: pointToLayer,
      }).addTo(point_layer);
    });
  });
}

function add_mapwarper_layer() {
  tileUrl.forEach((t) => {
    L.tileLayer(t, {
      attribution:
        'Tiles by <a href="https://mapwarper.h-gis.jp/users/234/">Map Warper user Nakamura</a>',
      opacity: 0.8,
      //maxZoom: 17,
      //minZoom: 14
    }).addTo(gsi_map);
  });
}

function init() {
  console.log("init");
  gsi_map = L.map("map");
  gsi_map.zoomControl.setPosition("topleft");

  add_gsi_layer();
  add_mapwarper_layer();
  add_point_layer();
}

onload = init;
