from cogs.utils.time import now
from config import reload_json
from discord.ext import commands


class Master(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{now()}: Master cog is online.')


    @commands.command()
    @commands.is_owner()
    async def reloadjson(self, ctx, extension):
        reload_json(extension)

def setup(bot):
    bot.add_cog(Master(bot))