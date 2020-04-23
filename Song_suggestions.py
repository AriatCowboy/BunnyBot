import sqlite3


#connect = sqlite3.connect(':memory:')
conn = sqlite3.connect('Song_Suggestions.db')

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS song_suggestions (
				Author          text,
				Artist          text,
				Song            text,
				Chat            text)""")

def suggest(Author, Artist, Song, Chat):
	with conn:
		c.execute("INSERT INTO song_suggestions (Author, Artist, Song, Chat) VALUES (?, ?, ?, ?)", (str(Author), str(Artist), str(Song), str(Chat)))
		return True

async def suggestion(embed, ctx):
	with conn:
		embed.set_author(name='Song Suggestions')
		artist = []
		song = []
		c.execute("""SELECT * FROM song_suggestions""")
		for row in c.fetchall():
			if len(row) == 0:
				pass
			else:
				artist = row[1]
				song = row[2]
				embed.add_field(name=artist, value=song, inline=False)
				artist = ""
				song = ""
		await ctx.message.author.send(embed=embed) 

def twitch_suggestions():
	pass
#conn.commit()
#conn.close()