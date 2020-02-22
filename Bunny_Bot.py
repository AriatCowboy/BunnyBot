import discord
import time
import datetime
import asyncio
import os
import pickle
import ffmpeg
import youtube_dl
import emoji
from itertools import islice
from discord.ext import commands
from itertools import cycle
from discord.ext.commands import has_permissions, CheckFailure
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
from discord.message import Attachment

prefix = '!'
TOKEN = "NjgwMzMwODE4NDEzMTMzODU0.XlCkUA.71LO_3VVN6MmZVFie5svQ2JSqpY"
client = commands.Bot(command_prefix='!')
client.remove_command('help')
Bot_Location = "E:\\Coding_Practice\\Python\\BunnyBot_Divnes_Bot"
musicchannel = ["music-bot"]
bot_name = "BunnyBot"
Creator = "-=UNiTY=- AriatCowboy#0404"
Creator_ID = 149044658549424128
delay_log = 900
valid_users = [Creator]
play_music = [prefix + "yt", prefix + "clear", prefix + "queue", prefix + "pause", prefix + "resume", prefix + "volume", prefix + "join", prefix + "skip", prefix + "stop", prefix + "play"]
status = ["Music", "Type " + prefix + "help", "Type " + prefix + "music", "Chill Vibes", "Feed BunnyBot"]
players = []
queues = []
filenames = []
lines = []
bot_channel = "bunny-bot"

#initializes tha bot
@client.event
async def on_ready():
	print(f"Logged in as {client.user}, {client.user.name}, {client.user.id}")

#gets the name of the server
def get_guild_name(message):
	try:
		name = message.guild.name
		return name
	except:
		UnicodeEncodeError
	else:
		try:
			name = message.guild
			return name
		except:
			UnicodeEncodeError
		else:
			try:
				name = member.guild
				return name
			except:
				UnicodeEncodeError
			else:
				pass

def get_guild_id(message, log_location):
	guild_id_file = log_location + time.strftime('\\%m_%d_%y_GuildID.txt')
	if os.path.isfile(guild_id_file):
		pass
	else:
		try:	
			guild_id = message.guild.id
		except:
			UnicodeEncodeError
		else:
			try:		
				name = message.guild.name
			except:
				UnicodeEncodeError
		write_guild_id = open(guild_id_file, "w")
		with write_guild_id as wgidf:
			wgidf.write('Guild name: {}\n{}\n'.format(name, guild_id))


#creates a folder named as the server name for logging information
def get_log_location(message):
	name = get_guild_name(message)
	log_location = Bot_Location + "\\Logs\\{}_Logs".format(name)
	get_guild_id(message, log_location)
	if os.path.isdir(log_location):
		return log_location
	else:
		try:
			os.mkdir(log_location)
		except OSError:
			print ("Creation of the directory %s failed" % log_location)
		else:
			print ("Successfully created the directory %s " % log_location)
		return log_location

#reads the message count file that keeps track of how many messages were sent
def read_message_count():
	for guild in client.guilds:
		name = guild.name
		log_location = Bot_Location + "\\Logs\\{}_Logs".format(name)
		message_count_file = log_location + time.strftime('\\%m_%d_%y_Number_File.txt')
		message_count = 0
		if os.path.isfile(message_count_file):
			read_message_count_file = open(message_count_file, "rb")
			with read_message_count_file as wjf:
				message_count = pickle.load(read_message_count_file)
				return message_count
		else:
			return message_count

#writes the the file that keeps track of the amount of messages sent per day
def write_message_count(message):
	log_location = get_log_location(message)
	message_count_file = log_location + "\\" + time.strftime('\\%m_%d_%y_Number_File.txt')
	message_count = read_message_count() + 1
	with open(message_count_file, "wb") as f:
		pickle.dump(message_count, f)

#logs all the data into a easy to read format in a TXT file
def log_message_data(time, author, content, channel, message):
	log_location = get_log_location(message)
	message_history_file = log_location + time.strftime('\\%m_%d_%y_Chat_History.txt')
	try:
		if os.path.isfile(message_history_file):
			write_chat_history = open(message_history_file, "a")
			with write_chat_history as wch:
				wch.write('Time: {}\nAuthor: {}\nContent: {}\nChannel: {}\n\n'.format(time, author, content, channel))
		else:
			write_chat_history = open(message_history_file, "w")
			with write_chat_history as wch:
				wch.write('Time: {}\nAuthor: {}\nContent: {}\nChannel: {}\n\n'.format(time, author, content, channel))
	except:
		UnicodeEncodeError

