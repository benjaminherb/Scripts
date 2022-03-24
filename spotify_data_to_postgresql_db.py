# Setup Table in postgres

# CREATE TABLE streams(
#   endTime date,
#   msPlayed numeric(16,0),
#   trackName varchar(512),
#   artistName varchar(512)
# );

import json
import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    database="DATABASE",
    user='USER',
    password='PASSWORD',
    # host='localhost',
    # port='5432'
)

print("IMPORTING EXTENDED DATA")

data = []
for i in 0,1,2,3,4:
    with open('data/endsong_' + str(i) + '.json') as f:
        data += json.load(f)

cursor = conn.cursor()

for i,d in enumerate(data):
    endTime = d.get('ts')
    msPlayed = d.get('ms_played')
    trackName = d.get('master_metadata_track_name')
    artistName = d.get('master_metadata_album_artist_name')
    print(i, end='\r')

    try:
        cursor.execute("INSERT INTO streams VALUES( %s, %s, %s, %s)", (
        endTime, msPlayed, trackName, artistName))
        conn.commit()
    except Exception as e:
        print(e)
        print(d)
        exit()

print("IMPORTING DATA")

for i in 0,1:
    with open('data/StreamingHistory' + str(i) + '.json') as f:
        data += json.load(f)

cursor.execute("""SELECT endTime FROM streams ORDER BY endTime DESC LIMIT 1;""")
newest_entry = cursor.fetchall()[0][0]
print(newest_entry)

print("IMPORTING DATA")
for i,d in enumerate(data):
    endTime = d.get('endTime') + ':00'
    msPlayed = d.get('msPlayed')
    trackName = d.get('trackName')
    artistName = d.get('artistName')
    print(i, end='\r')
    
    endTime_comp = datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')

    if (endTime_comp > newest_entry):
        print(str(endTime_comp) + " is newer compared to " + str(newest_entry))
        try:
            cursor.execute("INSERT INTO streams VALUES( %s, %s, %s, %s)", (
            endTime, msPlayed, trackName, artistName))
           
            conn.commit()
        except Exception as e:
            print(e)
            print(d)
            exit()

print()

conn.close()





