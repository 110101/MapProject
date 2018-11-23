#Schleife x pro Woche um Quelldatenbank zu füllen, aktualisieren

from M_Miner_OSM import M_Miner_OSM_overpass as Miner_OSM

#Miner 1 - OpenStreetMap / Overpass Shop Data
Miner_status = Miner_OSM.run_miner_OSM()
print(Miner_status)
