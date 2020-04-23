import sqlite3

#connect = sqlite3.connect(':memory:')
connect = sqlite3.connect('Song_list.db')

c = connect.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS song_list (
                Artist          text,
                Song            text,
                Times_Played    integer,
                Last_Played     integer)""")

def insert_song(Artist, Song):
    with connect:
        c.execute("INSERT INTO song_list (Artist, Song) VALUES (?, ?)", (Artist, Song))
        return True        

def get_random_song(number):
    pass

def remove_song(song):
    pass


#connect.commit()
#connect.close()