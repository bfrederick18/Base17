from cogs.utils.time import now
from config import jdata, reload_json
from discord.ext import commands
from replit import db


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


    @commands.command()
    @commands.is_owner()
    async def db(self, ctx, arg1, arg2, arg3, arg4='', arg5=''):
        if arg1 in db.keys():
            if arg2 == 'all':
                await ctx.send(f'```{db[arg1]}```', delete_after=jdata['config']['debug_seconds'] if arg3 != 'perm' else 2000000)
            if arg2 == 'keys':
                await ctx.send(f'```{list(db[arg1].keys())}```', delete_after=jdata['config']['debug_seconds'] if arg3 != 'perm' else 2000000)
            if arg2 == 'val':
                await ctx.send(db[arg1][arg3], delete_after=jdata['config']['debug_seconds'] if arg4 != 'perm' else 2000000)
            elif arg2 == 'set':
                db[arg1][arg3] = arg4
            if arg2 == 'del':
                del db[arg1][arg3]
    

    '''elif arg1 == 'db':  # DATABASE
    if arg2 == 'keys':
      await ctx.send(db.keys())
    elif arg2 == 'val' or arg2 == 'value':
      await ctx.send(db[arg3])
    elif arg2 == 'set':
      db[arg3] = arg4
    elif arg2 == 'del':
      del db[arg3]'''


def setup(bot):
    bot.add_cog(Master(bot))