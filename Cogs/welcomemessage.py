import discord          #basic functions
import numpy            #calling the random inhabitants
import datetime         #changing seconds to hours and minutes
import os               #accessing operating system info
import random           #Generating random number
import mysql.connector  #Creating and saving a database 
import sqlite3          #Local databaseS
import traceback        #Traceback for cogs
import sys              #For cogs
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

class WelcomeCog(commands.Cog, name = 'Welcome'):

    def __init__(self, bot):
        self.bot = bot

    # Setting up custom welcome commands per different server
    @commands.group(invoke_without_command = True)
    async def welcome(self, ctx):
        await ctx.send('Available setup commands: \nwelcome channel <#channel>\nwelcome text <message>')

    # Where the custom welcome message should go
    @welcome.command()
    async def channel(self, ctx, channel:discord.TextChannel):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main(guild_id, channel_id) VALUES (?,?)")
                val = (ctx.guild.id, channel.id)
                await ctx.send(f"Channel has been set to {channel.mention}")
            elif result is not None:
                sql = ("UPDATE main SET channel_id = ? WHERE guild_id = ?")
                val = (channel.id, ctx.guild.id)
                await ctx.send(f"Channel has been updated to {channel.mention}")
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

    # What the custom message should be
    @welcome.command()
    async def text(self, ctx, *, text):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT message FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main(guild_id, message) VALUES (?,?)")
                val = (ctx.guild.id, text)
                await ctx.send(f"The message has been set to {text}.")
            elif result is not None:
                sql = ("UPDATE main SET message = ? WHERE guild_id = ?")
                val = (text, ctx.guild.id)
                await ctx.send(f"The message has been updated to {text}.")
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

def setup(client):
    client.add_cog(WelcomeCog(client))
    print('Welcome is loaded')