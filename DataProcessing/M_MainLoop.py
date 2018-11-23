# Hauptloop
# Aufruf der einzelnen Miner Module und Ingest
# bis loop steht Datei für Testaufrufe

from M_Miner_Source_OSM import M_Miner_Source_OSM_overpass

# Main Loop
def miner_loop():
    # OSM Miner
    M_Miner_Source_OSM_overpass.run_miner_OSM()

    # run Miner 1
    # DB Ingest

    # Miner 2

    # run Miner 2
    # DB Ingest

    # Miner 3

    # run Miner 3
    # DB Ingest

    # status_log
    # write logfile

def dataprocessing_loop():


def main_loop():



main_loop()