#if someone tries to updata their nickname to the bots name it will not let them
@client.event
async def on_member_update(before, after):
	Creator_names = Creator
	nickname = after.nick
	last = before.nick
	if nickname:
		if nickname.lower().count(bot_name) > 0:
			if last:
				await after.edit(nick=last)
			else:
				await after.edit(nick="ThereCanOnlyBeOne")


#when a member joines the server gives the guest tab and keeps a log of it within a channel called guest-log
@client.event
async def on_member_join(member):
	write_joined_count(member)
	role = discord.utils.get(member.guild.roles, name='Guest')
	await member.add_roles(role)
	for channel in member.guild.channels:
		if str(channel) == "guest-log":
			await channel.send("{} has joined the community. Say Hi to the player and set their roles.".format(member.name))

#reads file that keeps track of the amount of member joined per day
def read_joined_count():
	joined = 0
	for guild in client.guilds:
		name = guild.name
		log_location = Bot_Location + "\\Logs\\{}_Logs".format(name)
		joined_file = log_location + "\\joinnumber.txt"
		if os.path.isfile(joined_file):
			read_joined_file = open(joined_file, "rb")
			with read_joined_file as wjf:
				joined = pickle.load(read_joined_file)
				return joined
		else:
			return joined

#writes the joined number to a file
def write_joined_count(member):
	joined = read_joined_count() + 1
	log_location = get_log_location(member)
	joined_file = log_location + "\\joinnumber.txt"
	with open(joined_file, "wb") as wjf:
		pickle.dump(joined, wjf)

#Writes to a log file
def open_log_file():
	time = datetime.datetime.now()
	message_count = read_message_count()
	joined = read_joined_count()
	for guild in client.guilds:
		name = guild.name
		log_location = Bot_Location + "\\Logs\\{}_Logs".format(name)
		log_file_location = log_location + time.strftime('\\%m_%d_%y_statistics.txt')
		if os.path.isfile(log_file_location):
			write_log = open(log_file_location, "a")
			with write_log as wl:
				wl.write('Time: {}, Message Count: {}, New Member Count: {}\n'.format(time, message_count, joined))
		else:
			write_log = open(log_file_location, "w")
			with write_log as wl:
				wl.write('Time: {}, Message Count: {}, New Member Count: {}\n'.format(time, message_count, joined))

#keeps track of the emojies added to posts and append it to the message history file
@client.event
async def on_reaction_add(reaction, user):
	reaction_convert = emoji.demojize(str(reaction))
	for channels in reaction.message.guild.channels:
		if channels.name == "logs":
			time = datetime.datetime.now()
			channel = reaction.message.channel
			await channels.send('Time: {}\nAuthor: {}\nContent: {}\nChannel: {}\nEmoji: {}\n\n'.format(time, user.name, reaction.message.content, channel, reaction_convert))
	time = datetime.datetime.now()
	log_location = get_log_location(reaction.message)
	message_history_file = log_location + time.strftime('\\%m_%d_%y_Chat_History.txt')
	print(reaction_convert)
	if os.path.isfile(message_history_file):
		write_chat_history = open(message_history_file, "a")
		with write_chat_history as wch:
			wch.write('Time: {}\nAuthor: {}\nContent: {}\nChannel: {}\nEmoji: {}\n\n'.format(time, user.name, reaction.message.content, channel, reaction_convert))
	else:
		write_chat_history = open(message_history_file, "w")
		with write_chat_history as wch:
			wch.write('Time: {}\nAuthor: {}\nContent: {}\nChannel: {}\nEmoji: {}\n\n'.format(time, user.name, reaction.message.content, channel, reaction_convert))

def read_bot_channel(message):
	log_location = get_log_location(message)
	bot_channel_file = log_location + "\\Bot_channel.txt"
	if os.path.isfile(bot_channel_file):
		read_bot_channel_file = open(bot_channel_file, "r")
		with read_bot_channel_file as rbcf:
			for line in rbcf:
				bot_channel = line
				return bot_channel

