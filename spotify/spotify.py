import json


data = []

for i in 0,1,2,3,4:
    with open('data/endsong_' + str(i) + '.json') as f:
        data += json.load(f)

#for d in data:
#    print("%s %s %s %f" % (d.get('ts'),d.get('master_metadata_track_name'),
#        d.get('master_metadata_album_artist_name'),d.get('ms_played')))

artists_playtime = {} 

for d in data:
    artist = d.get('master_metadata_track_name')
    playtime = d.get('ms_played')
    if artist not in artists_playtime:
        artists_playtime.update({artist: 0})
    
    artists_playtime[artist] += playtime

sorted_dict = dict(sorted(artists_playtime.items(), key= lambda x:x[1]))

for x, y in sorted_dict.items():
    print(x, y/1000/60) 


# print(artists_playtime["K.Flay"] / 1000 / 3600)
