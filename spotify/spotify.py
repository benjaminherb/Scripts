import json

def main():
    
    data = []

    for i in 0,1,2,3,4:
        with open('data/endsong_' + str(i) + '.json') as f:
            data += json.load(f)

    artist_list = []
    song_list = []

    for d in data:
        artist_name = d.get('master_metadata_album_artist_name')
        
        if not artist_name == None:
            artist = get_artist(artist_list, artist_name)
            artist.playtime += d.get('ms_played')
            artist.playcount += 1

        song_name = d.get('master_metadata_track_name')
        
        if not song_name == None:
            song = get_song(song_list, song_name)
            song.playtime += d.get('ms_played')
            song.playcount += 1


    artist_list.sort(key=lambda d: d.playtime, reverse=True)
    song_list.sort(key=lambda d: d.playtime, reverse=True)

    i = 0
    print("MOST PLAYED SONGS BY PLAYTIME")
    for s in song_list:
        s.print()
        if i == 20:
            break
        i += 1
    
    i = 0
    print("\nMOST PLAYED ARTISTS BY PLAYTIME")
    for a in artist_list:
        a.print()
        if i == 20:
            break
        i += 1




def get_artist(artist_list, name):
    for a in artist_list:
        if a.name == name:
            return a
    
    a = artist(name)
    artist_list.append(a)
    return a


class artist:
    def __init__(self, name):
        self.name = name
        self.playtime = 0
        self.playcount = 0
        self.song_playtime = ""

    def print(self):
        print("T:%04.0f S:%04d  %s" %  (self.playtime / 60000, self.playcount, self.name))



def get_song(song_list, name):
    for s in song_list:
        if s.name == name:
            return s
    
    s = song(name)
    song_list.append(s)
    return s


class song:
    def __init__(self, name):
        self.name = name
        self.playtime = 0
        self.playcount = 0
        self.song_playtime = ""

    def print(self):
        print("T:%03.0f S:%03d  %s" %  (self.playtime / 60000, self.playcount, self.name))



if __name__=="__main__":
    main()        
