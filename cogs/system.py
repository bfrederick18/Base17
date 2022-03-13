from cogs.utils.embed import send_error_embed
from cogs.utils.time import now
from discord.ext import commands
from replit import db


class System(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{now()}: System cog is online.')


    @commands.command()
    async def jump(self, ctx):
        if 'users' not in db.keys():
            await send_error_embed(ctx, 'no_users')
            return
        
        await ctx.message.delete()
        await ctx.send(f'Pong: {round(self.bot.latency * 1000)}ms.')


def setup(bot):
    bot.add_cog(System(bot))