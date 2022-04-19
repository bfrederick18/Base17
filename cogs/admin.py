from cogs.utils.embed import send_success_embed
from cogs.utils.trm import trmprint
from discord.ext import commands


class Administrator(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        trmprint('Admin cog is online.')


    @commands.command(aliases=['p'])
    async def ping(self, ctx):
        await ctx.message.delete()
        await ctx.send(f'Online: {round(self.bot.latency * 1000)}ms.')
        trmprint(f'Online: {round(self.bot.latency * 1000)}ms.')


    @commands.command()
    async def clear(self, ctx, amount: int):
        await ctx.message.delete()
        trmprint(f'Clearing messages in channel {ctx.channel.id} (max {amount})...', end=' ', flush=True)
        deleted = await ctx.channel.purge(limit=amount)
        await send_success_embed(ctx, f'Deleted {len(deleted)} message{"s" if len(deleted) < 1 or len(deleted) > 1 else ""}.')
        trmprint(f'Success: Cleared {len(deleted)} message{"s" if len(deleted) < 1 or len(deleted) > 1 else ""}.', type='success', time=False)

def setup(bot):
    bot.add_cog(Administrator(bot))