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
import argparse
import os
import re

def main(): 
    data_dir, database, table, user, password = parse_arguments()

    conn = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        # host='localhost',
        # port='5432'
    )
    
    data_reg = re.compile("^StreamingHistory[0-9]{1,2}.json$")
    data_ex_reg = re.compile("^endsong_[0-9]{1,2].json$")

    json = get_json_files(data_dir, data_reg)
    json_ex = get_json_files(data_dir, data_ex_reg)

    print("EXTENDED DATA: " + str(json_ex))
    print("DATA: " + str(json))

    ## Import extended data
    if not len(json_ex) == 0:
        while True:
            entry = input("ADD EXTENDED DATA AND DROP EXISTING TABLE? (y/n)")
            if entry == 'y' or entry == 'n':
                break
        
        if entry == 'y':
            for j in json_ex:
                import_extended_data(conn, j, data_dir, table)

    ## Import data if it is newer
    for j in json:
        import_data(conn, j, data_dir, table)


def drop_table(conn, table):
    cursor = conn.cursor()

    try:
        cursor.execute(f"DROP TABLE IF EXISTS{table};")
        conn.commit()
    except Exception as e:
        print(e)


def import_extended_data(conn, file, data_dir, table):
    
    cursor = conn.cursor()

    print("IMPORTING EXTENDED DATA")

    data = []
    with open(f'{data_dir}/{file}') as f:
        data += json.load(f)


    for i,d in enumerate(data):
        endTime = d.get('ts')
        msPlayed = d.get('ms_played')
        trackName = d.get('master_metadata_track_name')
        artistName = d.get('master_metadata_album_artist_name')
        print(i, end='\r')

        try:
            cursor.execute(f"INSERT INTO {table} VALUES( %s, %s, %s, %s)", (
            endTime, msPlayed, trackName, artistName))
            conn.commit()
        except Exception as e:
            print(e)
            print(d)
            exit()
        
    conn.close()


def import_data(conn, file, data_dir, table):

    cursor = conn.cursor()

    print("IMPORTING DATA")
    
    data = []

    with open(f'{data_dir}/{file}') as f:
        data += json.load(f)

    cursor.execute(f"""SELECT endTime FROM {table} ORDER BY endTime DESC LIMIT 1;""")
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

    conn.close()


def get_json_files(dir, regex):
    data = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if regex.match(file):
                data.append(file)
    return data


def parse_arguments():
    
    parser = argparse.ArgumentParser(description='Imports Spotify data into a postgres database')
    parser.add_argument("-s", "--spotify-data", required=True,
       help="Data Directory with Spotify .json Files")
    parser.add_argument("-d", "--database", required=True,
       help="Database Name")
    parser.add_argument("-t", "--table", required=True,
       help="Table Name")
    parser.add_argument("-u", "--user", required=True,
       help="User to access the database")
    parser.add_argument("-p", "--password", required=True,
       help="Password to access the database")
    
    args = vars(parser.parse_args())

    data_dir = args['spotify_data']
    database = args['database']
    table = args['table']
    user = args['user']
    password = args['password']

    return data_dir, database, table, user, password 


if __name__=="__main__":
    main()
