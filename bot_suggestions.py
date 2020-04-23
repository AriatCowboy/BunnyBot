import sqlite3
import datetime

#connect = sqlite3.connect(':memory:')
conn = sqlite3.connect('bot_suggestions.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS bot_suggestions (
			Cur_Time text,
			Author text,
			Content text,
			Channel text)""")

def bot_suggestion(message, Channel):	
	Cur_Time = datetime.datetime.now()
	Author = message.author
	Content = message.content
	Content = Content.split(" ", 1)
	Content = Content[1]
	with conn:
		c.execute("""INSERT INTO bot_suggestions (Cur_Time, Author, Content, Channel) VALUES(?, ?, ?, ?)""", (str(Cur_Time), str(Author), str(Content), str(Channel)))
