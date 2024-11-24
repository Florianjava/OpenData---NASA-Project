import requests
import sqlite3
from datetime import datetime, timedelta




def fetch_data_neo(json) :
    weakly_count = json["element_count"]

    objects = json["near_earth_objects"]
    ids = []
    abs_magn = []
    est_diam_min = []  # en km
    est_diam_max = []
    hazardous = []   # booléen 
    close_approch_date = []   # date en yyyy-mm-dd
    rel_veloc = []  # en km/s
    miss_dist = []  # en km
    orb_body = [] # str sur objet en orbit
    #print(objects)
    for day in objects :
        for obj in objects[day] :
            #print(obj)
            ids.append(obj["id"])
            abs_magn.append(obj["absolute_magnitude_h"])
            est_diam_max.append(obj["estimated_diameter"]["kilometers"]["estimated_diameter_max"])
            est_diam_min.append(obj["estimated_diameter"]["kilometers"]["estimated_diameter_min"])
            hazardous.append(obj["is_potentially_hazardous_asteroid"])
            close_approch_date.append(obj["close_approach_data"][0]["close_approach_date"])
            rel_veloc.append(obj["close_approach_data"][0]["relative_velocity"]["kilometers_per_second"])
            miss_dist.append(obj["close_approach_data"][0]["miss_distance"]["kilometers"])
            orb_body.append(obj["close_approach_data"][0]["orbiting_body"])

    return weakly_count, ids, abs_magn, est_diam_max, est_diam_min, hazardous, close_approch_date, rel_veloc, miss_dist, orb_body

def read_neo() :

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER,
            absolute_magnitude FLOAT,
            estimated_diameter_min FLOAT,
            estimated_diameter_max FLOAT,
            is_hazardous INTEGER,
            close_approach_date DATE,
            relative_velocity FLOAT,
            miss_distance FLOAT,
            orbite_body TEXT
        )
    """)
    

    start_date = datetime(2024, 1, 1)  # Date de début
    end_date = datetime.now() #datetime(2023, 12, 31)   # datetime.now()           # Date actuelle
    url_template = "https://api.nasa.gov/neo/rest/v1/feed?start_date={}&end_date={}&api_key=kmprgzbT3jYlUGYa2BeDfRWMjrEnUu4RcWrelMfJ"
    #url = "https://api.nasa.gov/neo/rest/v1/feed?start_date=2015-09-07&end_date=2015-09-08&api_key=kmprgzbT3jYlUGYa2BeDfRWMjrEnUu4RcWrelMfJ"
    total_count =0
    current_date = start_date
    while current_date < end_date:
        next_date = min(current_date + timedelta(days=7), end_date)
        url = url_template.format(current_date.strftime('%Y-%m-%d'), next_date.strftime('%Y-%m-%d'))
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json() 
            weakly_count, ids, abs_magn, est_diam_max, est_diam_min, hazardous, close_approch_date, rel_veloc, miss_dist, orb_body = fetch_data(data)
            total_count += weakly_count
            for i in range(weakly_count) :        
                cursor.execute("""INSERT INTO data (id, absolute_magnitude, estimated_diameter_min, estimated_diameter_max, is_hazardous,
                close_approach_date, relative_velocity, miss_distance, orbite_body) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (ids[i], abs_magn[i],
                est_diam_min[i], est_diam_max[i], hazardous[i], close_approch_date[i], rel_veloc[i], miss_dist[i], orb_body[i]))
            conn.commit()
            print(f"Données insérées pour la période du {current_date} au {next_date}")
        else:
            print(f"Erreur lors de la requête pour la période du {current_date} au {next_date}: {response.status_code}")
        current_date = next_date +timedelta(days=1)


