import discord          #basic functions
import numpy            #calling the random inhabitants
import datetime         #changing seconds to hours and minutes
import os               #accessing operating system info
import random           #Generating random number
import mysql.connector  #Creating and saving a database 
import sqlite3          #Local databaseS
import traceback        #Traceback for cogs
import sys              #For cogs
from utility import safe_cast_to_int
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

#Setting up the cog
class BuildingCog(commands.Cog, name = 'Building'):

    def __init__(self, bot):
        self.bot = bot

    #### BUILDING ####
    #What can you build?
    @commands.command()
    async def build(self, ctx):
        await ctx.send("You can choose to build a park, a school or a museum. Type .park for a park, .school for a school and .museum for a museum.")

    #Building a park
    @commands.command()
    async def park(self, ctx):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM gathering WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
        result = cursor.fetchone()


        if result is None:
            await ctx.send("Please set up a town first with .towny!")

        else:
            cursor.execute(f"SELECT user_id, flowers, parks FROM gathering WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
            result1 = cursor.fetchone()
            flowers = safe_cast_to_int(result1[1])
            parks = safe_cast_to_int(result1[2])
            value = 5 * parks

            if parks == 0:
                if flowers < value: 
                    await ctx.send("You need %d flowers to build a park. Try again when you have collected enough!")
                else:
                    sql = ("UPDATE gathering SET flowers = ? and parks = ? WHERE guild_id = ? and user_id = ?")
                    val = (flowers - value, parks + 1, str(ctx.message.guild.id), str(ctx.message.author.id))
                    cursor.execute(sql, val)
                    db.commit()
                    await ctx.send("You built a level 1 park!")
            else: 
                if flowers < value:
                    await ctx.send("You need to have %d flowers to upgrade your park. Try again when you have collected enough!" % (value))
                else:
                    sql = ("UPDATE gathering SET flowers = ? and parks = ? WHERE guild_id = ? and user_id = ?")
                    val = (flowers - value, parks + 1, str(ctx.message.guild.id), str(ctx.message.author.id))
                    cursor.execute(sql, val)
                    db.commit()
                    await ctx.send("You have upgraded your park! It is now level %d." % (parks+1))

        cursor.close()
        db.close()

    #Building a school
    @commands.command()
    async def school(self, ctx):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM gathering WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
        result = cursor.fetchone()


        if result is None:
            await ctx.send("Please set up a town first with .towny!")

        else:
            cursor.execute(f"SELECT user_id, wood, stones, schools FROM gathering WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
            result1 = cursor.fetchone()
            wood = safe_cast_to_int(result1[1])
            stones = safe_cast_to_int(result1[2])
            schools = safe_cast_to_int(result1[3])
            value1 = 8 * schools + 20
            value2 = 6 * schools + 20

            if schools == 0:
                if wood < value1:
                    await ctx.send("You need to have %d wood and %d stones to build a school. Try again when you have collected enough!" % (value1, value2))
                elif stones < value2:
                    await ctx.send("You need to have %d wood and %d stones to build a school. Try again when you have collected enough!" % (value1, value2))
                else:
                    sql = ("UPDATE gathering SET wood = ?, stones = ? and schools = ? WHERE guild_id = ? and user_id = ?")
                    val = (wood - value1, stones - value2, schools + 1, str(ctx.message.guild.id), str(ctx.message.author.id))
                    cursor.execute(sql, val)
                    db.commit()
                    await ctx.send("You built a level 1 school!")   
            else: 
                if wood < value1:
                    await ctx.send("You need to have %d wood and %d stones to upgrade your school. Try again when you have collected enough!" % (value1, value2))
                elif stones < value2:
                    await ctx.send("You need to have %d wood and %d stones to upgrade your school. Try again when you have collected enough!" % (value1, value2))
                else:
                    sql = ("UPDATE gathering SET wood = ?, stones = ? and schools = ? WHERE guild_id = ? and user_id = ?")
                    val = (wood - value1, stones - value2, schools + 1, str(ctx.message.guild.id), str(ctx.message.author.id))
                    cursor.execute(sql, val)
                    db.commit()
                    await ctx.send("You built a level %d school!" % (schools + 1))                                  
        cursor.close()
        db.close()

    #Building a museum
    async def museum(self, ctx):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM gathering WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
        result = cursor.fetchone()


        if result is None:
            await ctx.send("Please set up a town first with .towny!")

        else:
            cursor.execute(f"SELECT user_id, wood, stones, flowers, fish, bugs, museums FROM gathering WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{ctx.message.author.id}'")
            result1 = cursor.fetchone()
            wood = safe_cast_to_int(result1[1])
            stones = safe_cast_to_int(result1[2])
            flowers = safe_cast_to_int(result1[3])
            fish = safe_cast_to_int(result1[4])
            bugs = safe_cast_to_int(result1[5])
            museums = safe_cast_to_int(result1[6])
            value_wood = 8 * museums + 20
            value_stones = 6 * museums + 20
            value_flowers = 8 * museums + 15
            value_fish = 2 * museums + 5
            value_bugs = 2 * museums + 5

            if museums == 0:
                if wood < value_wood:
                    await ctx.send("You need to have 20 wood, 20 stones, 15 flowers, 5 bugs, and 5 fish to build a museum. Try again when you have all the resources!")
                elif stones < value_stones:
                    await ctx.send("You need to have 20 wood, 20 stones, 15 flowers, 5 bugs, and 5 fish to build a museum. Try again when you have all the resources!")   
                elif flowers < value_flowers:
                    await ctx.send("You need to have 20 wood, 20 stones, 15 flowers, 5 bugs, and 5 fish to build a museum. Try again when you have all the resources!")   
                elif fish < value_fish:
                    await ctx.send("You need to have 20 wood, 20 stones, 15 flowers, 5 bugs, and 5 fish to build a museum. Try again when you have all the resources!")                                   
                elif bugs < value_bugs:
                    await ctx.send("You need to have 20 wood, 20 stones, 15 flowers, 5 bugs, and 5 fish to build a museum. Try again when you have all the resources!") 
                else:
                    sql = ("UPDATE gathering SET wood = ?, stones = ?, flowers = ?, fish = ?, bugs = ?, museums = ? WHERE guild_id = ? and user_id = ?") 
                    val = (wood - value_wood, stones - value_stones, flowers - value_flowers, fish - value_fish, bugs - value_bugs, museums + 1, str(ctx.message.guild.id), str(ctx.message.author.id))
                    cursor.execute(sql, val)
                    db.commit()
                    await ctx.send("You've built a level 1 museum!")
            else:
                if wood < value_wood:
                    await ctx.send("You need to have %d wood, %d stones, %d flowers, %d bugs, and %d fish to upgrade your museum. Try again when you have all the resources!" % (value_wood, value_stones, value_flowers, value_fish, value_bugs))
                elif stones < value_stones:
                    await ctx.send("You need to have %d wood, %d stones, %d flowers, %d bugs, and %d fish to upgrade your museum. Try again when you have all the resources!" % (value_wood, value_stones, value_flowers, value_fish, value_bugs))   
                elif flowers < value_flowers:
                    await ctx.send("You need to have %d wood, %d stones, %d flowers, %d bugs, and %d fish to upgrade your museum. Try again when you have all the resources!" % (value_wood, value_stones, value_flowers, value_fish, value_bugs))
                elif fish < value_fish:
                    await ctx.send("You need to have %d wood, %d stones, %d flowers, %d bugs, and %d fish to upgrade your museum. Try again when you have all the resources!" % (value_wood, value_stones, value_flowers, value_fish, value_bugs))                                   
                elif bugs < value_bugs:
                    await ctx.send("You need to have %d wood, %d stones, %d flowers, %d bugs, and %d fish to upgrade your museum. Try again when you have all the resources!" % (value_wood, value_stones, value_flowers, value_fish, value_bugs)) 
                else:
                    sql = ("UPDATE gathering SET wood = ?, stones = ?, flowers = ?, fish = ?, bugs = ?, museums = ? WHERE guild_id = ? and user_id = ?") 
                    val = (wood - value_wood, stones - value_stones, flowers - value_flowers, fish - value_fish, bugs - value_bugs, museums + 1, str(ctx.message.guild.id), str(ctx.message.author.id))
                    cursor.execute(sql, val)
                    db.commit()
                    await ctx.send("You've upgraded your museum to level %d!" % (museums + 1))                


def setup(client):
    client.add_cog(BuildingCog(client))
    print('Building is loaded')