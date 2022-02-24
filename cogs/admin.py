from cogs.utils.time import now
from discord.ext import commands


class Administrator(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{now()}: Admin cog is online.')


    @commands.command(aliases=['p'])
    async def ping(self, ctx):
        await ctx.message.delete()
        await ctx.send(f'Pong: {round(self.bot.latency * 1000)}ms.')


    @commands.command()
    async def clear(self, ctx, amount: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        await ctx.send('test', delete_after=10.0)


def setup(bot):
    bot.add_cog(Administrator(bot))