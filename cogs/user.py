import discord

from cogs.utils.embed_tpl import error_tpl
from cogs.utils.time import now
from config import jdata
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
                await ctx.send(embed=error_tpl(ctx, jdata[jdata['config']['chosen_language']]['start_requires_nick_error']))
                return

            user_data = {
                'nick': nick,
                'bal': 0,
                'ships': {},
                'colonies': {},
            }
            db['users'][int(ctx.author.id)] = user_data
            embed = discord.Embed(color=discord.Color.dark_gray())
            embed.set_author(name=f'[{user_data["nick"]}] Done starting.')
            embed.set_footer(text=f'Credit: {user_data["bal"]}\nShips: {len(user_data["ships"].keys())} | Colonies: {len(user_data["colonies"].keys())}')
            await ctx.message.delete()
            await ctx.send(embed=embed)
            return
        await ctx.send(embed=error_tpl(ctx, jdata[jdata['config']['chosen_language']]['already_registered_error']))


    @commands.command(aliases=['i', 'inv', 'data'])
    async def info(self, ctx):
        user_id = str(ctx.author.id)
        if user_id not in db['users'].keys():
            await ctx.send(embed=error_tpl(ctx, jdata[jdata['config']['chosen_language']]['not_registered_error']))
            return
        db_data = db['users'][user_id]
        await ctx.send(f'{db_data["nick"]}\'s Info\nCredit: {db_data["bal"]}')

def setup(bot):
    bot.add_cog(User(bot))