url = "https://api.nasa.gov/DONKI/CME?startDate=2024-03-01&endDate=2024-03-30&api_key=kmprgzbT3jYlUGYa2BeDfRWMjrEnUu4RcWrelMfJ"   # beaucoup de data pas hyper intéressantes
#url = "https://api.nasa.gov/DONKI/CMEAnalysis?startDate=2016-09-01&endDate=2016-09-30&mostAccurateOnly=true&speed=500&halfAngle=30&catalog=ALL&api_key=kmprgzbT3jYlUGYa2BeDfRWMjrEnUu4RcWrelMfJ"   # version du dessus filtrée?
# [{'activityID', 'startTime', 'cmeAnalyses'=[{'isMostAccurate', 'latitude', 'longitude', 'halfAngle', 'speed', 'type' }], 'linkedEvents'}]

#url = "https://api.nasa.gov/DONKI/GST?startDate=2024-03-01&endDate=2024-03-30&api_key=kmprgzbT3jYlUGYa2BeDfRWMjrEnUu4RcWrelMfJ"   # peu de data et pas très intéressantes
# [{'gstID', 'startTime', 'allKpIndex'=[{'observedTime', 'kpIndex', 'source'}], 'linkedEvents'}]
#url = "https://api.nasa.gov/DONKI/IPS?startDate=2024-03-01&endDate=2024-03-30&api_key=kmprgzbT3jYlUGYa2BeDfRWMjrEnUu4RcWrelMfJ"   # peu de data pas très intéressantes
# [{'activityID','eventTime', 'location'}]   # PAS DE LINKED EVENTS ?
#url = "https://api.nasa.gov/DONKI/FLR?startDate=2024-03-01&endDate=2024-03-30&api_key=kmprgzbT3jYlUGYa2BeDfRWMjrEnUu4RcWrelMfJ"   # beaucoup de data pas très intéressantes
# [{'flrID', 'beginTime', 'peakTime', 'endTime', 'classType', 'sourceLocation', 'activeRegionNum', 'linkedEvents}]
#url = "https://api.nasa.gov/DONKI/SEP?startDate=2024-03-01&endDate=2024-03-30&api_key=kmprgzbT3jYlUGYa2BeDfRWMjrEnUu4RcWrelMfJ"   # peu de data pas très intéressantes
# [{'sepID', 'eventTime', 'linkedEvents'}]
#url = "https://api.nasa.gov/DONKI/MPC?startDate=2024-03-01&endDate=2024-03-30&api_key=kmprgzbT3jYlUGYa2BeDfRWMjrEnUu4RcWrelMfJ"   # peu de data pas très intéressantes
# [{'mpcID', 'eventTime', 'linkedEvents'}]
#url = "https://api.nasa.gov/DONKI/RBE?startDate=2024-03-01&endDate=2024-03-30&api_key=kmprgzbT3jYlUGYa2BeDfRWMjrEnUu4RcWrelMfJ"   # peu de data pas très intéressantes
# [{'rbeID', 'eventTime', 'linkedEvents'}]
#url = "https://api.nasa.gov/DONKI/HSS?startDate=2024-03-01&endDate=2024-03-30&api_key=kmprgzbT3jYlUGYa2BeDfRWMjrEnUu4RcWrelMfJ"   # peu de data pas très intéressantes
# HSS : [{'hssID', 'eventTime', 'linkedEvents'}]   
#url = "https://api.nasa.gov/DONKI/WSAEnlilSimulations?startDate=2024-03-01&endDate=2024-03-30&api_key=kmprgzbT3jYlUGYa2BeDfRWMjrEnUu4RcWrelMfJ"   # peu de data pas très intéressantes

# LINKED EVENT MIGHT BE NONE
    


response = requests.get(url)
if response.status_code == 200:
    data = response.json()             
else :
    print("bad response")

print(data)
#toto()
db_path = "donky.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()


cursor.execute("""
        CREATE TABLE IF NOT EXISTS climate (
            id TEXT,
            kind TEXT,
            eventTime TIMESTAMP
        )
""")

