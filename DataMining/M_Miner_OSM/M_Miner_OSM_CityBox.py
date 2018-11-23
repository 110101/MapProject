import csv
import requests

#eigentlich Teil von Dataprocessing
#Citybox wird als Input für Dataprocessing benötigt
#Synergie mit OSM Miner nur weil CityBox aus Kartendaten kommen
#Abfrage eigentlich nur 1 mal notwendig

def osm_querry_config():
    querrys = []
    keywords = []
   # with open("/M_Miner_OSM/config_miner_source_osm.csv", "r") as configfile:
        #userFileReader = csv.DictReader(configfile)

   # for query_row in userFileReader:
    #setup querry for overpass api
    osm_id_convert = 3600000000
    city_id = 62428 #int(query_row['osm_area_id'])
    #query_string = '"' + query_row['key_string'] + '"="' + query_row['key_value'] + '"'


    overpass_query = """
        [out:json][timeout:300];
        area(""" + str(osm_id_convert+city_id) + """)->.searchArea;
        (
        rel['admin_level'='6'](area.searchArea);
        );
        out body bb;"""
    querrys.append(overpass_query)
    #keywords.append(query_string)
    #configfile.close()
    return overpass_query, keywords


def osm_querry(query_request, query_keyword):
            overpass_url = "https://overpass-api.de/api/interpreter"
            response = requests.get(overpass_url,params={'data':query_request})

            if response.status_code == 200:
                query_results = response.json()

                # processing for ingest
                query_source = query_results['generator']
                query_data = query_results['elements']

                #create log file
                log_type = "success"

                return [query_source, query_data, log_type]
            elif response.status_code != 200:

                # creat log file
                log_type = "err"

                return ["empty", "none", log_type]


def osm_get_citybox():
    query_input, query_keywords = osm_querry_config()

    query_output = osm_querry(query_input, query_keywords)
    query_output_data = query_output[1]

    #citybox als klasse?
    city_minlat = query_output[1][0]['bounds']['minlat']
    city_maxlat = query_output[1][0]['bounds']['maxlat']
    city_minlon = query_output[1][0]['bounds']['minlon']
    city_maxlon = query_output[1][0]['bounds']['maxlon']

    # Ergebnis eigentlich in Datenbank packen Tabelle "CityBoxes"
    print(city_minlat, city_maxlat, city_minlon, city_maxlon)
    return {'minlat': city_minlat, 'maxlat': city_maxlat, 'minlon': city_minlon, 'maxlon': city_maxlon}


osm_get_citybox()