# Importing both discord.py and the commands that belong to discord.py
import discord      #basic functions
import numpy        #calling the random inhabitants
import datetime     #changing seconds to hours and minutes
import os           #accessing operating system info
import random       #Generating random number
import sqlite3      #Creating and saving a database 
import math         #For the leveling system
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

class TownNameCog(commands.Cog, name = 'TownName'):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command = True)
    async def townname(self, ctx):
        await ctx.send('Please set your town name with townname newname <your new town name>')

    @townname.command()
    async def newname(self, ctx, *, text):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECt townname FROM townnames WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO townnames(guild_id, user_id, townname) VALUES (?,?,?)")
            val = (str(ctx.guild.id), str(ctx.author.id), text)
            await ctx.send(f"Your town name has been set to {text}!")
        elif result is not None:
            sql = ("UPDATE townnames SET townname = ? WHERE guild_id = ? and user_id = ?")
            val = (text, str(ctx.guild.id), str(ctx.author.id))
            await ctx.send(f"Your town name has been updated to {text}!") 
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

def setup(client):
    client.add_cog(TownNameCog(client))
    print('TownNames is loaded')