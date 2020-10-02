#### Setting up the bot ####
# Importing both discord.py and the commands that belong to discord.py
import discord #basic functions
import numpy #calling the random inhabitants
import datetime #changing seconds to hours and minutes
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

# Adding a client variable
client = commands.Bot(command_prefix = '.')

# ping pong to check the latency
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! The latency is {round(client.latency * 1000)} ms.')

# Precious loved and worthy affirmation
@client.command()
async def affirmations(ctx):
    await ctx.send('You are precious, loved and worthy!')

# Invite link
@client.command()
async def invite(ctx):
    await ctx.send('https://discord.com/api/oauth2/authorize?client_id=761329713121198091&permissions=8&scope=bot')

#### TOWNY ####
#### Resources ####
# Moving in new inhabitants
# CHANGE: time limit to hours
global counter
counter = 0

@client.command()
@commands.cooldown(1, 60*60*24, type=commands.BucketType.user)
async def towny(ctx):
    global counter
    inhabitants = numpy.random.normal(loc=50, scale=20)
    counter += inhabitants
    await ctx.send("%d new people moved in!" % (inhabitants,))

#If the user already had people move in, display an error message
@towny.error
async def cooldown_towny(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'New people only move in once a day. Try again in {:.0f} seconds.'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error 


# Chopping wood
global woodcounter
woodcounter = 0

@client.command()
@commands.cooldown(1, 60*60, type=commands.BucketType.user)
async def wood(ctx):
    global woodcounter 
    wood = numpy.random.normal(loc = 8, scale = 2)
    woodcounter += wood
    await ctx.send("You chopped %d pieces of wood." % (wood,))

@wood.error
async def cooldown_wood(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'You cannot chop wood yet. Try again in {:.0f} seconds.'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error 

# Mining
global miningcounter
miningcounter = 0

@client.command()
@commands.cooldown(1,60*60, type=commands.BucketType.user)
async def mining(ctx):
    global miningcounter 
    stones = numpy.random.normal(loc = 5, scale = 5)
    miningcounter += stones
    await ctx.send("You mined %d stones." % (stones,))

@mining.error
async def cooldown_mining(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'You cannot mine yet. Try again in {:.0f} seconds.'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

# Picking flowers
global flowercounter
flowercounter = 0

@client.command()
@commands.cooldown(1,6*60, type=commands.BucketType.user)
async def flowers(ctx):
    global flowercounter
    flowers = numpy.random.normal(loc = 4, scale = 4)
    flowercounter += flowers
    await ctx.send("You picked %d flowers." % (flowers,))

@flowers.error
async def cooldown_flowers(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'You cannot pick flowers yet. Try again in {:.0f} seconds.'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

# The stats of your town
@client.command()
async def townystats(ctx):
    await ctx.send("You now have %d inhabitants in your town! You also have %d wood, %d stones and %d flowers. You have built: %d parks and %d schools." % (counter, woodcounter, miningcounter, flowercounter, parks, schools))


#### BUILDING ####
#What can you build?
@client.command()
async def build(ctx):
    await ctx.send("You can choose to build a park or a school. Type .park for a park and .school for a school.")

#Building a park
global parks
parks = 0

@client.command()
async def park(ctx):
    global flowercounter
    global parks
    value = 5
    if flowercounter < value:
        await ctx.send("You need 5 flowers to build a park. Try again when you have collected enough!")
    else:
        flowercounter = flowercounter - value
        parks = parks + 1
        await ctx.send("You built a park! You now have %d parks" % (parks,))

#Building a school
global schools
schools = 0

@client.command()
async def school(ctx):
    global woodcounter
    global miningcounter
    global schools
    value = 10
    if woodcounter < value:
        await ctx.send("You need to have 10 wood and 10 stones to build a school. Try again when you have collected enough!")
    elif miningcounter < value:
        await ctx.send("You need to have 10 wood and 10 stones to build a school. Try again when you have collected enough!")
    else:
        woodcounter = woodcounter - value
        miningcounter = miningcounter - value
        schools = schools + 1
        await ctx.send("You built a school! You now have %d schools" % (schools,))

# Adding the token that belongs to the bot
client.run('X') #Send me a request if you want the token