cursor.execute("""
        CREATE TABLE IF NOT EXISTS flare (
            id TEXT,
            beginTime TIMESTAMP,
            peakTime TIMESTAMP,
            endTime TIMESTAMP,
            classType TEXT,
            sourceLocation TEXT,
            activeRegionNum INTEGER
        )
""")
cursor.execute("""
        CREATE TABLE IF NOT EXISTS geomagnetic (
            id TEXT,
            kpId Integer,
            observedTime TIMESTAMP,
            kpIndex FLOAT,
            source TEXT
        )
""")

cursor.execute("""
        CREATE TABLE IF NOT EXISTS coronal_analyse (
            id TEXT,
            isMostAccurate INTEGER,
            latitude FLOAT,
            longitude FLOAT,
            halfAngle FLOAT,
            speed FLOAT,
            type TEXT
        )
""")

cursor.execute("""
        CREATE TABLE IF NOT EXISTS coronal_impact (
            id TEXT,
            isGlancingBlow INTEGER,
            location TEXT,
            arrivalTime TIMESTAMP
        )
""")

cursor.execute("""
        CREATE TABLE IF NOT EXISTS linked_climate (
            event1 TEXT,
            event2 TEXT
        )
""")


def fetch_data_donky(data, kind):
    if kind == 'GST' :
        geomagnetic_rows = []
        linked_rows = []
        climate_rows = []
        for obs in data :   # on itère sur liste des observations 
            gstId = obs['gstID']
            eventTime = obs["startTime"]
            climate_rows.append([gstId, kind, eventTime])
            kps = obs["allKpIndex"]
            i = 1
            for kp in kps :
                geomagnetic_rows.append([gstId, i, kp['observedTime'], kp['kpIndex'], kp['source']])
                i+=1
            linked = obs['linkedEvents']
            if linked is not None :
                for link in linked :
                    linked_rows.append([gstId, link['activityID']])
        return climate_rows, linked_rows, geomagnetic_rows, None


    if kind == 'FLR' :
        flare_rows = []
        linked_rows = []
        climate_rows = []
        for obs in data : 
            flrId = obs['flrID']
            eventTime = obs["peakTime"]
            climate_rows.append([flrId, kind, eventTime])
            flare_rows.append([flrId, obs["beginTime"], obs["peakTime"], obs["endTime"], obs['classType'], obs["sourceLocation"], obs['activeRegionNum']])
            linked = obs['linkedEvents']
            if linked is not None :
                for link in linked :
                    linked_rows.append([flrId, link['activityID']])
        return climate_rows, linked_rows, flare_rows, None

    if kind == 'CME' :
        i=0
        coronal_rows = []
        coronal_impact_rows = []
        linked_rows = []
        climate_rows = []
        for obs in data :
            #print(obs)
            cmeId = obs['activityID']
            eventTime = obs["startTime"]
            climate_rows.append([cmeId, kind, eventTime])

            analyses = obs['cmeAnalyses']
            for an in analyses :
                coronal_rows.append([cmeId, an["isMostAccurate"], an['latitude'], an["longitude"], an["halfAngle"], an['speed'], an["type"]])
            
            for an in analyses :
                enlil = an["enlilList"]
                if enlil is not None :    
                    for en in enlil :
                        imp = en["impactList"]
                        if imp is not None :
                            print("il est pas None")
                            for im in imp :
                                coronal_impact_rows.append([cmeId, im["isGlancingBlow"], im["location"], im['arrivalTime']])


            linked = obs['linkedEvents']
            if linked is not None :
                for link in linked :
                    linked_rows.append([cmeId, link['activityID']])
        return climate_rows, linked_rows, coronal_rows, coronal_impact_rows

    else :
        linked_rows = []
        climate_rows = []
        if kind == 'IPS' :
            id_col = 'activityID'
        else :
            id_col = str.lower(kind)+"ID"
        for obs in data :
            iidd = obs[id_col]
            eventTime = obs["eventTime"]
            climate_rows.append([iidd, kind, eventTime])
            if 'linkedEvents' in obs :
                linked = obs['linkedEvents']
                if linked is not None :
                    for link in linked :
                        linked_rows.append([iidd, link['activityID']])

        return climate_rows, linked_rows, None, None
    