#checks if there is a curse word or someone using some sort of offensive language
@client.event
async def on_message(message):
	if message.author == client.user:
		return
	else:
		for channels in message.guild.channels:
			if channels.name == "logs":
				content = message.content
				author = message.author
				time = datetime.datetime.now()
				channel = message.channel
				await channels.send('Time: {}\nAuthor: {}\nContent: {}\nChannel: {}\n\n'.format(time, author, content, channel))
	bot_channel = read_bot_channel(message)	
	write_message_count(message)
	userID = message.author.id
	msg = message.content.lower()
	author = message.author
	content = message.content
	channel = message.channel
	time = datetime.datetime.now()
	print('{} {} {} {}'.format(time, channel, author, content))
	log_message_data(time, author, content, channel, message)
	open_log_file()
	if message.content == "!logoff":
		if message.author.id == Creator_ID:
			await client.process_commands(message)
		else:
			await message.author.send('You do not have permission to do that.')
	if str(channel) in musicchannel:
		for word in play_music:
			if msg.startswith(word):
				if message.author == client.user:
					return
				else:		
					await client.process_commands(message)

	if str(channel) == 'song-suggestions':
		if msg.startswith("!suggest") or msg.startswith("!suggestions"):
			await client.process_commands(message)

	elif str(channel) == 'bots-channel':
		await client.process_commands(message)

	elif message.author == client.user:
		return

	elif str(channel) == bot_channel:
		await client.process_commands(message)

	elif str(channel) == 'bot-command-center':
		await client.process_commands(message)

#changes the channel the bot will work in
@client.command()
async def bot_channel(ctx, channel):
	bot_channel = channel
	message = ctx.message
	log_location = get_log_location(message)
	bot_channel_file = log_location + "\\Bot_channel.txt"
	write_bot_channel_file = open(bot_channel_file, "w")
	with write_bot_channel_file as wbcf:
		wbcf.write(bot_channel)
		print(bot_channel)
		print('Appended file')


#feeds bunnybot
#@client.command()
#async def feed(ctx):
#	with open('Bunny Bot.png', 'rb') as f:
#		picture = discord.File(f)
#		await ctx.message.channel.send(picture)


#counts the amount of members on the server
@client.command()
async def usercount(ctx):
	await ctx.message.author.send(f"""Number of Members: {ctx.message.guild.member_count}""")

#Gives the user a status of everyone online, idle, and offline
@client.command()
async def report(ctx):
	message_channel = ctx.message.channel
	guild = ctx.message.guild
	online = 0
	idle = 0
	offline = 0
	for mem in guild.members:
		if str(mem.status) == "online":
			online += 1
		if str(mem.status) == "offline":
			offline += 1
		else:
			idle += 1
	author = ctx.message.author
	embed = discord.Embed(color=0xb663b6)
	embed.set_author(name='Status')
	embed.add_field(name="Online", value=online, inline=False)
	embed.add_field(name="Offline", value=offline, inline=False)
	embed.add_field(name="Idle", value=idle, inline=False)
	await ctx.message.author.send(embed=embed) 

@client.command()
async def suggestions(ctx):
	if ctx.message.author.id == ctx.message.guild.owner.id:
		message = ctx.message
		data_to_send = ""
		num_lines = 0
		authors = []
		contents = []
		author = ""
		content = ""

		embed = discord.Embed(color=0xb663b6)
		embed.set_author(name='Song Suggestions')

		log_location = get_log_location(message)
		suggestions_location = log_location + "\\" + 'suggestion.txt'
		if os.path.isfile(suggestions_location):
			read_suggest = open(suggestions_location, "r")
			with read_suggest as rs:
				for line in rs:
					lines = line.rstrip()
					data_to_send = data_to_send + lines
					if line.startswith("T") or line.startswith("A") or line.startswith("C"):
						data_to_send = data_to_send + "\n"			
						if line.startswith("Author: "):
							num_lines += 1
							for i in range(0, len(line)): 
								if i > 7: 
									author = author + line[i]
							authors.append(author)
							author = ""
						if line.startswith("Content: "):
							for i in range(0, len(line)): 
								if i > 8: 
									content = content + line[i]
							contents.append(content)
							content = ""
				i = 0
				while num_lines > 0:
					num_lines = num_lines - 1
					embed.add_field(name=authors[i], value=contents[i], inline=False)
					i += 1
			await ctx.message.author.send(embed=embed) 
		else:
			await ctx.message.author.send("There are no suggestions on file.")

