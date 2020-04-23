import sqlite3
import datetime

#connect = sqlite3.connect(':memory:')
conn = sqlite3.connect('guild.db')

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS guild (
			Name_Guild text,
			ID integer PRIMARY KEY,
			AFK_channel text,
			AFK_timeout integer,
			Bit_rate_limit integer,
			Categories integer,
			Channels integer,
			Created_at text,
			Default_role text,
			Emoji_limit integer,
			Member_count integer,
			Owner text,
			Owner_id integer,
			Premium_subs_disco integer,
			Premium_tier integer,
			Roles integer,
			Rules_channel text,
			Text_channel integer,
			Voice_channel integer)""")

c.execute("""CREATE TABLE IF NOT EXISTS text_channels (
			ID Integer PRIMARY KEY,
			Name text,
			Position integer,
			NSFW text,
			News text,
			Category_ID Integer,
			Guild_id integer,
			FOREIGN KEY(Guild_id) REFERENCES guild(ID))""")

c.execute("""CREATE TABLE IF NOT EXISTS voice_channels (
			ID integer PRIMARY KEY,
			Name text,
			Position integer,
			Bitrate integer,
			User_Limit integer,
			Category_ID integer,
			Guild_id integer,
			FOREIGN KEY(Guild_id) REFERENCES guild(ID))""")

c.execute("""CREATE TABLE IF NOT EXISTS categories (
			ID integer PRIMARY KEY,
			Name text,
			Position integer,
			Guild_id integer,
			FOREIGN KEY(Guild_id) REFERENCES guild(ID))""")

c.execute("""CREATE TABLE IF NOT EXISTS users (
			Name text,
			Nickname text,
			ID integer PRIMARY KEY,
			Joined_datetime text,
			Premium_since text,
			Top_Role text,
			Guild_id integer)""")

c.execute("""CREATE TABLE IF NOT EXISTS banned_users (
			Name text,
			Nickname text,
			ID integer PRIMARY KEY,
			Guild_id integer,
			FOREIGN KEY(Guild_id) REFERENCES guild(ID))""")

c.execute("""CREATE TABLE IF NOT EXISTS authorized_users (
			Name text,
			User_ID integer,
			Guild_id integer,
			FOREIGN KEY(User_ID) REFERENCES users(ID),
			FOREIGN KEY(Guild_id) REFERENCES guild(ID))""")

c.execute("""CREATE TABLE IF NOT EXISTS logs (
			Author text,
			Author_ID integer,
			Message_ID integer,
			Cur_Time text,
			Content text,
			Guild_ID integer,
			Reaction text,
			FOREIGN KEY(Guild_id) REFERENCES guild(ID)
			FOREIGN KEY(Author_ID) REFERENCES users(ID))""")

c.execute("""CREATE TABLE IF NOT EXISTS count_data (
			Message_Num int,
			Join_Num int,
			Guild_id int,
			FOREIGN KEY(Guild_id) REFERENCES guild(ID))""")

c.execute("""CREATE TABLE IF NOT EXISTS bot_channel (
			Channel_name text,
			Guild_id int,
			FOREIGN KEY(Guild_id) REFERENCES guild(ID))""")


c.execute("""CREATE TABLE IF NOT EXISTS del_edit (
			Edit_Delete text,
			Author text,
			Cur_Time text,
			Content text,
			Updated_Content text,
			Channel text,
			Guild_ID integer,
			FOREIGN KEY(Guild_ID) REFERENCES guild(ID))""")

def update_guild_Info(Name_Guild, ID, AFK_channel, AFK_timeout, Bit_rate_limit, Categories, Channels, Created_at, Default_role, Emoji_limit, Member_count, Owner, Owner_id, Premium_subs_disco, Premium_tier, Roles, Rules_channel, Text_channel, Voice_channel):
	with conn:
		not_add = False
		guild_data = [Name_Guild, ID, AFK_channel, AFK_timeout, Bit_rate_limit, Categories, Channels, Created_at, Default_role, Emoji_limit, Member_count, Owner, Owner_id, Premium_subs_disco, Premium_tier, Roles, Rules_channel, Text_channel, Voice_channel]
		update_guild_data = ["Name_Guild", "ID", "AFK_channel", "AFK_timeout", "Bit_rate_limit", "Categories", "Channels", "Created_at", "Default_role", "Emoji_limit", "Member_count", "Owner", "Owner_id", "Premium_subs_disco", "Premium_tier", "Roles", "Rules_channel", "Text_channel", "Voice_channel"]
		c.execute("""SELECT * FROM guild""")
		for row in c.fetchall():
			if row[1] == guild_data[1]:
				not_add = True
		if not_add == True:
			c.execute("""SELECT * FROM guild WHERE ID={}""".format(ID))
			for row in c.fetchall():
				i = 0
				while i != 19:
					if row[1] == guild_data[1]:
						if row[i] != guild_data[i]:
							update = guild_data[i]
							c.execute("""UPDATE guild SET {} = ? Where {} = ?""".format(update_guild_data[i], update_guild_data[i]), (update, row[i]))
							update = ""
							print('Database has been updated.')
						else:
							pass
						i += 1
					else:
						pass

		else:
			c.execute("""INSERT INTO guild (Name_Guild, ID, AFK_channel, AFK_timeout, Bit_rate_limit, Categories, Channels, Created_at, Default_role, Emoji_limit, Member_count, Owner, Owner_id, Premium_subs_disco, Premium_tier, Roles, Rules_channel, Text_channel, Voice_channel) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (Name_Guild, ID, AFK_channel, AFK_timeout, Bit_rate_limit, Categories, Channels, Created_at, Default_role, Emoji_limit, Member_count, Owner, Owner_id, Premium_subs_disco, Premium_tier, Roles, Rules_channel, Text_channel, Voice_channel))

   
