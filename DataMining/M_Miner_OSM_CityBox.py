import csv
import requests
import pandas as pd

#eigentlich Teil von Dataprocessing
#Citybox wird als Input für Dataprocessing benötigt
#Synergie mit OSM Miner nur weil CityBox aus Kartendaten kommen
#Abfrage eigentlich nur 1 mal notwendig

def osm_querry_config(city):
    querrys = []
    keywords = []
   # with open("/M_Miner_OSM/config_miner_source_osm.csv", "r") as configfile:
        #userFileReader = csv.DictReader(configfile)

   # for query_row in userFileReader:
    #setup querry for overpass api
    osm_id_convert = 3600000000

    if city == "Muenchen":
        city_id01 = 62428 #int(query_row['osm_area_id'])
        osm_id_convert = osm_id_convert + city_id01
        level = 6
    elif city == "Berlin":
        city_id02 = 62422
        osm_id_convert = osm_id_convert + city_id02
        level = 4
    else:
        city_id = 0
    #query_string = '"' + query_row['key_string'] + '"="' + query_row['key_value'] + '"'


    overpass_query = """
        [out:json][timeout:300];
        area(""" + str(osm_id_convert) + """)->.searchArea;
        (
        rel['admin_level'='""" + str(level) + """'](area.searchArea);
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


def osm_get_citybox(city):
    query_input, query_keywords = osm_querry_config(city)

    query_output = osm_querry(query_input, query_keywords)
    query_output_data = query_output[1]

    #citybox als klasse?

    city_lat = []
    city_lon = []
    for i in range(len(query_output)):

        minlat = query_output[1][0]['bounds']['minlat']
        maxlat = query_output[1][0]['bounds']['maxlat']
        minlon = query_output[1][0]['bounds']['minlon']
        maxlon = query_output[1][0]['bounds']['maxlon']

        city_lon.append(maxlon)
        city_lon.append(minlon)
        city_lat.append(maxlat)
        city_lat.append(minlat)

    df_lat = pd.DataFrame(city_lat)
    df_lat.columns = ['A']
    df_lon = pd.DataFrame(city_lon)
    df_lon.columns = ['A']

    city_minlat = df_lat.min()
    city_maxlat = df_lat.max()
    city_minlon = df_lon.min()
    city_maxlon = df_lon.max()


    # Ergebnis eigentlich in Datenbank packen Tabelle "CityBoxes"
    #print(city_minlat, city_maxlat, city_minlon, city_maxlon)
    return {'minlat': city_minlat['A'], 'maxlat': city_maxlat['A'], 'minlon': city_minlon['A'], 'maxlon': city_maxlon['A']}
