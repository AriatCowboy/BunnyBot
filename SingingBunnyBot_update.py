import socket
import os
from twitch_db import update_twitch, authorized_users
from Song_suggestions import suggest, conn
from Song_List import connect, insert_song
from twitchio.ext import commands

TMI_TOKEN = "oauth:1qjj2944mdkz3cplyenq50ksa6znkn"
CLIENT_ID = "Pivk5b4z7x9x2zxvkaqpye00ig8tm76"
BOT_NICK = "singingbunnybot"
BOT_PREFIX = "!"
CHANNEL = "SingingBunnyBot"

bot = commands.Bot(
		# set up the bot
	irc_token="oauth:1qjj2944mdkz3cplyenq50ksa6znkn",
	client_id="Pivk5b4z7x9x2zxvkaqpye00ig8tm76",
	nick="singingbunnybot",
	prefix="!",
	initial_channels=["SingingBunnyBot"])

@bot.event
async def event_ready():
	print(f'Ready | {bot.nick}')

@bot.event
async def event_message(message):
    print(message.content)
    author = message.author
    update_twitch(author)
    await bot.handle_commands(message)

@bot.command()
async def calp(ctx):
	await ctx.send("divneoCalp divneoCalp divneoCalp divneoCalp divneoCalp divneoCalp")

@bot.command()
async def love(ctx):
	await ctx.send("divneoLav 💜 🖤 divneoLav 💜 🖤 divneoLav 💜 🖤 divneoLav 💜 🖤 ")

@bot.command()
async def squid(ctx):
	await ctx.send("Squid1 Squid2 Squid3 Squid2 Squid4")

@bot.command()
async def sadgirl(ctx):
	await ctx.send("divneoSADGIRL divneoSADGIRL divneoSADGIRL divneoSADGIRL Sad Girl Vibes divneoSADGIRL divneoSADGIRL divneoSADGIRL divneoSADGIRL")

@bot.command()
async def mac(ctx):
	await ctx.send("etcOops etcOops etcOops etcOops etcOops etcOops etcOops etcOops etcOops etcOops etcOops")

@bot.command()
async def raid(ctx):
	await ctx.send("divneoCARROTS twitchRaid divneoCARROTS twitchRaid Divneofficial CARROT GANG twitchRaid divneoCARROTS twitchRaid divneoCARROTS")

@bot.command()
async def raid(ctx):
	await ctx.send("@{} !calp !sadgirl !squid !love !calp !adds !mac !raid !ss <Author - Song>")




@bot.command()
async def ss(ctx):
	message = ctx.message
	content = message.content.split(" ", 1)
	try:
		new_message = content[1].split("-", 1)
	except:
		await ctx.send("@{} please use Author - song format".format(ctx.message.author.display_name))
	else:
		await ctx.send("@{} please use Author - song format".format(ctx.message.author.display_name))
		return
	author = new_message[0]
	try:
		song = new_message[1]
	except:
		await ctx.send("@{} please use Author - song format".format(ctx.message.author.display_name))
	else:
		await ctx.send("@{} please use Author - song format".format(ctx.message.author.display_name))
		return
	print(author + " - " + song)
	chat = "Twitch"
	suggest(ctx.message.author, author, song, chat)
	await ctx.send(author + " = " + song + " was added to the suggestions list. @{}".format(ctx.message.author.display_name))

@bot.command()
async def suggestions(ctx):
	twitch_suggestions()

@bot.command()
async def logoff(ctx):
	authorized_user = authorized_users(ctx)
	if authorized_user:
		connect.close()
		conn.close()
		bot.close()
	else:
		await ctx.send("@{} You are not authorized to use this command!".format(ctx.message.author.display_name))

bot.run()