def update_voice_channel_info(ID, Name, Position, Bitrate, User_Limit, Category_ID, Guild_id):
	with conn:
		not_add = False
		channel_data = [ID, Name, Position, Bitrate, User_Limit, Category_ID, Guild_id]
		update_channel_data = ["ID", "Name", "Position", "Bitrate", "User_Limit", "Category_ID", "Guild_id"]
		c.execute("""SELECT * FROM voice_channels""")
		for row in c.fetchall():
			if row[0] == channel_data[0]:
				not_add = True
		if not_add:
			c.execute("""SELECT * FROM voice_channels WHERE ID={}""".format(ID))
			for row in c.fetchall():
				i = 0	
				while i != 7:
					if row[0] == channel_data[0]:
						if row[i] != channel_data[i]:
							update = channel_data[i]
							c.execute("""UPDATE voice_channels SET {} = ? Where {} = ?""".format(update_channel_data[i], update_channel_data[i]), (update, row[i]))
							update = ""
							print('Database has been updated.')
						else:
							pass
						i += 1
					else:
						pass

		else:
			c.execute("""INSERT INTO voice_channels (ID, Name, Position, Bitrate, User_Limit, Category_ID, Guild_id) VALUES(?, ?, ?, ?, ?, ?, ?)""", (ID, Name, Position, Bitrate, User_Limit, Category_ID, Guild_id))

def update_category_info(cat_ID, name, cat_position, guild_ID):
	with conn:
		not_add = False
		cat_data = [cat_ID, name, cat_position, guild_ID]
		update_cat_data = ["cat_ID", "name", "cat_position", "guild_ID"]
		c.execute("""SELECT * FROM categories""")
		for row in c.fetchall():
			if row[0] == cat_data[0]:
				not_add = True
		if not_add:
			c.execute("""SELECT * FROM categories WHERE ID={}""".format(cat_ID))
			for row in c.fetchall():
				i = 0
				while i != 4:
					if row[0] == cat_data[0]:
						if row[i] != cat_data[i]:
							update = cat_data[i]
							c.execute("""UPDATE categories SET {} = ? Where {} = ?""".format(update_cat_data[i], update_cat_data[i]), (update, row[i]))
							update = ""
							print('Database has been updated.')
						else:
							pass
						i += 1
					else:
						pass
		else:
			c.execute("""INSERT INTO categories (ID, Name, Position, guild_ID) VALUES(?, ?, ?, ?)""", (cat_ID, name, cat_position, guild_ID))

def update_ban_info(Name, nickname, ID, Guild_id):
	with conn:
		not_add = False
		ban_data = [Name, nickname, ID, Guild_id]
		update_ban_data = ["Name", "nickname", "ID", "Guild_id"]
		c.execute("""SELECT * FROM banned_users""")
		for row in c.fetchall():
			if row[2] == ban_data[2]:
				not_add = True
		if not_add:
			c.execute("""SELECT * FROM banned_users WHERE ID={}""".format(ID))
			for row in c.fetchall():
				i = 0
				while i != 4:
					if row[2] == ban_data[2]:
						if row[i] != ban_data[i]:
							update = ban_data[i]
							c.execute("""UPDATE banned_users SET {} = ? Where {} = ?""".format(update_ban_data[i], update_ban_data[i]), (update, row[i]))
							update = ""
							print('Database has been updated.')
						else:
							pass
						i += 1
					else:
						pass
		else:
			c.execute("""INSERT INTO banned_users (Name, nickname, id, Guild_id) VALUES(?, ?, ?, ?, ?, ?, ?)""", (Name, nickname, ID, Guild_id))

