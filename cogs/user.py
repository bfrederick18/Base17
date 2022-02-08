from cogs.utils.embed_tpl import error_tpl
from cogs.utils.time import now
from config import data
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
                await ctx.send(embed=error_tpl(ctx, data[data['config']['chosen_language']]['start_requires_nick_error']))
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
        await ctx.send(embed=error_tpl(ctx, data[data['config']['chosen_language']]['already_registered_error']))


    @commands.command(aliases=['i', 'inv', 'data'])
    async def info(self, ctx):
        global data
        user_id = str(ctx.author.id)
        if user_id not in db['users'].keys():
            await ctx.send(embed=error_tpl(ctx, data[data['config']['chosen_language']]['not_registered_error']))
            return
        data = db['users'][user_id]
        await ctx.send(f'{data["nick"]}\'s Info\nSilver: {data["bal"]}')

def setup(bot):
    bot.add_cog(User(bot))