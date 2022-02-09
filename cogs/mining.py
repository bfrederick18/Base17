import random

import discord

from cogs.utils.embed_tpl import error_tpl
from cogs.utils.time import now
from config import jdata
from discord.ext import commands
from replit import db


class Mining(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{now()}: Mining cog is online.')


    @commands.command(aliases=['m'])
    async def mine(self, ctx):
        if 'users' not in db.keys():
            await ctx.send(embed=error_tpl(ctx, jdata[jdata['config']['chosen_language']]['no_users_error']))
            return
        user_id = str(ctx.author.id)
        if user_id not in db['users'].keys():
            await ctx.send(embed=error_tpl(ctx, jdata[jdata['config']['chosen_language']]['not_registered_error']))
            return
        
        inc = 1
        db['users'][user_id]['bal'] += inc
        bal = db['users'][user_id]['bal']
        embed = discord.Embed(
            description=f'Mined a profit of **{inc}** credit.',
            color=discord.Color.dark_gray())
        embed.set_author(name=f'[{ctx.author.name}] Successfully mined.',
                            icon_url=jdata['config']['ore_icons'][random.randint(0, 1)])
        embed.set_footer(text=f'Credit: {bal} | Profit: {inc}')
        await ctx.message.delete()
        await ctx.send(embed=embed, delete_after=60.0)


def setup(bot):
    bot.add_cog(Mining(bot))