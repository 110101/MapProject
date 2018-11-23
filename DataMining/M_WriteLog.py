import os
import csv

# create log folder and new log *.csv file
def writelog(log_type, path, query_timestamp, query_source, query_keyword, timestamp_ingest_start, timestamp_ingest_fin, log_comment):


    if log_type == "success":

        log_folder = '' + path + '/logs/'
        if not os.path.exists(log_folder):
                os.makedirs(log_folder)
        date_f = query_timestamp[:query_timestamp.find(' ')]
        time_f = query_timestamp[query_timestamp.find(' '):]
        log_name = log_folder + date_f + '_' + time_f + '_Logfile_Miner_Source_OSM.csv'

        with open(log_name, 'w') as csvfile:
            logwriter = csv.writer(csvfile)
            logwriter.writerow([query_timestamp])
            logwriter.writerow([str("Query_Source: " + query_source)])
            logwriter.writerow(["Keyword: " + query_keyword[2]])
            logwriter.writerow(["Comment:" +  log_comment])
            logwriter.writerow(["Ingest Start:" + str(timestamp_ingest_start) + " / Ingest Fin:" + str(timestamp_ingest_fin)])
            logwriter.writerow(["successfull"])
    elif log_type == "err":
        err_log_folder = '' + path + '/err_logs/'
        if not os.path.exists(err_log_folder):
            os.makedirs(err_log_folder)
        date_f = query_timestamp[:query_timestamp.find(' ')]
        time_f = query_timestamp[query_timestamp.find(' '):]
        err_log_name = err_log_folder + date_f + '_' + time_f + '_ERROR_Logfile_Miner_Source_OSM.csv'
        with open(err_log_name, 'w') as csvfile:
            err_logwriter = csv.writer(csvfile)
            err_logwriter.writerow([query_timestamp])
            err_logwriter.writerow([str("Query_Source: " + query_source)])
            err_logwriter.writerow(["Keyword: " + query_keyword])
            err_logwriter.writerow(["ERROR!" + log_comment + "Querry not successfull"])
        return

# add additional Information to an existen querry log file
def addlog(log_type):
    return