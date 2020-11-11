#### Setting up the bot ####
# Importing both discord.py and the commands that belong to discord.py
import discord          #basic functions
import numpy            #calling the random inhabitants
import datetime         #changing seconds to hours and minutes
import os               #accessing operating system info
import random           #Generating random number
import sqlite3          #Local databaseS
import traceback        #Traceback for cogs
import sys              #For cogs
from utility import safe_cast_to_int
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

# Adding a client variable
client = commands.Bot(command_prefix = '.')

# Setting up cogs
initial_extensions = ['Cogs.cog', 'Cogs.leveling', 'Cogs.townnames', 'Cogs.welcomemessage', 'Cogs.towngathering']

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            print(f'Sorry, I could not load extension {extension}', file = sys.stderr)
            traceback.print_exc()

# Bot event: print when it goes live
# Additionally: connecting to the database
@client.event
async def on_ready():
    print("I am live!")

# ping pong to check the latency
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! The latency is {round(client.latency * 1000)} ms.')

# Precious loved and worthy affirmation
@client.command()
async def affirmations(ctx):
    messages = ["You are precious, loved and worthy!", "You are beautiful, inside and out!", "You have a positive impact on this world!", 
    "Just keep moving forward, you got this!", "You are a wonderful person who deserves everything this world has to offer!",
    "You are honestly amazing!", "You are one of the nicest people I've ever seen!", "Your heart is so big and beautiful!", 
    "You mean a lot to me!", "You are strong and brave!", "You are so much stronger and braver than you think, lovely!",
    "You are spectacular!", "You are breathtaking!", "You are amazing!", "You are the bee's knees!", "You are legendary!",
    "You are sublime!", "I believe in you!", "I am so proud of you!", "You deserve love, compassion and empathy!", "You are enough!",
    "You matter!", "You are excellent!", "You are enough!", "You are worthy!", "You're doing your best!", "You deserve to be happy!",
    "You are astonishing!", "You are awesome!", "You are stellar!"]
    await ctx.send(random.choice(messages))

# Invite link
@client.command()
async def invite(ctx):
    await ctx.send('https://discord.com/api/oauth2/authorize?client_id=761329713121198091&permissions=8&scope=bot')

#### TINYTOWN ####
#Stats of the town
@client.command()
async def townystats(ctx):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id, inhabitants, wood, stones, flowers, fish, bugs FROM gathering WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
    result = cursor.fetchone()

    inhabitants = safe_cast_to_int(result[1])
    wood = safe_cast_to_int(result[2])
    stones = safe_cast_to_int(result[3])
    flowers = safe_cast_to_int(result[4])
    fish = safe_cast_to_int(result[5])
    bugs = safe_cast_to_int(result[6])

    await ctx.send('You now have %d inhabitants in your town! You also have %d wood, %d stones and %d flowers, as well as %d fish and %d bugs.' %(inhabitants, wood, stones, flowers, fish, bugs))

    cursor.close()
    db.close()

# Adding the token that belongs to the bot
client.run(os.environ['CLIENT_TOKEN']) #Send me a request if you want the token
