#### Setting up the bot ####
# Importing both discord.py and the commands that belong to discord.py
import discord #basic functions
import numpy #calling the random inhabitants
import datetime #changing seconds to hours and minutes
import os #accessing operating system info
import random #Generating random number
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
@commands.cooldown(1,60*60, type=commands.BucketType.user)
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

# Fishing
global fishcounter
fishcounter = 0

@client.command()
@commands.cooldown(1,60*30, type=commands.BucketType.user)
async def fish(ctx):
    global fishcounter
    chance = random.randint(1,100)
    if chance <= 80:
        fishcounter = fishcounter + 1
        await ctx.send("Congrats! You caught a fish. Your total is now %d." % (fishcounter,))
    else:
        await ctx.send("Oh no! You didn't catch a fish. Try again later!")

@fish.error
async def cooldown_fish(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'You cannot fish yet! Please wait {:.0f} seconds.'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error 

# Catching bugs
global bugs
bugcounter = 0

@client.command()
@commands.cooldown(1,60*30, type=commands.BucketType.user)
async def bugs(ctx):
    global bugcounter
    chance = random.randint(1,100)
    if chance <= 60:
        bugcounter = bugcounter + 1
        await ctx.send("Congrats! You caught a bug. Your total is now %d." % (bugcounter,))
    else:
        await ctx.send("Oh no! You didn't catch a bug. Try again later!")

@bugs.error
async def cooldown_bugs(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'You cannot catch a bug yet! Please wait {:.0f} seconds.'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error 

# The stats of your town
@client.command()
async def townystats(ctx):
    await ctx.send("You now have %d inhabitants in your town! You also have %d wood, %d stones and %d flowers, as well as %d fish and %d bugs. You have built: %d parks, %d schools and %d museums." % (counter, woodcounter, miningcounter, flowercounter, fishcounter, bugcounter, parks, schools, museums))


#### BUILDING ####
#What can you build?
@client.command()
async def build(ctx):
    await ctx.send("You can choose to build a park, a school or a museum. Type .park for a park and .school for a school.")

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

#Building a museum
global museums
museums = 0

@client.command()
async def museum(ctx):
    global woodcounter
    global miningcounter
    global flowercounter
    global fishcounter
    global bugcounter
    global museums
    value_wood = 20
    value_stones = 10
    value_flowers = 15
    value_fish = 5
    value_bug = 5
    if woodcounter < value_wood:
        await ctx.send("You need to have 20 wood, 10 stones, 15 flowers, 5 fish and 5 bugs to build a museum. Try again when you have all the resources!")
    elif miningcounter < value_stones:
        await ctx.send("You need to have 20 wood, 10 stones, 15 flowers, 5 fish and 5 bugs to build a museum. Try again when you have all the resources!")
    elif flowercounter < value_flowers:
        await ctx.send("You need to have 20 wood, 10 stones, 15 flowers, 5 fish and 5 bugs to build a museum. Try again when you have all the resources!")
    elif fishcounter < value_fish:
        await ctx.send("You need to have 20 wood, 10 stones, 15 flowers, 5 fish and 5 bugs to build a museum. Try again when you have all the resources!")
    elif bugcounter < value_bug:
        await ctx.send("You need to have 20 wood, 10 stones, 15 flowers, 5 fish and 5 bugs to build a museum. Try again when you have all the resources!")
    else:
        woodcounter = woodcounter - value_wood
        miningcounter = miningcounter - value_stones
        flowercounter = flowercounter - value_flowers
        fishcounter = fishcounter - value_fish
        bugcounter = bugcounter - value_bug
        museums = museums + 1
        await ctx.send("Congratulations! You built a museum! You now have %d museums." % (museums,))


# Adding the token that belongs to the bot
client.run(os.environ['CLIENT_TOKEN']) #Send me a request if you want the token
