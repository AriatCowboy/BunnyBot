import discord
import time
import datetime
import asyncio
import os
import pickle
import ffmpeg
import youtube_dl
import emoji
import discord
import http
from Discord_db import update_guild_Info, update_ban_info, update_text_channels_info, update_voice_channel_info, update_category_info, update_member_info, update_authorized_users, get_authorized_users, check_users, update_authorized_users, update_logs, update_message_count, botchannel, readbotchannel, log_reaction, update_message_edit, update_message_delete
from Song_suggestions import suggest, conn, suggestion
from Song_List import connect, insert_song
from bot_suggestions import bot_suggestion
from discord.ext import commands
from itertools import cycle
from discord.ext.commands import has_permissions, CheckFailure
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
from discord.message import Attachment

prefix = '!'
TOKEN = "NTY3MTYxNzczMjM3NzMxMzMw.Xk4eRg.3WDE9GXOTJuds34EYfQvjMrRLQc"
client = commands.Bot(command_prefix='!')
client.remove_command('help')
Bot_Location = "E:\\Coding_Practice\\Python\\BunnyBot_Divnes_Bot"
bot_name = "BunnyBot"
Creator = "-=UNiTY=- AriatCowboy#0404"
Creator_ID = 149044658549424128
valid_users = [Creator]
status = ["Music", "Type " + prefix + "help", "Type " + prefix + "music", "Chill Vibes", "Feed BunnyBot"]
play_music = [prefix + "yt", prefix + "clear", prefix + "queue", prefix + "pause", prefix + "resume", prefix + "volume", prefix + "join", prefix + "skip", prefix + "stop", prefix + "play"]
players = []
queues = []
filenames = []
lines = []
authorized_users = []

#initializes tha bot
@client.event
async def on_ready():
	print(f"Logged in as {client.user}, {client.user.name}, {client.user.id}")

#updates all data for discord database.
#Everything from here down till the next
#comment is apart of this section
async def update_database(message):
	guild_name = message.author.guild
	await Get_update_guild(guild_name)
	await Get_update_text_channels(message)
	await Get_update_voice_channels(message)
	await Get_update_cat(message)
	await Get_update_users(message)
	await Get_update_ban(message)
	await update_logs(message)

async def Get_update_guild(guild_name):
	guild = guild_name
	guild_id  = guild.id
	afk_channel = guild.afk_channel
	afk_timeout = guild.afk_timeout
	bans = await guild.bans()
	ban_num = 0
	for ban in bans:
		ban_num += 1
	bitrate = guild.bitrate_limit
	categories = guild.categories
	cat_num = 0
	for cat in categories:
		cat_num += 1
	textchannels = guild.text_channels
	txt_num = 0
	for txt in textchannels:
		txt_num += 1
	voicechannel = guild.voice_channels
	voi_num = 0
	for voice in voicechannel:
		voi_num += 1
	channels = voi_num + cat_num + txt_num
	created_date = guild.created_at
	defaultrole = str(guild.default_role)
	defaultrole = defaultrole.replace( "@", "")
	emoji_num = guild.emoji_limit
	member_count = guild.member_count
	guild_owner = guild.owner
	Guild_owner_id = guild.owner_id
	premium_num_subs_disco = guild.premium_subscription_count
	premium_teir = guild.premium_tier
	guild_role_count = guild.roles
	role_num = 0
	for role in guild_role_count:
		role_num += 1
	channel_rule = guild.rules_channel
	update_guild_Info(str(guild_name), int(guild_id), str(afk_channel), int(afk_timeout), int(bitrate), int(cat_num), int(channels), str(created_date), str(defaultrole), int(emoji_num), int(member_count), str(guild_owner), int(Guild_owner_id), int(premium_num_subs_disco), int(premium_teir), int(role_num), str(channel_rule), int(txt_num), int(voi_num))

async def Get_update_ban(message):
	guild_ID = message.guild.id
	banned_members = await message.guild.bans()
	for ban_user in banned_members:
		name = ban_user.display_name
		nick = ban_user.nick
		ID = ban_user.id
		update_ban_info(name, nick, ID, guild_ID)

async def Get_update_users(message):
	guild_ID = message.guild.id
	for mem in message.guild.members:
		mem_name = mem.display_name
		mem_nick = mem.nick
		mem_id = mem.id
		mem_joined_date = mem.joined_at
		mem_premium_since = mem.premium_since
		mem_topRole = mem.top_role
		update_member_info(str(mem_name), str(mem_nick), int(mem_id), str(mem_joined_date), str(mem_premium_since), str(mem_topRole), int(guild_ID))

async def Get_update_cat(message):
	guild_ID = message.guild.id
	for cat in message.guild.categories:
		cat_ID = cat.id
		cat_name = cat.name
		cat_position = cat.position
		update_category_info(cat_ID, cat_cane, cat_position, guild_ID)

