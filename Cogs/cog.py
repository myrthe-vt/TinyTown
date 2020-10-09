import discord
from discord.ext import commands
import asyncio

class Example(commands.Cog):
    """Commands involving examples."""

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel= self.bot.get_channel()
        await channel.set(f'Welcome to the server {member.mention}!')

    @commands.command()
    async def pong(self, ctx):
        await ctx.send('ping!')

def setup(client):
    client.add_cog(Example(client))
    print('Cog.py is loaded')