def update_text_channels_info(ID, Name, Position, NSFW, News, Category_ID, Guild_id):
	with conn:
		not_add = False
		channel_data = [ID, Name, Position, NSFW, News, Category_ID, Guild_id]
		update_channel_data = ["ID", "Name", "Position", "NSFW", "News", "Category_ID", "Guild_id"]
		c.execute("""SELECT * FROM text_channels""")
		for row in c.fetchall():
			if row[0] == channel_data[0]:
				not_add = True
		if not_add:
			c.execute("""SELECT * FROM text_channels WHERE ID={}""".format(ID))
			for row in c.fetchall():
				i = 0
				while i != 7:
					if row[0] == channel_data[0]:
						if row[i] != channel_data[i]:
							update = channel_data[i]
							c.execute("""UPDATE text_channels SET {} = ? Where {} = ?""".format(update_channel_data[i], update_channel_data[i]), (update, row[i]))
							update = ""
							print('Database has been updated.')
						else:
							pass
						i += 1
					else:
						pass
		else:
			c.execute("""INSERT INTO text_channels (ID, Name, Position, NSFW, News, Category_ID, Guild_id) VALUES(?, ?, ?, ?, ?, ?, ?)""", (ID, Name, Position, NSFW, News, Category_ID, Guild_id))

def update_member_info(mem_name, mem_nick, mem_id, mem_joined_date, mem_premium_since, mem_topRole, guild_ID):
	with conn:
		not_add = False
		user_data = [mem_name, mem_nick, mem_id, mem_joined_date, mem_premium_since, mem_topRole, guild_ID]
		update_user_data = ["Name", "Nickname", "ID", "Joined_datetime", "Premium_since", "Top_Role", "Guild_id"]
		c.execute("""SELECT * FROM users WHERE ID={} AND Guild_id = {}""".format(mem_id, guild_ID))
		for row in c.fetchall():
			if row[2] == user_data[2]:
				not_add = True
				print("not add")
			else:
				pass
		if not_add:
			c.execute("""SELECT * FROM users WHERE ID={} AND Guild_id = {}""".format(mem_id, guild_ID))
			for row in c.fetchall():
				i = 0				
				while i != 7:
					print("not add")
					if row[0] == user_data[0]:
						if row[i] != user_data[i]:
							update = user_data[i]
							c.execute("""UPDATE users SET {} = ? Where {} = ?""".format(update_user_data[i], update_user_data[i]), (update, row[i]))
							update = ""
							print('Database has been updated.')
						else:
							pass
						i += 1
					else:
						pass
		else:
			c.execute("""INSERT INTO users (Name, Nickname, id, joined_datetime, premium_since, top_role, Guild_id) VALUES(?, ?, ?, ?, ?, ?, ?)""", (mem_name, mem_nick, mem_id, mem_joined_date, mem_premium_since, mem_topRole, guild_ID))

def update_authorized_users(Name, ID, Guild_id):
	with conn:
		not_add = False
		user_data = [Name, ID, Guild_id]
		update_user_data = ["Name", "User_ID", "Guild_id"]
		c.execute("""SELECT * FROM users""")
		for row in c.fetchall():
			if row[1] == user_data[1]:
				not_add = True
		if not_add:
			c.execute("""SELECT * FROM users WHERE ID={}""".format(ID))
			for row in c.fetchall():
				i = 0				
				while i != 3:
					if row[0] == user_data[0]:
						if row[i] != user_data[i]:
							update = user_data[i]
							c.execute("""UPDATE users SET {} = ? Where {} = ?""".format(update_user_data[i], update_user_data[i]), (update, row[i]))
							update = ""
							print('Database has been updated.')
						else:
							pass
						i += 1
					else:
						pass
		else:

			c.execute("""INSERT INTO users (Name, Nickname, id, joined_datetime, premium_since, top_role, Guild_id) VALUES(?, ?, ?, ?, ?, ?, ?)""", (mem_name, mem_nick, mem_id, mem_joined_date, mem_premium_since, mem_topRole, guild_ID))

def get_authorized_users(ID):
	with conn:
		authorized_users = 149044658549424128
		c.execute("""SELECT * FROM authorized_users WHERE User_ID={}""".format(ID))
		for row in c.fetchall():
			authorized_users = [row[1]]
		return authorized_users

def check_users(Name):
	with conn:
		user_id = ""
		name = Name.split()
		c.execute("""SELECT * FROM users""")
		for row in c.fetchall():
			if str(row[0]) == str(Name):
				user_id = str(row[2])
		return int(user_id)

