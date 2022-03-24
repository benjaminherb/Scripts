# Setup Table in postgresdb

# CREATE TABLE streams(
#   endTime date,
#   msPlayed numeric(16,0),
#   trackName varchar(512),
#   artistName varchar(512)
# );

import json
import psycopg2

data = []

for i in 0,1,2,3,4:
    with open('data/endsong_' + str(i) + '.json') as f:
        data += json.load(f)


conn = psycopg2.connect(
    database="DATABASE",
    user='USER',
    password='PASSWORD',
    # host='localhost',
    # port='5432'
)

cursor = conn.cursor()
print("IMPORTING DATA")
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

print()
conn.close()