#changes the bots status
async def change_status():
	await client.wait_until_ready()
	msgs = cycle(status)
	while not client.is_closed():
		current_status = next(msgs)
		await client.change_presence(activity=discord.Game(name=current_status))
		await asyncio.sleep(5)

#clears a certian amount of user defined messages
@client.command()
async def clear(ctx, amount):
	if ctx.message.author.id == ctx.message.guild.owner.id or str(ctx.author) in valid_users or ctx.message.author.guild_permissions.administrator:
		amount = int(amount)
		amount += 1
		channel = ctx.message.channel
		messages = []
		async for message in channel.history(limit=amount):
			messages.append(message)
		await channel.delete_messages(messages)
		await ctx.message.author.send('Messages Deleted!')
	else:
		await ctx.message.author.send('You do not have permission to do that.')

@client.command()
async def suggest(ctx, *args):
	output = ''
	time = datetime.datetime.now()
	author = ctx.message.author
	count = len(args)
	for word in args:
		output += word
		if count > 1:
			count = count - 1
			output += ' '
	channel = ctx.message.channel
	message = ctx.message
	log_location = get_log_location(message)
	suggestions_location = log_location + "\\" + 'suggestion.txt'
	if os.path.isfile(suggestions_location):
		write_suggest = open(suggestions_location, "a")
		with write_suggest as ws:
			ws.write('Time: {}\nAuthor: {}\nContent: {}\nChannel: {}\n\n'.format(time, author, output, channel))
			await ctx.send('Suggestion has been sent!')
	else:
		write_suggest = open(suggestions_location, "w")
		with write_suggest as ws:
			ws.write('Time: {}\nAuthor: {}\nContent: {}\nChannel: {}\n\n'.format(time, author, output, channel))
			await ctx.send('Suggestion has been sent!')

@client.command()
async def botsuggest(ctx, *args):
	output = ''
	time = datetime.datetime.now()
	author = ctx.message.author
	count = len(args)
	for word in args:
		output += word
		if count > 1:
			count = count - 1
			output += ' '
	channel = ctx.message.channel
	message = ctx.message
	log_location = get_log_location(message)
	suggestions_location = log_location + "\\" + "Bot_suggestion.txt"
	if os.path.isfile(suggestions_location):
		write_suggest = open(suggestions_location, "a")
		with write_suggest as ws:
			ws.write('Time: {}\nAuthor: {}\nContent: {}\nChannel: {}\n\n'.format(time, author, output, channel))
			await ctx.send('Suggestion has been sent!')
	else:
		write_suggest = open(suggestions_location, "w")
		with write_suggest as ws:
			ws.write('Time: {}\nAuthor: {}\nContent: {}\nChannel: {}\n\n'.format(time, author, output, channel))
			await ctx.send('Suggestion has been sent!')

#logs the bot offline
@client.command()
async def logoff(ctx):
	if ctx.message.author.id == Creator_ID:
		await ctx.message.author.send('Hello {0.author.mention}, I\'m Logging off!'.format(ctx))
		await client.close()
	else:
		await ctx.message.author.send('Hello {0.author.mention}, You dont have permission!'.format(ctx))

#displays the music bot help command
@client.command(pass_context=True)
async def help(ctx):
	author = ctx.message.author
	embed = discord.Embed(color=0xb663b6)
	embed.set_author(name='Help')
	embed.add_field(name=prefix + 'music', value='Displays music menu', inline=False)
	embed.add_field(name=prefix + 'usercount', value='Sends a DM of total amount of users', inline=False)
	embed.add_field(name=prefix + 'report', value='Shows how many users are online/offline/idle', inline=False)
	embed.add_field(name=prefix + 'clear', value='Clears messages at mass (Server owner/Admins/AriatCowboy)', inline=False)
	embed.add_field(name=prefix + 'suggestions', value='Sends all the suggestions (only Server owner)', inline=False)	
	embed.add_field(name=prefix + 'suggest', value='Adds the requested data to the Server owner. Please use artist - title', inline=False)	
	embed.add_field(name=prefix + 'botsuggest', value='Suggest updates or features for bot', inline=False)
	embed.add_field(name=prefix + 'logoff', value='Only AriatCowboy can use this, shuts down the bot entirly', inline=False)
	embed.add_field(name=prefix + 'bot_channel', value='changes the channel the bot works in. (Server Owner and Admin Only)', inline=False)
	await author.send(embed=embed) 

