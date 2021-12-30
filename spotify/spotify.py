import json

def main():
    
    data = []

    for i in 0,1,2,3,4:
        with open('data/endsong_' + str(i) + '.json') as f:
            data += json.load(f)

    artist_list = []
    song_list = []

    for d in data:
        ts = d.get('ts')
        if ("2021" in ts) or ("2020" in ts) or ("2019" in ts) or ("2018" in ts):
            artist_name = d.get('master_metadata_album_artist_name')
            
            if not artist_name == None:
                artist = get_artist(artist_list, artist_name)
                artist.playtime += d.get('ms_played')
                artist.playcount += 1

            song_name = d.get('master_metadata_track_name')
            
            if not song_name == None:
                song = get_song(song_list, song_name, artist_name)
                song.playtime += d.get('ms_played')
                song.playcount += 1


    artist_list.sort(key=lambda d: d.playtime, reverse=True)
    # song_list.sort(key=lambda d: d.playtime, reverse=True)

    # i = 0
    # print("MOST PLAYED SONGS BY PLAYTIME")
    # print("\n%4s %5s  %s" % ("TIME", "PLAYS", "NAME"))
    # for s in song_list:
        # s.print()
        # if i == 20:
            # break
        # i += 1
    
    i = 0
    print("\nMOST PLAYED ARTISTS BY PLAYTIME")
    print("\n%-4s%4s %5s  %-20s %s" % ("#", "TIME", "PLAYS", "ARTIST NAME", "MOST PLAYED SONG"))
    for a in artist_list:
        a.print(i, song_list)
        i += 1
        if i == 99:
            break




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
        self.song_playtime = song(None, None) 

    def print(self, i, song_list):
        i = i+1
        for s in song_list:
            if s.artist_name == self.name and s.playtime > self.song_playtime.playtime:
                self.song_playtime = s
        print("%02d: %4.0f %5d  %-20s %s (%.0f%%)" %
            (i, self.playtime / 60000, self.playcount, self.name, 
            self.song_playtime.name, (self.song_playtime.playtime/self.playtime) * 100))



def get_song(song_list, name, artist_name):
    for s in song_list:
        if s.name == name:
            return s
    
    s = song(name, artist_name)
    song_list.append(s)
    return s


class song:
    def __init__(self, name, artist_name):
        self.name = name
        self.artist_name = artist_name
        self.playtime = 0.0
        self.playcount = 0
        self.song_playtime = ""

    def print(self):


        print("%4.0f %5d  %s" %  (self.playtime / 60000, self.playcount, self.name))



if __name__=="__main__":
    main()        
