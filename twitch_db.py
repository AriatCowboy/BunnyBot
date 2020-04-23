import sqlite3


#connect = sqlite3.connect(':memory:')
conn = sqlite3.connect('Usernames.db')

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS usernames (
				Username text,
				ID integer PRIMARY KEY,
				is_mod text,
				is_subscriber text,
				subscriber text,
				channel text,
				name text)""")

def update_twitch(author):
	with conn:
		not_add = False
		author_username = author.display_name
		author_id = author.id
		author_mod = author.is_mod
		author_is_sub = author.is_subscriber
		author_sub = author.subscriber
		author_channel = author.channel
		author_name = author.name
		c.execute("""SELECT * FROM usernames WHERE ID = {}""".format(author_id))
		for row in c.fetchall():
			if row[0] == author_username:
				not_add = True
		user_data = [str(author_username), int(author_id), str(author_mod), str(author_is_sub), str(author_sub), str(author_channel), str(author_name)]
		update_user_data = ["Username", "ID", "is_mod", "is_subscriber", "subscriber", "channel", "name"]
		if not_add:
			c.execute("""SELECT * FROM usernames WHERE ID = {}""".format(author_id))
			for row in c.fetchall():
				i = 0				
				while i != 7:
					if row[0] == user_data[0]:
						if row[i] != user_data[i]:
							update = user_data[i]
							c.execute("""UPDATE usernames SET {} = ? Where {} = ?""".format(update_user_data[i], update_user_data[i]), (update, row[i]))
							update = ""
							print('Database has been updated.')								
						else:
							pass
						i += 1
					else:
						pass
		else:
			c.execute("INSERT INTO usernames (Username, ID, is_mod, is_subscriber, subscriber, channel, name) VALUES (?, ?, ?, ?, ?, ?, ?)", (str(author_username), int(author_id), str(author_mod), str(author_is_sub), str(author_sub), str(author_channel), str(author_name)))

def authorized_users(ctx):
	with conn:
		author_id = ctx.message.author.id
		try:
			c.execute("""SELECT * FROM usernames WHERE ID = {}""".format(author_id))
		except:
			pass
		for row in c.fetchall():
			if row[1] == author_id:
				return row[2]
			else:
				return author_id