#displays the music bot help command
@client.command(pass_context=True)
async def music(ctx):
	author = ctx.message.author
	embed = discord.Embed(color=0xb663b6)
	embed.set_author(name='Help')
	embed.add_field(name=prefix + 'join', value='Joins server (must add channel name)', inline=False)
	embed.add_field(name=prefix + 'play', value='Plays a YouTube link', inline=False)
	embed.add_field(name=prefix + 'volume', value='Changes the volume', inline=False)
	embed.add_field(name=prefix + 'stop', value='Kicks bot from voice channel', inline=False)
	embed.add_field(name=prefix + 'queue', value='Adds song to queue', inline=False)	
	embed.add_field(name=prefix + 'pause', value='Pauses current song', inline=False)	
	embed.add_field(name=prefix + 'resume', value='Resumes current song', inline=False)
	embed.add_field(name=prefix + 'skip', value='Skips current song', inline=False)
	await author.send(embed=embed) 


# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '10.0.0.160' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
	def __init__(self, source, *, data, volume=0.1):
		super().__init__(source, volume)
		self.data = data
		self.title = data.get('title')
		self.url = data.get('url')

	@classmethod
	async def from_url(cls, url, *, loop=None, stream=True):
		loop = loop or asyncio.get_event_loop()
		data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
		if 'entries' in data:
			# take first item from a playlist
			data = data['entries'][0]
		filename = data['url'] if stream else ytdl.prepare_filename(data)
		return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


def check_queue(ctx, queues, players):
	if queues != []:
		player = queues.pop(0)
		players = player
		ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else check_queue(ctx, queues, players))

@client.command()
async def join(ctx, *, channel: discord.VoiceChannel):
	"""Joins a voice channel"""
	if ctx.voice_client is not None:
		return await ctx.voice_client.move_to(channel)
	if client.voice_client.is_connected() == True:
		await discord.VoiceChannel.connect(channel)
	else:
		print('is not connected to voice')

#plays a song from Youtube		
@client.command()
async def play(ctx, *, url):
	"""Plays from a url (almost anything youtube_dl supports)"""
	async with ctx.typing():
		player = await YTDLSource.from_url(url, loop=client.loop)
		players = player		
		ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else check_queue(ctx, queues, players))
		log_location = get_log_location(ctx.message)
		song_list_file = log_location + "\\Song_list.txt"
	volume = ctx.voice_client.source.volume
	volume = volume / 10
	await ctx.send('Now playing: {}'.format(player.title))


@client.command()
async def stream(ctx, *, url):
	"""Streams from a url (same as play, but doesn't predownload doesnt work atm)"""
	async with ctx.typing():
		player, filename = await YTDLSource.from_url(url, loop=client.loop, stream=True)
		players = player
		ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else check_queue(ctx, queues, players))
	volume = ctx.voice_client.source.volume
	volume = volume / 10
	await ctx.send('Now playing: {}'.format(player.title))

@client.command()
async def volume(ctx, volume: int):
	"""Changes the player's volume"""
	if ctx.voice_client is None:
		return await ctx.send("Not connected to a voice channel.")
	volume = ctx.voice_client.source.volume
	volume = volume / 10
	await ctx.send("Changed volume to {}%".format(volume))

@client.command()
async def queue(ctx, url):
	player = await YTDLSource.from_url(url)
	queues.append(player)
	await ctx.send('The song has been entered into the queue.')

@client.command()
async def stop(ctx):
	"""Stops and disconnects the bot from voice"""
	await client.voice_clients[0].disconnect()

@client.command()
async def pause(ctx):
	await ctx.voice_client.pause()

@client.command()
async def resume(ctx):
	await ctx.voice_client.resume()

@client.command()
async def skip(ctx):
	ctx.voice_client.stop()
	check_queue(ctx, queues, players)

@join.before_invoke
#@hp.before_invoke	
@queue.before_invoke
@play.before_invoke
async def ensure_voice(ctx):
	if ctx.voice_client is None:
		if ctx.author.voice:
			await ctx.author.voice.channel.connect()
		else:
			await ctx.send("You are not connected to a voice channel.")
			raise commands.CommandError("Author not connected to a voice channel.")
		
client.loop.create_task(change_status())
client.run(TOKEN)