async def Get_update_text_channels(message):
	guild_ID = message.guild.id
	for channel in message.guild.text_channels:
		channel_ID = channel.id
		channel_name = channel.name
		channel_pos = channel.position
		channel_NSFW = channel.nsfw
		channel_News = channel.is_news()
		try:
			channel_cat = channel.category.id
		except:
			channel_cat = None
		update_text_channels_info(int(channel_ID), str(channel_name), int(channel_pos), str(channel_NSFW), str(channel_News), str(channel_cat), int(guild_ID))

async def Get_update_voice_channels(message):
	guild_ID = message.guild.id
	for channel in message.guild.voice_channels:
		channel_ID = channel.id
		channel_name = channel.name
		channel_pos = channel.position
		channel_BR = channel.bitrate
		channel_userLimit = channel.user_limit
		try:
			channel_cat = channel.category.id
		except:
			channel_cat = None
		update_voice_channel_info(channel_ID, channel_name, channel_pos, channel_BR, channel_userLimit, channel_cat, guild_ID)

#changes the bots status
async def change_status():
	await client.wait_until_ready()
	msgs = cycle(status)
	while not client.is_closed():
		current_status = next(msgs)
		await client.change_presence(activity=discord.Game(name=current_status))
		await asyncio.sleep(5)

#logs the bot offline
@client.command()
async def logoff(ctx):
	if ctx.message.author.id == Creator_ID:
		await ctx.message.author.send('Hello {0.author.mention}, I\'m Logging off!'.format(ctx))
		await client.close()
	else:
		await ctx.message.author.send('Hello {0.author.mention}, You dont have permission!'.format(ctx))

#Gives user mod perms with the bot
@client.command()
async def mod_user(ctx):
	content = ctx.message.content
	username = ctx.message.content
	content = content.split(" ", 1)
	new_content = content[1]
	user_id = check_users(new_content)
	if user_id == "":
		print("Does not exist!")
	else:
		guild_id = ctx.message.author.guild.id
		update_authorized_users(new_content, user_id, guild_id)

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

@client.event
async def on_message_delete(message):
	time = datetime.datetime.now()
	content = message.content
	author = message.author
	channel = message.channel
	for guild in client.guilds:
		if guild.id == message.guild.id:
			for channels in guild.channels:
				if channels.name == "logs":
					if author == client.user:
						pass
					else:
						update_message_delete(author, channel, time, content)
						embed = discord.Embed(color=0xb663b6)
						embed.set_author(name=author)
						embed.add_field(name="Time", value=time, inline=False)
						embed.add_field(name="content", value=content, inline=False)
						embed.add_field(name="channel", value=channel, inline=False)
						await channels.send(embed=embed) 

@client.event
async def on_message_edit(before, after):
	author = before.author
	if author == client.user:
		pass
	else:
		content = before.content
		time = datetime.datetime.now()
		channel = before.channel
		updated_content	= after.content
		for guild in client.guilds:
			if guild.id == before.guild.id:
				for channels in guild.channels:
					if channels.name == "logs":
						update_message_edit(author, channel, time, content, updated_content)
						embed = discord.Embed(color=0xb663b6)
						embed.set_author(name=author)
						embed.add_field(name="Channel", value=channel, inline=False)
						embed.add_field(name="Time", value=time, inline=False)
						embed.add_field(name="content", value=content, inline=False)
						embed.add_field(name="Updated Content", value=updated_content, inline=False)
						await channels.send(embed=embed)

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

#keeps track of the emojies added to posts and append it to the message history file
@client.event
async def on_reaction_add(reaction, user):
	reaction_convert = emoji.demojize(str(reaction))
	time = datetime.datetime.now()
	log_reaction(reaction, user)

#changes the channel the bot will work in
@client.command()
async def bot_channel(ctx):
	message = ctx.message
	channel = message.content.split(" ", 1)
	channel = channel[1]
	botchannel(channel, ctx)
	await ctx.send("channel changed to {}".format(channel))

#adds a song to the DB
@client.command()
async def addsl(ctx):
	message = ctx.message
	author = message.author
	content = message.content
	if author.id == message.guild.owner.id or str(author) in valid_users or author.guild_permissions.administrator:
		seperate = content.split(" ", 1)
		print(seperate)
		Artist_song = seperate[1].split("-", 1)
		print(Artist_song)
		Artist = Artist_song[0]
		print(Artist)
		try:
			Song = Artist_song[1]
		except:
			await ctx.send("Please check what you entered. I need the song in Artist - Song format.")
		else:
			Song = Artist_song[1]
			num = len(Artist) - 1
			reply = insert_song(Artist[:num], Song[1:])
			if reply:
				await author.send("{} {} - {} was added to the song database!".format(author, Artist[:num], Song[1:]))
			else:
				await author.send("{} Please use the format Artist - Song.".format(author))

#adds suggestions for the bot to a DB
@client.command()
async def botsuggest(ctx):
	message = ctx.message
	Channel = "Discord"
	bot_suggestion(message, Channel)