def update_authorized_users(content, user_id, guild_ID):
	with conn:
		not_add = ""
		try:
			c.execute("""SELECT * FROM authorized_users WHERE Name = {}""".format(str(content)))
		except:
			pass
		for row in c.fetchall():
			if row[0] == content:
				not_add = True
		user_data = [content, user_id, guild_ID]
		update_user_data = ["Name", "User_ID", "Guild_id"]
		if not_add:
			c.execute("""SELECT * FROM authorized_users WHERE ID=(?)""", User_id)
			for row in c.fetchall():
				i = 0				
				while i != 3:
					if row[0] == user_data[0]:
						if row[i] != user_data[i]:
							update = user_data[i]
							c.execute("""UPDATE users SET {} = ? Where {} = ?""".format(update_user_data[i], update_user_data[i]), (update, row[i]))
							update = ""
							print('Database has been updated.')
						else:
							pass
						i += 1
					else:
						pass
		else:
			c.execute("""INSERT INTO authorized_users (Name, User_ID, Guild_id) VALUES(?, ?, ?)""", (content, user_id, guild_ID))

def update_logs(message):
	author = message.author
	author_id = author.id
	message_id = message.id
	cur_time = datetime.datetime.now()
	content = message.content
	guild_id = message.author.guild.id
	with conn:
		c.execute("""INSERT INTO logs (Author, Author_ID, Message_ID, Cur_Time, Content, Guild_ID) VALUES(?, ?, ?, ?, ?, ?)""", (str(author), int(author_id), int(message_id), str(cur_time), str(content), int(guild_id)))

def update_message_count(message):
	with conn:
		print(message.content)

		guild_id = message.author.guild.id
		Message_Num = 0
		Join_Num = 0
		c.execute("""SELECT * FROM count_data WHERE Guild_id = {}""".format(guild_id))
		for row in c.fetchall():
			Message_Num = row[0]
			Join_Num = row[1]
			Message_Num += 1
		if Message_Num > 0:
			ok = True
		else:
			ok = False
		if ok:
			c.execute("""INSERT INTO count_data (Message_Num, Join_Num, Guild_id) VALUES (?, ?, ?)""", (Message_Num, Join_Num, guild_id))
		else:
			Message_Num = 1
			join_num = 0
			c.execute("""INSERT INTO count_data (Message_Num, Join_Num, Guild_id) VALUES (?, ?, ?)""", (Message_Num, Join_Num, guild_id))

def botchannel(channel, ctx):
	with conn:
		guild_id = ctx.message.author.guild.id
		c.execute("""SELECT * FROM bot_channel WHERE Guild_id = {}""".format(guild_id))
		for row in c.fetchall():
			if row == 0:
				guild_id = ctx.message.author.guild.id
				c.execute("""INSERT INTO bot_channel (bot_channel, Guild_id) VALUES (?, ?)""", (channel, guild_id))
			else:
				old_channel = row[0]
				c.execute("""UPDATE bot_channel set Channel_name = ? WHERE Channel_name = ?""", (str(channel), str(old_channel)))
		return True

def readbotchannel(message):
	with conn:
		bot_channel = ""
		guild_id = message.author.guild.id
		c.execute("""SELECT * FROM bot_channel WHERE Guild_id = {}""".format(guild_id))
		for row in c.fetchall():
			bot_channel = row[0]
		if len(bot_channel) == 0:
			bot_channel = message.channel
			c.execute("""INSERT INTO bot_channel (Channel_name, Guild_id) VALUES (?, ?)""", (str(bot_channel), int(guild_id)))
			return bot_channel
		else:
			bot_channel = message.channel
			return bot_channel

def log_reaction(reaction, user):
	author = user.name
	author_id = user.id
	message_id = reaction.message.id
	cur_time = datetime.datetime.now()
	content = reaction.message.content
	guild_id = reaction.message.author.guild.id
	with conn:
		c.execute("""INSERT INTO logs (Author, Author_ID, Message_ID, Cur_Time, Content, Guild_ID, Reaction) VALUES(?, ?, ?, ?, ?, ?, ?)""", (str(author), int(author_id), int(message_id), str(cur_time), str(content), int(guild_id), str(reaction)))

def update_message_edit(author, channel, time, content, updated_content):
	with conn:
		edit = "EDIT"
		guild_id = author.guild.id	
		c.execute("""INSERT INTO del_edit (Edit_Delete, Author, Cur_Time, Content, Updated_Content, Channel, Guild_ID) VALUES (?, ?, ?, ?, ?, ?, ?)""", (str(edit), str(author), str(time), str(content), str(updated_content), str(channel), int(guild_id)))

def update_message_delete(author, channel, time, content):
	with conn:
		delete = "DELETE"
		guild_id = author.guild.id	
		c.execute("""INSERT INTO del_edit (Edit_Delete, Author, Cur_Time, Content, Channel, Guild_ID) VALUES (?, ?, ?, ?, ?, ?)""", (str(delete), str(author), str(time), str(content), str(channel), int(guild_id)))

#conn.commit()
#conn.close()