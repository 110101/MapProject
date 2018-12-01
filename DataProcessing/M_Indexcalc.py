import os
import time
import datetime
import numpy as np
import pandas as pd
from DataProcessing import M_DBAccess as DBA
from DataProcessing import M_createcitygrid as ccg
from DataProcessing import M_Data2geoJSON as d2gj


class city():
    def __init__(self):
        self.gridsize = []
        self.data = []
        self.dim = []
        self.name = ""

    def adddata(self, name, gridsize, citydim, citydata):
        self.gridsize = gridsize
        self.dim = citydim
        self.data = citydata
        self.name = name

cityarray = ["Munich","Berlin"]
cols = ['binid', 'lon1', 'lat1', 'lon2', 'lat2', 'value', 'valuepercent']
all_citybins = pd.DataFrame(columns=cols)

for cityn in cityarray:
    print("Start: " + cityn + str(datetime.datetime.now()))
    newcity = city()

    #get city dimensions and calc number of bins (gridesize in meters, cityname in en)
    # return is [adjcitydim, dataset]
    cityname = cityn
    gridsize = 1000 # in meters
    citygrid = ccg.calcgrid(gridsize, cityname)

    #citygrid[0]: city dimensions ; citygrid[1]: dataframe containing bins and default index value
    newcity.adddata(cityname, gridsize, citygrid[0], citygrid[1])


    keyword = "pub"
    sql_table = "pois_germany"
    if cityname == "Munich":
        cityname_de = "München"
    elif cityname == "Berlin":
        cityname_de = "Berlin"

    # Indexberechnung
    # get sql data
    # load data from source 1 "OSM" with Keyword "pub" into dataframe
    sql_output_OSM_bar = DBA.pull_data(sql_table, keyword, cityname_de)

    if sql_output_OSM_bar is None:
        print("error")
    else:
        print("Found items in DB: " + str(sql_output_OSM_bar.shape[0]))

        #bins durch iterieren bin a - vergleich mit allen Quellen
        #bins für Stadt
        citybins = []
        citybins = newcity.data

        for numberofbin in range(citybins.shape[0]):
            bin_index = 0
            lat1_bin = citybins.at[numberofbin, 'lat1']
            lat2_bin = citybins.at[numberofbin, 'lat2']
            lon1_bin = citybins.at[numberofbin, 'lon1']
            lon2_bin = citybins.at[numberofbin, 'lon2']

            for row_sql_out in range(sql_output_OSM_bar.shape[0]):
                sql_lat = sql_output_OSM_bar.at[row_sql_out, 'lat']
                sql_lon = sql_output_OSM_bar.at[row_sql_out, 'lon']


                if (sql_lat <= lat1_bin) & (sql_lat >= lat2_bin) & (sql_lon >= lon1_bin) & (sql_lon <= lon2_bin):
                    #print("yes")
                    bin_index = bin_index+1
            #print(bin_index)

            #prozent
            citybins.at[numberofbin, 'value'] = bin_index

            #prozent
        maxval_bin = citybins['value'].max()
        for numobins in range(citybins.shape[0]):
            citybins.at[numobins, 'valuepercent'] = (citybins.at[numobins, 'value'] / maxval_bin) * 100

        print(citybins.iloc[:,citybins.columns.get_indexer(['binid','value'])])
        # Check output
        print("Number of active bins:" + str(citybins.shape[0]))


        #print(data)
        # setup city box
        # Raster Bins um

    bigdata = pd.concat([all_citybins, citybins], ignore_index=True)
    all_citybins = citybins

    print("Stop: " + cityn + str(datetime.datetime.now()))

d2gj.data2geoJson(bigdata)

# 3. in Objekt an Heat Map ausgabe übergeben


######
"""radius_earth = 6378.137

dLat = citybox['minlon']  * math.pi / 180 - citybox['maxlon'] * math.pi / 180
dLon = citybox['minlat'] * math.pi / 180 - citybox['maxlat'] * math.pi / 180

a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(citybox['minlat'] * math.pi / 180) * math.cos(citybox['maxlat'] * math.pi / 180) * math.sin(dLon / 2) * math.sin(dLon / 2)

c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
d = radius_earth * c

#print(d)"""