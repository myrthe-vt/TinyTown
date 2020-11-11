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

#Setting up the cog
class GatheringCog(commands.Cog, name = 'Gathering'):

    def __init__(self, bot):
        self.bot = bot

    #### TINYTOWN ####
    #### Resources ####
    # Moving in new inhabitants
    @commands.command()
    @commands.cooldown(1, 60*60*24, type=commands.BucketType.user)
    async def towny(self, ctx):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM gathering WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
        result = cursor.fetchone()

        inhabitants = numpy.random.normal(loc=50, scale=20)

        if result is None:
            sql = ("INSERT INTO gathering(guild_id, user_id, inhabitants) VALUES(?,?,?)")
            val = (ctx.message.guild.id, ctx.message.author.id, inhabitants)
            cursor.execute(sql, val)
            db.commit()
            await ctx.send("%d new people moved in!" % (inhabitants,))

        else:
            cursor.execute(f"SELECT user_id, inhabitants FROM gathering WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
            result1 = cursor.fetchone()
            people = safe_cast_to_int(result1[1])

            sql = ("UPDATE gathering SET inhabitants = ? WHERE guild_id = ? and user_id = ?")
            val = (people + inhabitants, str(ctx.message.guild.id), str(ctx.message.author.id))
            db.commit()
            await ctx.send("%d new people moved in!" % (inhabitants,))
        
        cursor.close()
        db.close()

    #If the user already had people move in, display an error message
    @towny.error
    async def cooldown_towny(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            msg = 'New people only move in once a day. Try again in {:.0f} hours, {:.0f} minutes and {:.0f} seconds.'.format(h, m, s)
            await ctx.send(msg)
        else:
            raise error 

    # Chopping wood
    @commands.command()
    @commands.cooldown(1, 60*60, type=commands.BucketType.user)
    async def wood(self, ctx):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM gathering WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
        result = cursor.fetchone()

        wood = numpy.random.normal(loc = 8, scale = 2)

        if result is None:
            sql = ("INSERT INTO gathering(guild_id, user_id, wood) VALUES(?,?,?)")
            val = (ctx.message.guild.id, ctx.message.author.id, wood)
            cursor.execute(sql, val)
            db.commit()
            await ctx.send("You chopped %d pieces of wood." % (wood,))

        else:
            cursor.execute(f"SELECT user_id, wood FROM gathering WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
            result1 = cursor.fetchone()
            woodcurrent = safe_cast_to_int(result1[1])

            sql = ("UPDATE gathering SET wood = ? WHERE guild_id = ? and user_id = ?")
            val = (woodcurrent + wood, str(ctx.message.guild.id), str(ctx.message.author.id))
            db.commit()
            await ctx.send("You chopped %d pieces of wood." % (wood,))
        
        cursor.close()
        db.close()

    @wood.error
    async def cooldown_wood(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            msg = 'You cannot chop wood yet. Try again in {:.0f} hours, {:.0f} minutes and {:.0f} seconds.'.format(h, m, s)        
            await ctx.send(msg)
        else:
            raise error 

    # Mining for stones
    @commands.command()
    @commands.cooldown(1, 60*60, type=commands.BucketType.user)
    async def stones(self, ctx):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM gathering WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
        result = cursor.fetchone()

        stones = numpy.random.normal(loc = 5, scale = 5)

        if result is None:
            sql = ("INSERT INTO gathering(guild_id, user_id, stones) VALUES(?,?,?)")
            val = (ctx.message.guild.id, ctx.message.author.id, stones)
            cursor.execute(sql, val)
            db.commit()
            await ctx.send("You mined %d stones." % (stones,))

        else:
            cursor.execute(f"SELECT user_id, stones FROM gathering WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
            result1 = cursor.fetchone()
            stonescurrent = safe_cast_to_int(result1[1])

            sql = ("UPDATE gathering SET stones = ? WHERE guild_id = ? and user_id = ?")
            val = (stonescurrent + stones, str(ctx.message.guild.id), str(ctx.message.author.id))
            db.commit()
            await ctx.send("You mined %d stones." % (stones,))
        
        cursor.close()
        db.close()

    @stones.error
    async def cooldown_mining(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            msg = 'You cannot mine yet. Try again in {:.0f} hours, {:.0f} minutes and {:.0f} seconds.'.format(h, m, s)        
            await ctx.send(msg)
        else:
            raise error


    # Picking flowers
    @commands.command()
    @commands.cooldown(1, 60*60, type=commands.BucketType.user)
    async def flowers(self, ctx):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM gathering WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
        result = cursor.fetchone()

        flowers = random.randint(1,4)

        if result is None:
            sql = ("INSERT INTO gathering(guild_id, user_id, flowers) VALUES(?,?,?)")
            val = (ctx.message.guild.id, ctx.message.author.id, flowers)
            cursor.execute(sql, val)
            db.commit()
            await ctx.send("You picked %d flowers." % (flowers,))

        else:
            cursor.execute(f"SELECT user_id, flowers FROM gathering WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
            result1 = cursor.fetchone()
            flowerscurrent = safe_cast_to_int(result1[1])

            sql = ("UPDATE gathering SET wood = ? WHERE guild_id = ? and user_id = ?")
            val = (flowerscurrent + flowers, str(ctx.message.guild.id), str(ctx.message.author.id))
            db.commit()
            await ctx.send("You picked %d flowers." % (flowers,))
        
        cursor.close()
        db.close()

    @flowers.error
    async def cooldown_flowers(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            msg = 'You cannot pick flowers yet. Try again in {:.0f} hours, {:.0f} minutes and {:.0f} seconds.'.format(h, m, s)        
            await ctx.send(msg)
        else:
            raise error

    # Fishing
    @commands.command()
    @commands.cooldown(1, 60*30, type=commands.BucketType.user)
    async def fish(self, ctx):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM gathering WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
        result = cursor.fetchone()

        fish = random.randint(1,3)

        if result is None:
            sql = ("INSERT INTO gathering(guild_id, user_id, fish) VALUES(?,?,?)")
            val = (ctx.message.guild.id, ctx.message.author.id, fish)
            cursor.execute(sql, val)
            db.commit()
            await ctx.send("You caught %d fish." % (fish,))

        else:
            cursor.execute(f"SELECT user_id, fish FROM gathering WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
            result1 = cursor.fetchone()
            fishcurrent = safe_cast_to_int(result1[1])

            sql = ("UPDATE gathering SET fish = ? WHERE guild_id = ? and user_id = ?")
            val = (fishcurrent + fish, str(ctx.message.guild.id), str(ctx.message.author.id))
            db.commit()
            await ctx.send("You caught %d fish." % (fish,))
        
        cursor.close()
        db.close()

    @fish.error
    async def cooldown_fish(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            msg = 'You cannot fish yet. Try again in {:.0f} hours, {:.0f} minutes and {:.0f} seconds.'.format(h, m, s)        
            await ctx.send(msg)
        else:
            raise error 

    # Bugs
    @commands.command()
    @commands.cooldown(1, 60*30, type=commands.BucketType.user)
    async def bugs(self, ctx):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM gathering WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
        result = cursor.fetchone()

        bugs = random.randint(1,2)

        if result is None:
            sql = ("INSERT INTO gathering(guild_id, user_id, bugs) VALUES(?,?,?)")
            val = (ctx.message.guild.id, ctx.message.author.id, bugs)
            cursor.execute(sql, val)
            db.commit()
            await ctx.send("You caught %d bugs." % (bugs,))

        else:
            cursor.execute(f"SELECT user_id, bugs FROM gathering WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
            result1 = cursor.fetchone()
            bugscurrent = safe_cast_to_int(result1[1])

            sql = ("UPDATE gathering SET bugs = ? WHERE guild_id = ? and user_id = ?")
            val = (bugscurrent + bugs, str(ctx.message.guild.id), str(ctx.message.author.id))
            db.commit()
            await ctx.send("You caught %d bugs." % (bugs,))
        
        cursor.close()
        db.close()

    @bugs.error
    async def cooldown_bugs(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            msg = 'You cannot catch a bug yet! Try again in {:.0f} hours, {:.0f} minutes and {:.0f} seconds.'.format(h, m, s)
            await ctx.send(msg)
        else:
            raise error 

def setup(client):
    client.add_cog(GatheringCog(client))
    print('Gathering is loaded')