import json
import os
import re
import psycopg2
from dateutil import parser, tz


# Remove "seconds" from endTime

data_regex = "StreamingHistory\d+\.json"
ext_data_regex = "endsong_\d+\.json"

DATADIR = '/mnt/Daten/Dateien/Spotify/data'


def main():
    json_files, extended_json_files = get_json_files(DATADIR)

    if extended_json_files:
        print("FOUND EXTENDED DATA")
        for f in extended_json_files:
            print(f"\t- {f}")

    print()

    if json_files:
        print("FOUND DATA")
        for f in json_files:
            print(f"\t- {f}")

    print()

    data = []
    for json_file in json_files:
        with open(json_file) as f:
            data += json.load(f)

    extended_data = []
    for json_file in extended_json_files:
        with open(json_file) as f:
            extended_data += json.load(f)

    conn = psycopg2.connect(
        database="spotify",
        user='ben',
        password='postgres',
        # host='localhost',
        # port='5432'
    )

    cursor = conn.cursor()

    print("IMPORTING EXTENDED DATA")
    import_extended_data(conn, cursor, extended_data)
    print("IMPORTING DATA")
    import_data(conn, cursor, data)

    print()
    cursor.close()
    conn.close()


def import_data(conn, cursor, data):
    length = len(data)
    for i, d in enumerate(data):
        endTime = d.get('endTime')
        msPlayed = d.get('msPlayed')
        trackName = d.get('trackName')
        artistName = d.get('artistName')
        print(f"{i} / {length}", end='\r')

        try:
            cursor.execute("""
            INSERT INTO streams (endTime, msPlayed, trackname, artistName)
                SELECT %s, %s, %s, %s
                WHERE
                    NOT EXISTS (SELECT * FROM streams WHERE endtime=%s AND msPlayed=%s AND trackName=%s AND artistName=%s)
            """, (endTime, msPlayed, trackName, artistName, endTime, msPlayed, trackName, artistName))

            conn.commit()
        except Exception as e:
            print(e)
            print(d)
            exit()

    print(f"{length} / {length}")


def import_extended_data(conn, cursor, data):
    length = len(data)
    for i, d in enumerate(data):
        endTime = d.get('ts')
        # Remove seconds and match the formatting of the less accurate "MyData" jsons
        endTime = parser.isoparse(endTime).replace(
            second=00).astimezone(tz.gettz('Europe/Berlin'))
        msPlayed = d.get('ms_played')
        trackName = d.get('master_metadata_track_name')
        artistName = d.get('master_metadata_album_artist_name')

        print(f"{i} / {length}", end='\r')

        try:
            cursor.execute("""
            INSERT INTO streams (endTime, msPlayed, trackname, artistName)
                SELECT %s, %s, %s, %s
                WHERE
                    NOT EXISTS (SELECT * FROM streams WHERE endtime=%s AND msPlayed=%s AND trackName=%s AND artistName=%s)
            """, (endTime, msPlayed, trackName, artistName, endTime, msPlayed, trackName, artistName))

            conn.commit()

        except Exception as e:
            print(e)
            print(d)
            exit()

    print(f"{length} / {length}")


def get_json_files(root):
    data_files = []
    extended_data_files = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if re.match(data_regex, name):
                data_files.append(os.path.join(path, name))
            elif re.match(ext_data_regex, name):
                extended_data_files.append(os.path.join(path, name))
    return data_files, extended_data_files


if __name__ == "__main__":
    main()
