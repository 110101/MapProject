import mysql.connector

class POI_data:

    def __init__(self, id, timestamp, source, country, city, cat, name, type, addr, addr_nr, postcode, lat, lon, osm_id, opening_hours, addfield1):
            self.id = id
            self.timestamp = timestamp
            self.source = source
            self.country = country
            self.city = city
            self.cat = cat
            self.name = name
            self.type = type
            self.addr = addr
            self.addr_nr = addr_nr
            self.postcode = postcode

            # standard for all POIs
            self.lat = lat
            self.lon = lon

            # OSM spezifisch
            self.osm_id = osm_id
            self.opening_hours = opening_hours  # o
            self.addfield1 = addfield1


def pull_data(keyword):
    mysql_connection = mysql.connector.connect(host='localhost',database='POI_data',user='root',password='timsa110101')
    mysql_cursor = mysql_connection.cursor()

    sql_tabel = "pois_germany"
    sqL_query_string ="SELECT " + keyword + " FROM " + sql_tabel

    print(sqL_query_string)

    #ingest_args = (self.timestamp, self.source, self.country, self.city, self.cat, self.name, self.type, self.addr, self.addr_nr, self.postcode, self.lat, self.lon, self.osm_id, self.opening_hours, self.addfield1)

    try:
        mysql_cursor.execute(sqL_query_string,)
        sql_query_feedback = mysql_cursor.fetchall()
        mysql_cursor.close()

        print(sql_query_feedback)


        pois = [POI_data(c[0],c[1],c[2],c[3],c[4],c[5],c[6],c[7],c[8],c[9],c[10],c[11],c[12],c[13],c[14],c[15]) for c in sql_query_feedback]

        #for feedback_row in sql_query_feedback:
            #print(len(sql_query_feedback))


            #POIs = {'name': POI_data(num) for num in len(feedback_row)}


        '''class Switch:
             def __init__(self, ip, port):
                 self.ip, self.port = ip, port

           
           

             config = [['switch1', '10.0.0.101', '161'], ['switch2', '10.0.0.202', '161']]
             switches = [Switch(c[1], c[2]) for c in config]'''


        return pois
    except:
        mysql_connection.rollback()
        print("error")

    mysql_connection.close()




poi_sql = pull_data("*")

print(len(poi_sql))

print(poi_sql[780].country)