#Adds a song to the Song Suggestions DB
@client.command()
async def ss(ctx):
	message = ctx.message
	author = message.author
	content = message.content
	content = content.split(" ", 1)
	content = content[1]
	try:
		content = content.split("-", 1)
	except:
		await ctx.send("Please enter in Artist - Song format. Thanks!")
		return
	artist = content[0]
	artist = artist.split(" ", 1)
	new_aritst = artist[0]
	artist = new_aritst
	try:
		song = content[1]
	except:
		await ctx.send("Please enter in Artist - Song format. Thanks!")
		return
	chat = "Discord"
	worked = suggest(author, artist, song, chat)
	if worked:
		await ctx.send("Song has been added.")
	else:
		await ctx.send("Something Went Wrong! Please try again or DM AriatCowboy!")

#send a list of songs to the server owner
@client.command()
async def suggestions(ctx):
	embed = discord.Embed(color=0xb663b6)
	await suggestion(embed, ctx)

#clears a certian amount of user defined messages
@client.command()
async def clear(ctx, amount):
	author = ctx.message.author
	amount = int(amount)
	amount += 1
	channel = ctx.message.channel
	messages = []
	async for message in channel.history(limit=amount):
		messages.append(message)
	await channel.delete_messages(messages)
	await ctx.message.author.send('Messages Deleted!')

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	bot_channel = readbotchannel(message)
	await update_message_count(message)
	author = message.author
	content = message.content
	channel = message.channel
	musicchannel = "music-bot"
	time = datetime.datetime.now()
	print('{} {} {} {}'.format(time, channel, author, content))
	await update_database(message)
	authorized_users = get_authorized_users(author.id)
	if message.content.startswith("!mod_user"):
		if author.id in authorized_users:
			await client.process_commands(message)
		else:
			await channel.send('You do not have permission to do that.')
	elif content == "!logoff":
		if author.id in authorized_users:
			await client.process_commands(message)
		else:
			await channel.send('You do not have permission to do that.')
	elif content == "!bot_channel":
		if author.id in authorized_users:
			await client.process_commands(message)
		else:
			await channel.send('You do not have permission to do that.')
	elif str(channel) == musicchannel:
		for word in play_music:
			if content.startswith(word):
				if message.author == client.user:
					return
				else:		
					await client.process_commands(message)
	elif str(channel) == 'song-suggestions':
		if content.startswith("!ss") or content.startswith("!suggestions") or content.startswith("!clear"):
			if author.id in authorized_users:
				await client.process_commands(message)
			else:
				await channel.send('You do not have permission to do that.')
	elif str(channel) == bot_channel:
		await client.process_commands(message)

#displays the Admin bot help command
@client.command(pass_context=True)
async def admin(ctx):
	author = ctx.message.author
	embed = discord.Embed(color=0xb663b6)
	embed.set_author(name='Admin')
	embed.add_field(name=prefix + 'logoff', value='Restarts Bunny Bot.', inline=False)
	embed.add_field(name=prefix + 'mod_user', value='Allows user to have access to mod perms in bot. Do Not Use Nick Names !mod_user <display_name>', inline=False)
	embed.add_field(name=prefix + 'addsl', value='Adds a song to the Song List DB for Divne to sing during streams.', inline=False)
	embed.add_field(name=prefix + 'bot_channel', value='changes the channel the bot works in. (Server Owner and Admin Only)', inline=False)
	embed.add_field(name=prefix + 'suggestions', value='Sends all the suggestions (only Server owner)', inline=False)	
	embed.add_field(name=prefix + 'clear', value='Clears messages at mass (Server owner/Admins/AriatCowboy)', inline=False)
	await ctx.channel.send(embed=embed) 

#displays the Normal help command
@client.command(pass_context=True)
async def help(ctx):
	author = ctx.message.author
	embed = discord.Embed(color=0xb663b6)
	embed.set_author(name='Help')
	embed.add_field(name=prefix + 'music', value='Displays music menu', inline=False)
	embed.add_field(name=prefix + 'usercount', value='Sends a DM of total amount of users', inline=False)
	embed.add_field(name=prefix + 'report', value='Shows how many users are online/offline/idle', inline=False)
	embed.add_field(name=prefix + 'ss', value='Please use artist - title', inline=False)	
	embed.add_field(name=prefix + 'botsuggest', value='Suggest updates or features for bot', inline=False)
	await ctx.channel.send(embed=embed) 

#displays the music bot help command
@client.command(pass_context=True)
async def music(ctx):
	author = ctx.message.author
	embed = discord.Embed(color=0xb663b6)
	embed.set_author(name='Music')
	embed.add_field(name=prefix + 'join', value='Joins server (must add channel name)', inline=False)
	embed.add_field(name=prefix + 'play', value='Plays a YouTube link', inline=False)
	embed.add_field(name=prefix + 'volume', value='Changes the volume', inline=False)
	embed.add_field(name=prefix + 'stop', value='Kicks bot from voice channel', inline=False)
	embed.add_field(name=prefix + 'queue', value='Adds song to queue', inline=False)	
	embed.add_field(name=prefix + 'pause', value='Pauses current song', inline=False)	
	embed.add_field(name=prefix + 'resume', value='Resumes current song', inline=False)
	embed.add_field(name=prefix + 'skip', value='Skips current song', inline=False)
	await ctx.channel.send(embed=embed) 

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