names = {'CME' : 'Coronal mass ejection', 'GST' : 'Geomagnetic storm', 'IPS':'Interplanetary shock', 'FLR' : 'Solar Flare', 'SEP' : 'Solar energetic particle',
          'MPC':'Magnetopause crossing', 'RBE': 'Radiation Belt Enhancement', 'HSS': 'Hight speed stream'}
    
base_url = url = "https://api.nasa.gov/DONKI/"
for kind in ['CME'] :
    print("----- KIND =", kind, ' ----')
    url_template = base_url+kind+"?start_date={}&end_date={}&api_key=kmprgzbT3jYlUGYa2BeDfRWMjrEnUu4RcWrelMfJ"

    start_date = datetime(2023, 1, 1)  # Date de début
    end_date = datetime.now() #datetime(2023, 12, 31)   # datetime.now()           # Date actuelle
    total_count =0
    current_date = start_date
    while current_date < end_date:
            next_date = min(current_date + timedelta(days=30), end_date)
            url = url_template.format(current_date.strftime('%Y-%m-%d'), next_date.strftime('%Y-%m-%d'))
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json() 
                climate_rows, linked_rows, auxiliary_rows, subauxiliary_rows = fetch_data_donky(data, kind=kind)
                #toto()
                total_count += len(climate_rows)
                
                #for i in range(len(climate_rows)) :
                #    cursor.execute("""INSERT INTO climate (id, kind, eventTime) VALUES (?, ?, ?)""", (climate_rows[i][0], climate_rows[i][1], climate_rows[i][2]))
                #conn.commit()

                #for i in range(len(linked_rows)) :
                #    cursor.execute("""INSERT INTO linked_climate (event1, event2) VALUES (?, ?)""", (linked_rows[i][0], linked_rows[i][1]))
                #conn.commit()
                
                
                if kind == 'CME' :
                #    for i in range(len(auxiliary_rows)) :
                #        cursor.execute("""INSERT INTO coronal_analyse (id, isMostAccurate, latitude, longitude, halfAngle, speed, type) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                #        (auxiliary_rows[i][0], auxiliary_rows[i][1], auxiliary_rows[i][2], auxiliary_rows[i][3], auxiliary_rows[i][4], auxiliary_rows[i][5], auxiliary_rows[i][6]))
                #    conn.commit()
                    for i in range(len(subauxiliary_rows)) :
                        cursor.execute("""INSERT INTO coronal_impact (id, isGlancingBlow, location, arrivalTime) VALUES (?, ?, ?, ?)""",
                        (subauxiliary_rows[i][0], subauxiliary_rows[i][1], subauxiliary_rows[i][2], subauxiliary_rows[i][3]))
                    conn.commit()

                #if kind == 'FLR' :
                #    for i in range(len(auxiliary_rows)) :
                #        cursor.execute("""INSERT INTO flare (id, beginTime, peakTime, endTime, classType, sourceLocation, activeRegionNum) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                #        (auxiliary_rows[i][0], auxiliary_rows[i][1], auxiliary_rows[i][2], auxiliary_rows[i][3], auxiliary_rows[i][4], auxiliary_rows[i][5], auxiliary_rows[i][6]))
                #    conn.commit()

                #if kind == 'GST' :
                #    for i in range(len(auxiliary_rows)) :
                #        cursor.execute("""INSERT INTO  geomagnetic (id, kpId, observedTime, kpIndex, source) VALUES (?, ?, ?, ?, ?)""",
                #        (auxiliary_rows[i][0], auxiliary_rows[i][1], auxiliary_rows[i][2], auxiliary_rows[i][3], auxiliary_rows[i][4]))
                #    conn.commit()
                
                print(f"Données insérées pour la période du {current_date} au {next_date}")
            else:
                print(f"Erreur lors de la requête pour la période du {current_date} au {next_date}: {response.status_code}")
            current_date = next_date +timedelta(days=1)



conn.close()


    
