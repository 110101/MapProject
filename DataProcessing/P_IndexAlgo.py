import datetime
import pandas as pd
from DataProcessing import M_DBAccess as dba
from DataProcessing import P_createcitygrid as ccg

class city():
    def __init__(self):
        self.gridsize = []
        self.bins = []
        self.dim = []
        self.name = ""
        self.log_starttime = 0
        self.log_stoptime = 0

    def adddata(self, name, gridsize, citydim, class_citybins):
        self.gridsize = gridsize
        self.dim = citydim
        self.bins = class_citybins
        self.name = name

    def logging(self,starttime, stoptime):
        self.log_starttime = starttime
        self.log_stoptime = stoptime

    ####################################
    # def sqldata4cat(self, keyword)


cityarray = ["Munich"]
cols = ['binid', 'lon1', 'lat1', 'lon2', 'lat2', 'value', 'valuepercent']
all_citybins = pd.DataFrame(columns=cols)
bigdata = []
cityn = 0

for cityn in cityarray:
    # new city class
    newcity = city()
    citybins = []
    sql_output_OSM_leisure = []
    sql_output_OSM_hipster = []

    # recording start time for logging
    starttime = datetime.datetime.now()
    print("Start: " + cityn + " at " + str(starttime))
    newcity.logging(starttime, 0)

    # this needs to be automated with config file
    sql_table = "data_munich"
    if cityn == "Munich":
        cityname = "Muenchen"
    else:
        cityname = cityn

    # get city dimensions and calc number of bins (gridesize in meters, cityname in en)
    # return is [adjcitydim, dataset]
    gridsize = 1500  # in meters
    city_dim, city_bins = ccg.calcgrid(gridsize, cityname)

    # citygrid[0]: city dimensions ; citygrid[1]: dataframe containing bins and default index value
    newcity.adddata(cityname, gridsize, city_dim, city_bins)

    # --- index calculation ---
    # the magic happens here
    #
    # Setup the different sub_index (leisure, hipster, unhippness, pricing, location)
    # setup leisure index and querry sql_table for leisure_keywords aka. categories (or short cat)
    leisure_keywords = ["bar", "restaurant"]
    factor_leisure_cat = [0, 1]
    factor_leisure_total = 1
    for leisure_keyword_n in range(len(leisure_keywords)):
        sql_output_OSM_leisure.append(dba.pull_data(sql_table, leisure_keywords[leisure_keyword_n], cityname))
        print("Found " + str(sql_output_OSM_leisure[leisure_keyword_n].shape[0]) + " in DB for " +
              leisure_keywords[leisure_keyword_n])

    # setup hipster index and querry sql_table
    hipster_keys = ["cafe", "coffee", "organic"]
    factor_hipster_cat = [1, 1.5, 2]
    factor_hipster_total = 0
    for hipster_keys_n in range(len(hipster_keys)):
        sql_output_OSM_hipster.append(dba.pull_data(sql_table, hipster_keys[hipster_keys_n], cityname))
        print("Found " + str(sql_output_OSM_hipster[hipster_keys_n].shape[0]) + " in DB for " +
              hipster_keys[hipster_keys_n])

    # get city bins for selected city out of class
    citybins = newcity.bins
    print("Number of bins:" + str(citybins.shape[0]))

    # Iterate thorugh all bins for one city
    # citybins.shape is the total number of bins for the city
    # select bin and calculate all sub_indices and the over all bin_index as the final result
    for numberofbin in range(citybins.shape[0]):
        bin_index = 1
        lat1_bin = citybins.at[numberofbin, 'lat1']
        lat2_bin = citybins.at[numberofbin, 'lat2']
        lon1_bin = citybins.at[numberofbin, 'lon1']
        lon2_bin = citybins.at[numberofbin, 'lon2']

        # --- calculate leisure index for selected bin ---
        #
        # set empty dict for output leisure index for each category
        leisure_index = {}
        for index_leisure_cats in range(len(sql_output_OSM_leisure)):
            # check if sql_output for OSM leisure data is not None
            if sql_output_OSM_leisure[index_leisure_cats] is None or factor_leisure_total == 0:
                print("")
            else:
                # if sql output is not None calculate leisure index for each category
                temp_leisure_index = 0
                for row_sql_out in range(sql_output_OSM_leisure[index_leisure_cats].shape[0]):
                    # rework... !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # matching different outputs from sql with selected bin in loop
                    sql_lat = sql_output_OSM_leisure[index_leisure_cats].at[row_sql_out, 'lat']
                    sql_lon = sql_output_OSM_leisure[index_leisure_cats].at[row_sql_out, 'lon']

                    if (sql_lat <= lat1_bin) & (sql_lat >= lat2_bin) & (sql_lon >= lon1_bin) & (sql_lon <= lon2_bin):
                        temp_leisure_index = temp_leisure_index + 1
            leisure_index[leisure_keywords[index_leisure_cats]] = temp_leisure_index * \
                factor_leisure_cat[index_leisure_cats]

        # --- calculate hipster sub_index for selected bin ---
        #
        # set empty dict for output hipster index for each category
        hipster_index = {}
        for index_hipster_cats in range(len(sql_output_OSM_hipster)):
            # check if sql_output for OSM leisure data is not None
            if sql_output_OSM_hipster[index_hipster_cats] is None or factor_hipster_total == 0:
                temp_hipster_index = 0
            else:
                # if sql output is not None calculate leisure index for each category
                temp_hipster_index = 0
                for row_sql_out in range(sql_output_OSM_hipster[index_hipster_cats].shape[0]):
                    # rework... !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # matching different outputs from sql with selected bin in loop
                    sql_lat = sql_output_OSM_hipster[index_hipster_cats].at[row_sql_out, 'lat']
                    sql_lon = sql_output_OSM_hipster[index_hipster_cats].at[row_sql_out, 'lon']

                    if (sql_lat <= lat1_bin) & (sql_lat >= lat2_bin) & (sql_lon >= lon1_bin) & (
                            sql_lon <= lon2_bin):
                        temp_hipster_index = temp_hipster_index + 1
            hipster_index[hipster_keys[index_hipster_cats]] = temp_hipster_index * factor_hipster_cat[
                index_hipster_cats]

        # Main Algo equation
        bin_index = sum(leisure_index.values()) * factor_leisure_total + sum(hipster_index.values()) * \
            factor_hipster_total

        # final value for bin
        citybins.at[numberofbin, 'value'] = bin_index

        # prozent
    maxval_bin = citybins['value'].max()
    for numobins in range(citybins.shape[0]):
        norm_index = (citybins.at[numobins, 'value'] / maxval_bin) * 100
        citybins.at[numobins, 'valuepercent'] = round(norm_index,2)

    # setup city box
    # Raster Bins um

    bigdata = pd.concat([all_citybins, citybins], ignore_index=True)
    all_citybins = citybins

print("Stop: " + cityn + str(datetime.datetime.now()) + "  Duration: " + str(datetime.datetime.now() - starttime))

ccg.data2geoJson(bigdata, cityarray)


######
"""radius_earth = 6378.137

dLat = citybox['minlon']  * math.pi / 180 - citybox['maxlon'] * math.pi / 180
dLon = citybox['minlat'] * math.pi / 180 - citybox['maxlat'] * math.pi / 180

a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(citybox['minlat'] * math.pi / 180) * math.cos(citybox['maxlat'] 
    * math.pi / 180) * math.sin(dLon / 2) * math.sin(dLon / 2)

c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
d = radius_earth * c

print(d)"""
