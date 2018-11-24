import os
import json
# Exporting Data to a geoJSON file that is used with Leaflet to show on a Map in Browser
# Input is an Array if Lat

# was brauche ich? Stadtname > cityname; id, LonLat, Index > dataset
dataset = [{'id':1,'index':20,'coordinates':[[11.55830,48.16],[11.56830,48.16],[11.56830,48.155],[11.55830,48.155]]},
           {'id':2,'index':40,'coordinates':[[11.56830,48.16],[11.57830,48.16],[11.57830,48.155],[11.56830,48.155]]},
           {'id':3,'index':60,'coordinates':[[11.57830,48.16],[11.58830,48.16],[11.58830,48.155],[11.57830,48.155]]},
           {'id':4,'index':40,'coordinates':[[11.55830,48.155],[11.56830,48.155],[11.56830,48.15],[11.55830,48.15]]},
           {'id':5,'index':70,'coordinates':[[11.56830,48.155],[11.57830,48.155],[11.57830,48.15],[11.56830,48.15]]},
           {'id':6,'index':80,'coordinates':[[11.57830,48.155],[11.58830,48.155],[11.58830,48.15],[11.57830,48.15]]},
           {'id':7,'index':30,'coordinates':[[11.55830,48.15],[11.56830,48.15],[11.56830,48.145],[11.55830,48.145]]},
           {'id':8,'index':50,'coordinates':[[11.56830,48.15],[11.57830,48.15],[11.57830,48.145],[11.56830,48.145]]},
           {'id':9,'index':70,'coordinates':[[11.57830,48.15],[11.58830,48.15],[11.58830,48.145],[11.57830,48.145]]},
           ]
cityname = "Munich"

def data2geoJson (dataset):
    geojson = {'type':'FeatureCollection','features':[]}
    for i in range(len(dataset)):
        feat = {'type':'Feature','id':'' + str(dataset[i]['id']) + '','properties':{'calcindex': dataset[i]['index']},'geometry':{'type':'Polygon','coordinates': [dataset[i]['coordinates']]}}
        geojson['features'].append(feat)
    print(geojson)

    dir = os.path.dirname(os.path.dirname(__file__))
    exportdir = dir + "/M_Weboutput/JSON/"
    filename = "Grid_Munich.json"


    if os.path.exists(exportdir):
        with open(exportdir + filename, 'w') as output:
            output.write('var city_grid = ')
            json.dump(geojson, output, indent=2)
        print("yeah")
    else:
        print("fatal error in creatin geoJSON")

data2geoJson(cityname, dataset)


