# Creating a Grid for each analysed city based on the map city box fetched from OSM
import math
from DataMining import M_Miner_OSM_CityBox as citybox

gridsize_m = 500; #value in Metern?

citydim = citybox.osm_get_citybox("Munich")

# doing the math
#gridsizes meter in grad
gridsize = (gridsize_m/111.32) * 0.001

#currently works only for cities east of greenich and north of the equator--- bug
#calculate citywidth an max. amount of bins
citylon = round(citydim['maxlon'] - citydim['minlon'], 6)
maxbins_lon = math.trunc(citylon/gridsize)

citylat = round(citydim['maxlat'] - citydim['minlat'], 6)
maxbins_lat = math.trunc(citylat/gridsize)

#place grid with max amount of bins in the middle of the lon city boundaries
adjvalue_lon = (citylon - maxbins_lon * gridsize)/2
adjcitydim = {}
adjcitydim['maxlon'] = round(citydim['maxlon'] - adjvalue_lon, 6)
adjcitydim['minlon'] = round(citydim['minlon'] + adjvalue_lon, 6)

adjvalue_lat = (citylat - maxbins_lat * gridsize)/2
adjcitydim['maxlat'] = round(citydim['maxlat'] - adjvalue_lat, 6)
adjcitydim['minlat'] = round(citydim['minlat'] + adjvalue_lat, 6)

#print(citylat, adjvalue_lat)
#print (adjcitydim['minlat'], adjcitydim['maxlat'], adjcitydim['minlon'], adjcitydim['maxlon'])
#print(maxbins_lon, maxbins_lat, gridsize)

#create lon lat for each bin
#...
# idea.. bin[i] : minlon/maxlat and then lon + gridsizes, lat stays initially same  ... rows of bins

