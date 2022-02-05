import cogs.utils.constants as c

from cogs.utils.embed_tpl import error_tpl
from cogs.utils.time import now
from discord.ext import commands
from replit import db


class User(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{now()}: User cog is online.')


    @commands.command(aliases=['join', 'register'])
    async def start(self, ctx, nick=''):
        user_id = str(ctx.author.id)
        if user_id not in db['users'].keys():
            if nick == '':
                await ctx.send(embed=error_tpl(ctx, c.start_requires_nick_error), delete_after=60.0)
                return

            user_data = {
                'nick': nick,
                'bal': 0,
                'ships': {},
                'colonies': {},
            }
            db['users'][int(ctx.author.id)] = user_data
            await ctx.send('Done starting.')
            return
        await ctx.send(embed=error_tpl(ctx, c.already_registered_error), delete_after=60.0)


    @commands.command(aliases=['i'])
    async def info(self, ctx):
        user_id = str(ctx.author.id)
        if user_id not in db['users'].keys():
            await ctx.send(embed=error_tpl(ctx, c.not_registered_error), delete_after=60.0)
            return
        data = db['users'][user_id]
        await ctx.send(f'{data["nick"]}\'s Info\nSilver: {data["bal"]}')

def setup(bot):
    bot.add_cog(User(bot))