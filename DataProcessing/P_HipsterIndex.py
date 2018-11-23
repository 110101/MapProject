import os
from M_Miner_Source_OSM import M_Miner_OSM_CityBox

# Struktur der Datei:
# 1. Daten für HipsterIndex aus Datenbanken ziehen

#Quelle 1: OSM > Bio, Bars,

#Daten aus Datenbank für HipsterIndex


#Json Dump für Anzeige um Durch Stich sicherzustellen

# City Bounding Box
# 4. nachkommerstelle ist der 10 m Bereich, exakter 11.1 m Bereich. Die 5 Stelle um 9 Erhöhren um 10 m weiter zu gehen
#   10km 1km 100m 10m  1m
#11.1     2    3   4    5

#Abfrage s. M_Miner_OSM_CityBox > Frage CityCenter und CityBox
citycenter = {'lat': 48.1548703, 'lon': 11.5418426}    # 48.123456 / lon: 11.123456

print(os.path.curdir)
citybox = M_Miner_OSM_CityBox.osm_get_citybox()
citybox_dummy = {"minlat": 48.0616244, "minlon": 11.3607770, "maxlat": 48.2481162, "maxlon": 11.7229083}

#createbins
# double check range

print(citybox)

#num of boxes
lonrange = round(citybox['maxlon'] - citybox['minlon'],3)
latrange = round(citybox['maxlat'] - citybox['minlat'],3)

lon_num_boxes = int(lonrange/0.001)   #x bins
lat_num_boxes = int(latrange/0.001)   #y bins

#-#-#-#


print(lon_num_boxes, lat_num_boxes)


# setup city box
# Raster Bins um



# 3. in Objekt an Heat Map ausgabe übergeben


######
"""radius_earth = 6378.137

dLat = citybox['minlon']  * math.pi / 180 - citybox['maxlon'] * math.pi / 180
dLon = citybox['minlat'] * math.pi / 180 - citybox['maxlat'] * math.pi / 180

a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(citybox['minlat'] * math.pi / 180) * math.cos(citybox['maxlat'] * math.pi / 180) * math.sin(dLon / 2) * math.sin(dLon / 2)

c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
d = radius_earth * c

#print(d)"""