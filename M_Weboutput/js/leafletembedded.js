
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

	var tilelayer = new L.StamenTileLayer("toner-lite");
	tilelayer.options.maxZoom = 17;
	tilelayer.options.minZoom = 11; //12

	map = new L.Map('map').setView([defaultlat, defaultlong], 12);

	// create the tile layer with correct attribution
	//var osmUrl='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	//var osmAttrib='Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors / 110101';
	//var osm = new L.TileLayer(osmUrl, {minZoom: 3, maxZoom: 18, attribution: osmAttrib, subdomains: ['a','b']});
	//map.addLayer(osm);
	function setColor(d){
		return d > 95 ? '#00fecc' :
					d > 90 ? '#03f6ca':
					d > 85 ? '#06efc9':
			    d > 80 ? '#09e8c9' :
					d > 75 ? '#0ddec7':
			    d > 70 ? '#0fd8c7' :
					d > 65 ? '#12d0c6':
			    d > 60 ? '#14c9c5' :
					d > 55 ? '#17c1c4':
			    d > 50 ? '#1bb9c3' :
					d > 45 ? '#1db0c2':
			    d > 40 ? '#21a9c1' :
					d > 35 ? '#249fbf':
			    d > 30 ? '#2799be' :
					d > 25 ? '#2a90bd':
			    d > 20 ? '#2c8abc' :
					d > 15 ? '#2f83bb':
			    d > 10 ? '#317dbb' :
					d > 5  ? '#327aba':
			            '#3476ba' ;
		}

	function setFillOpac (d){
		return d > 90 ? '0.90' :
					 d > 50 ? '0.80':
					 d > 30 ? '0.75':
					 d > 25 ? '0.65':
					 d > 20 ? '0.50':
					 d > 15 ? '0.40':
					 d > 10 ? '0.30':
					 d > 5  ? '0.15':
					 d > 0  ? '0.05':
						'0.4' ;
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
