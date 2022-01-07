import json


def main():
    
    data = []

    for i in 0,1,2,3,4:
        with open('data/endsong_' + str(i) + '.json') as f:
            data += json.load(f)

    print_playtime_month(data, 2018, 2)
    print_artist_playstats_since(data, 2018, 2, 1, 50)


def get_months(data, start_year, start_month):
    months = []
    
    for d in data:

        year,month,day,hh,mm,ss = parse_date(d.get('ts'))
        
        if (year > start_year or
           (year == start_year and month >= start_month)):
            


def print_playtime_month(data, start_year, start_month):
    months = {}
    for d in data:

        year,month,day,hh,mm,ss = parse_date(d.get('ts'))
        
        if (year > start_year or
           (year == start_year and month >= start_month)):

            key = "%04d-%02d" % (year, month)

            if not key in months:
                months.update({key: 0}) 
            
            months[key] += d.get('ms_played')

    print("PLAYTIME SINCE %02d.%04d\n" % (start_month, start_year))
    
    month_objects = [] 
    for m in sorted(months):
        
        print("%s: " % m, end ="")
        playtime = months.get(m) / (1000*60*60)

        for i in range (0, round(playtime)):
            print("#", end="")  
        print(" (%.1fh)" % playtime)
    print()
    for m in month_objects:
        m.print_artists()


def print_artist_playstats_since(data, start_year, start_month, start_day, list_length):

    artist_list = []
    song_list = []

    for d in data:
            year,month,day,hh,mm,ss = parse_date(d.get('ts'))

            if ((year > start_year) or 
                (year == start_year and month > start_month) or 
                (year == start_year and month == start_month and day >= start_day)):
                
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

    print("\nMOST PLAYED ARTISTS BY PLAYTIME (SINCE %02d.%02d.%04d)" % (start_day, start_month, start_year))
    print("\n%-3s%4s %5s  %-20s %s" % ("##", "TIME", "PLAYS", "ARTIST NAME", "MOST PLAYED SONG"))
    for a in artist_list:
        a.print(i, song_list)
        i += 1
        if i == list_length: 
            break


def parse_date(ts):
        year,month,day = ts.split("-")
        time = day.split("T")[1].replace('Z', '', 1)
        day = day.split("T")[0]
        hh,mm,ss = time.split(":")
        return int(year), int(month), int(day), int(hh), int(mm), int(ss)


def get_artist_list(data, start, end):
    for d in data:
            year,month,day,hh,mm,ss = parse_date(d.get('ts'))
            this_date = "%04d%02d%02d" % (year,month,day)
            if int(start) <= int(this_date) <= int(end) :
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


    return artist_list.sort(key=lambda d: d.playtime, reverse=True)

def get_month(month_list, year, month, data):
    for m in month_list:
        if m.year == year and m.month == month:
            return m
    
    m = month(data, year, month)
    artist_list.append(a)
    return a

def get_artist(artist_list, name):
    for a in artist_list:
        if a.name == name:
            return a
    
    a = artist(name)
    artist_list.append(a)
    return a


def get_song(song_list, name, artist_name):
    for s in song_list:
        if s.name == name:
            return s
    
    s = song(name, artist_name)
    song_list.append(s)
    return s

class month:
    def __init__(self, data, year, month):
        self.year = year
        self.month = month
        artists = get_artist_list(data, "%04d%02d%02d" % (year,month,0), "%04d%02d%02d" % (year,month,32))
        
    def print_artists():
        for a in artists:
            print(a)

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
        print("%02d %4.0f %5d  %-20s %s (%.0f%%)" %
            (i, self.playtime / 60000, self.playcount, self.name, 
            self.song_playtime.name, (self.song_playtime.playtime/self.playtime) * 100))


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
