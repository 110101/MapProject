import os
import numpy as np
import pandas as pd
from DataProcessing import M_createcitygrid as ccg
from DataProcessing import M_Data2geoJSON as D2GJ

#get city dimensions and calc number of bins (gridesize in meters, cityname in en)
# return is [adjcitydim, dataset]
gridsize = 500 # in meters
citygrid = ccg.calcgrid(gridsize, "Munich")


citydim = citygrid[0]
data = citygrid[1]

#print(data)
# setup city box
# Raster Bins um
print(data.shape)

D2GJ.data2geoJson(data, gridsize)

# 3. in Objekt an Heat Map ausgabe übergeben


######
"""radius_earth = 6378.137

dLat = citybox['minlon']  * math.pi / 180 - citybox['maxlon'] * math.pi / 180
dLon = citybox['minlat'] * math.pi / 180 - citybox['maxlat'] * math.pi / 180

a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(citybox['minlat'] * math.pi / 180) * math.cos(citybox['maxlat'] * math.pi / 180) * math.sin(dLon / 2) * math.sin(dLon / 2)

c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
d = radius_earth * c

#print(d)"""