import os
import json
# Exporting Data to a geoJSON file that is used with Leaflet to show on a Map in Browser
# Input is an Array if Lat

# was brauche ich? Stadtname > cityname; id, LonLat, Index > dataset
# dataset = [{'id':1,'index':20,'coordinates':[[11.55830,48.16],[11.56830,48.16],[11.56830,48.155],[11.55830,48.155]]},
#            {'id':2,'index':40,'coordinates':[[11.56830,48.16],[11.57830,48.16],[11.57830,48.155],[11.56830,48.155]]},
#            {'id':3,'index':60,'coordinates':[[11.57830,48.16],[11.58830,48.16],[11.58830,48.155],[11.57830,48.155]]},
#            {'id':4,'index':40,'coordinates':[[11.55830,48.155],[11.56830,48.155],[11.56830,48.15],[11.55830,48.15]]},
#            {'id':5,'index':70,'coordinates':[[11.56830,48.155],[11.57830,48.155],[11.57830,48.15],[11.56830,48.15]]},
#            {'id':6,'index':80,'coordinates':[[11.57830,48.155],[11.58830,48.155],[11.58830,48.15],[11.57830,48.15]]},
#            {'id':7,'index':30,'coordinates':[[11.55830,48.15],[11.56830,48.15],[11.56830,48.145],[11.55830,48.145]]},
#            {'id':8,'index':50,'coordinates':[[11.56830,48.15],[11.57830,48.15],[11.57830,48.145],[11.56830,48.145]]},
#            {'id':9,'index':70,'coordinates':[[11.57830,48.15],[11.58830,48.15],[11.58830,48.145],[11.57830,48.145]]},
#            ]
# cityname = "Munich"

def data2geoJson (dataset):
    geojson = {'type':'FeatureCollection','features':[]}
    ran = dataset.shape
    for i in range(ran[0]):
        if dataset.at[i, 'valuepercent'] > 0:
            p1 = [dataset.at[i, 'lon1'], dataset.at[i, 'lat1']]
            p2 = [dataset.at[i, 'lon2'], dataset.at[i, 'lat1']]
            p4 = [dataset.at[i, 'lon2'], dataset.at[i, 'lat2']]
            p3 = [dataset.at[i, 'lon1'], dataset.at[i, 'lat2']]
            coords = [p1,p2,p4,p3]
            #feat = {'type':'Feature','id':'' + str(dataset[i]['id']) + '','properties':{'calcindex': dataset[i]['index']},'geometry':{'type':'Polygon','coordinates': [dataset[i]['coordinates']]}}
            feat = {'type': 'Feature', 'id': dataset.at[i, 'binid'],
                    'properties': {'calcindex': dataset.at[i, 'valuepercent']},
                    'geometry': {'type': 'Polygon', 'coordinates': [ coords ]}}
            #print(feat)
            geojson['features'].append(feat)
            #print(geojson)

    dir = os.path.dirname(os.path.dirname(__file__))
    exportdir = dir + "/M_Weboutput/JSON/"
    filename = "Grid_Munich.json"


    if os.path.exists(exportdir):
        with open(exportdir + filename, 'w') as output:
            output.write('var city_grid = ')
            json.dump(geojson, output, indent=2)
        print("geoJSON success")
    else:
        print("fatal error in creatin geoJSON")



