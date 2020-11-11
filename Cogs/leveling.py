# Importing both discord.py and the commands that belong to discord.py
import discord      #basic functions
import numpy        #calling the random inhabitants
import datetime     #changing seconds to hours and minutes
import os           #accessing operating system info
import random       #Generating random number
import sqlite3      #Creating and saving a database 
import math         #For the leveling system
from utility import safe_cast_to_int
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

class LevelCog(commands.Cog, name = 'Leveling'):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM levels WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO levels(guild_id, user_id, exp, level) VALUES(?,?,?,?)")
            val = (message.guild.id, message.author.id, 2, 0)
            cursor.execute(sql, val)
            db.commit()
        else:
            cursor.execute(f"SELECT user_id, exp, level FROM levels WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
            result1 = cursor.fetchone()
            exp = safe_cast_to_int(result1[1])
            sql = ("UPDATE levels SET exp = ? WHERE guild_id = ? and user_id = ?")
            val = (exp + 2, str(message.guild.id), str(message.author.id))
            cursor.execute(sql, val)
            db.commit()

            cursor.execute(f"SELECT user_id, exp, level FROM levels WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
            result2 = cursor.fetchone()

            xp_start = safe_cast_to_int(result2[1])
            lvl_start = safe_cast_to_int(result2[2])
            xp_end = math.floor(5 * (lvl_start ^ 2) + 50 * lvl_start + 100)
            if xp_end < xp_start:
                await message.channel.send(f'{message.author.mention} has leveled up to level {lvl_start + 1}')
                sql = ("UPDATE levels SET level = ? WHERE guild_id = ? and user_id = ?")
                val = (int(lvl_start + 1), str(message.guild.id), str(message.author.id))
                cursor.execute(sql, val)
                db.commit()
                sql = ("UPDATE levels SET exp = ? WHERE guild_id = ? and user_id = ?")
                val = (0, str(message.guild.id), str(message.author.id))
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

    @commands.command()
    async def rank(self, ctx, user:discord.User=None):
        if user is not None:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT user_id, exp, level FROM levels WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{user.id}'")
            result = cursor.fetchone()
            if result is None:
                await ctx.send('This user is not yet ranked')
            else: 
                await ctx.send(f'{user.name} is currently level {str(result[2])} and has {str(result[1])} xp!')
            cursor.close()
            db.close()

        elif user is None:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT user_id, exp, level FROM levels WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
            result = cursor.fetchone()
            if result is None:
                await ctx.send('This user is not yet ranked')
            else: 
                await ctx.send(f'{ctx.message.author.name} is currently level {str(result[2])} and has {str(result[1])} xp!')
            cursor.close()
            db.close()

def setup(client):
    client.add_cog(LevelCog(client))
    print('Leveling is loaded')