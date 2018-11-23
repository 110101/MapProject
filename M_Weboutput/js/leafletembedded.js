
var map;
var ajaxRequest;
var plotlist;
var plotlayers=[];
var defaultlat = 48.149889;
var defaultlong = 11.585537;

	function onMoveStart(e){
		map.stopLocate();
		alert('locate stop')
	};

function initmap(){
	
	var tilelayer = new L.StamenTileLayer("toner");
	tilelayer.options.maxZoom = 20;
	tilelayer.options.minZoom = 1; //12

	map = new L.Map('map').setView([defaultlat, defaultlong], 12);

	// create the tile layer with correct attribution
	//var osmUrl='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	//var osmAttrib='Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors / 110101';
	//var osm = new L.TileLayer(osmUrl, {minZoom: 3, maxZoom: 18, attribution: osmAttrib, subdomains: ['a','b']});		
	//map.addLayer(osm);
	function setColor(d){
		return d > 90 ? '#a50026' :
			   d > 80 ? '#d73027' :
			   d > 70 ? '#f46d43' :
			   d > 60 ? '#f46d43' :
			   d > 50 ? '#fdae61' :
			   d > 40 ? '#fee08b' :
			   d > 30 ? '#d9ef8b' :
			   d > 10 ? '#a6d96a' :
			            '#e0e0e0' ;
		}
	
	function setFillOpac (d){
		return d > 10 ? '0.7' :
						'0.4' ;
	}


	function style(feature){
		return {
		fillColor: setColor(feature.properties.index), //'#786590',
		weight: 0,
        opacity: 0,
        fillOpacity: setFillOpac(feature.properties.index)
    	};
	}

	/* bisher keine Verwendung */
	var city = cities;

	/* Grid aus geoJson auf Karte legen */
	L.geoJson(city_grid, {style: style}).addTo(map);
	map.addLayer(tilelayer);
	
	//map.on('click', viewPos);


}

function locate_user(){
	map.locate({watch: true, setView: false, maxZoom: 18, maximumAge: 2000, enableHighAccuracy: true})
	//map.locate()

	function onLocationFound(e){
		var radius = e.accuracy / 2;
		var heading = e.accuracy;
		var timestamp_act = e.timestamp;

		map.setView(e.latlng, 18);
		L.circle(e.latlng, radius).addTo(map);

		/* L.marker(e.latlng).addTo(map) 
        .bindPopup("You are within " + heading + " meters from this point").openPopup(); */
        //map.on('movestart', onMoveStart);
	}
	map.on('locationfound', onLocationFound);

}

function viewPos(e){
	var location = e.latlng;
	alert(location[1]);
}

map.on('zoomout', onMoveStart);
