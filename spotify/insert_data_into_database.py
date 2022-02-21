import json
import psycopg2

data = []

for i in 0,1,2,3,4:
    with open('data/endsong_' + str(i) + '.json') as f:
        data += json.load(f)


conn = psycopg2.connect(
    database="spotify",
    user='ben',
    password='postgres',
    #host='localhost',
    #port='5432'
)

cursor = conn.cursor()

for i,d in enumerate(data):
    ts = d.get('ts')
    username = d.get('username')
    platform =  d.get('platform')
    ms_played = d.get('ms_played')
    conn_country = d.get('conn_country')
    ip_addr_decrypted = d.get('ip_addr_decrypted')
    user_agent_decrypted = d.get('user_agent_decrypted')
    master_metadata_track_name = d.get('master_metadata_track_name')
    master_metadata_album_artist_name = d.get('master_metadata_album_artist_name')
    master_metadata_album_album_name = d.get('master_metadata_album_album_name')
    spotify_track_uri = d.get('spotify_track_uri')
    episode_name = d.get('episode_name')
    episode_show_name = d.get('episode_show_name')
    spotify_episode_uri = d.get('spotify_episode_uri')
    reason_start = d.get('reason_start')
    reason_end = d.get('reason_end')
    shuffle = d.get('shuffle')
    skipped = d.get('skipped')
    offline = d.get('offline')
    offline_timestamp = d.get('offline_timestamp')
    incognito_mode = d.get('incognito_mode')
    print(i)

    try:
        cursor.execute("INSERT INTO streams VALUES( \
            %s, %s, %s, \
            %s, %s, %s, \
            %s, %s, %s, \
            %s, %s, %s, \
            %s, %s, %s, \
            %s, %s, %s, \
            %s, %s, %s)", (
            ts, username, platform, 
            ms_played, conn_country, ip_addr_decrypted, 
            user_agent_decrypted, master_metadata_track_name, master_metadata_album_artist_name, 
            master_metadata_album_album_name, spotify_track_uri, episode_name, 
            episode_show_name, spotify_episode_uri, reason_start, 
            reason_end, shuffle, skipped, 
            offline, offline_timestamp, incognito_mode
            ))
        
        conn.commit()
    except Exception as e:
        print(e)
        print(d)
        exit()

conn.close()


