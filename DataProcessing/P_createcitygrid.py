# Creating a Grid for each analysed city based on the map city box fetched from OSM
import pandas as pd
import math
import os
import json
from DataMining import M_Miner_OSM_CityBox as citybox
import numpy as np


def calcgrid(gridsize_m,cityname):
    #gridsize_m = value in meters

    citydim = citybox.osm_get_citybox(cityname)

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

    adjvalue_lat = (citylat - maxbins_lat * (gridsize))/2
    adjcitydim['maxlat'] = round(citydim['maxlat'] - adjvalue_lat, 6)
    adjcitydim['minlat'] = round(citydim['minlat'] + adjvalue_lat, 6)

    #output verification
    #print(citylat, adjvalue_lat)
    #print (adjcitydim['minlat'], adjcitydim['maxlat'], adjcitydim['minlon'], adjcitydim['maxlon'])
    #print(maxbins_lon, maxbins_lat, gridsize)


    numofbins = range(maxbins_lon * maxbins_lat)
    #databins.append()


    cols =[ 'binid','lon1','lat1','lon2','lat2','value','valuepercent']
    df2=[]
    for r in range(maxbins_lat):
        latval1 = adjcitydim['maxlat'] - (gridsize * r)
        latval2 = adjcitydim['maxlat'] - (gridsize * (r+1))
        for c in range(maxbins_lon):
            lonval1 = round(adjcitydim['minlon'] + (gridsize * c), 6)
            lonval2 = round(adjcitydim['minlon'] + (gridsize * (c+1)),6)
            #print(lonval1, latval1, lonval2, latval2)
            binid = 'R' + str(r+1) + 'N' + str(c+1)
            #dummyvalue = np.random.randint(10,100)
            dummyvalue = 0
            d = {'binid': binid, 'lon1': lonval1, 'lat1': latval1, 'lon2': lonval2, 'lat2': latval2, 'value': dummyvalue, 'valuepercent': dummyvalue}
            #print(d['value'])
            df2.append(d)
    df3 = pd.DataFrame(df2, columns=cols)
    df3.value = df3.value.astype('float')
    df3.valuepercent = df3.valuepercent.astype('float')
   # print(databins.head())
    return [adjcitydim, df3]

def data2geoJson (dataset, cityarray):
    geojson = {'type':'FeatureCollection','features':[]}
    ran = dataset.shape
    for i in range(ran[0]):
        if dataset.at[i, 'valuepercent'] > 0:
            p1 = [dataset.at[i, 'lon1'], dataset.at[i, 'lat1']]
            p2 = [dataset.at[i, 'lon2'], dataset.at[i, 'lat1']]
            p4 = [dataset.at[i, 'lon2'], dataset.at[i, 'lat2']]
            p3 = [dataset.at[i, 'lon1'], dataset.at[i, 'lat2']]
            coords = [p1,p2,p4,p3]
            # feat = {'type':'Feature','id':'' + str(dataset[i]['id']) + '','properties':{'calcindex': dataset[i]['index']},'geometry':{'type':'Polygon','coordinates': [dataset[i]['coordinates']]}}
            feat = {'type': 'Feature', 'id': dataset.at[i, 'binid'],
                    'properties': {'calcindex': dataset.at[i, 'valuepercent']},
                    'geometry': {'type': 'Polygon', 'coordinates': [ coords ]}}
            # print(feat)
            geojson['features'].append(feat)
            # print(geojson)

    syspath = os.path.dirname(os.path.dirname(__file__))
    exportpath = syspath + "/M_Weboutput/JSON/"
    filename = "Grid_Munich.json"

    if os.path.exists(exportpath):
        with open(exportpath + filename, 'w') as output:
            output.write('var city_array= ' + str(cityarray) + '\n')
            output.write('var city_grid = ')
            json.dump(geojson, output, indent=2)
        print("geoJSON success")
    else:
        print("fatal error in creating geoJSON")
