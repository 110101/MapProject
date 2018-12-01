
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
	
	var tilelayer = new L.StamenTileLayer("terrain");
	tilelayer.options.maxZoom = 20;
	tilelayer.options.minZoom = 1; //12

	map = new L.Map('map').setView([defaultlat, defaultlong], 12);

	// create the tile layer with correct attribution
	//var osmUrl='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	//var osmAttrib='Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors / 110101';
	//var osm = new L.TileLayer(osmUrl, {minZoom: 3, maxZoom: 18, attribution: osmAttrib, subdomains: ['a','b']});		
	//map.addLayer(osm);
	function setColor(d){
		return d > 90 ? '#06f6c6' :
			   d > 80 ? '#0debc8' :
			   d > 70 ? '#14e1cc' :
			   d > 60 ? '#1bd5ce' :
			   d > 50 ? '#24c9d2' :
			   d > 40 ? '#2dbcd5' :
			   d > 30 ? '#34b1d7' :
			   d > 20 ? '#3da5da' :
			   d > 10 ? '#4795de' :
			            '#3e88d4' ;
		}
	
	function setFillOpac (d){
		return d > 50 ? '0.9' :
			   d > 30 ? '0.9' :
						'0.6' ;
	}


	function style(feature){
		return {
		fillColor: setColor(feature.properties.calcindex), //'#786590',
		weight: 0,
        opacity: 0,
        fillOpacity: setFillOpac(feature.properties.calcindex)
    	};
	}

	/* bisher keine Verwendung */
	// var city = cities;

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

// Wenn zu weit rausgezoomt wird Kreis bei Stadt anzeigen
//map.on('zoomout', onMoveStart);
