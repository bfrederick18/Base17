import discord

from cogs.utils.time import now
from discord.ext import commands


class Master(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{now()}: Master cog is online.')


    @commands.command()
    async def load(self, ctx, extension):
        self.bot.load_extension(f'cogs.{extension}')


    @commands.command()
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')

def setup(bot):
    bot.add_cog(Master(bot))