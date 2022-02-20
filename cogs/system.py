from cogs.utils.time import now
from discord.ext import commands


class System(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{now()}: System cog is online.')


    @commands.command()
    async def jump(self, ctx):
        await ctx.message.delete()
        await ctx.send(f'Pong: {round(self.bot.latency * 1000)}ms.')


def setup(bot):
    bot.add_cog(System(bot))