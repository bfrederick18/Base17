from cogs.utils.embed import send_success
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
        print(f'{now()}: Clearing messages in channel {ctx.channel.id}.')
        deleted = await ctx.channel.purge(limit=amount)
        await send_success(ctx, f'Deleted {len(deleted)} message{"s" if len(deleted) < 1 or len(deleted) > 1 else ""}.')
        print(f'{now()}: Successfully cleared {len(deleted)} message{"s" if len(deleted) < 1 or len(deleted) > 1 else ""}.')


def setup(bot):
    bot.add_cog(Administrator(bot))