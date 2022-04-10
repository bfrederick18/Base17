import random

import discord

from cogs.utils.embed import send_error_embed
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
            await send_error_embed(ctx, 'no_users')
            return

        user_id = str(ctx.author.id)
        if user_id not in db['users'].keys():
            await send_error_embed(ctx, 'not_registered')
            return
        
        inc = 1
        db['users'][user_id]['quarx'] += inc

        user_data = db['users'][user_id]
        ore_icons = jdata['config']['icons']['ores']

        embed = discord.Embed(description=f'Mined a profit of **{inc}** quarx.', color=int(jdata['config']['colors']['embed']['mining'], 16))
        embed.set_author(
            name=f'[{user_data["username"]}] Successfully mined.',
            icon_url=(ore_icons[random.randint(0, len(ore_icons) - 1)] if len(ore_icons) > 0 else discord.Embed.Empty))
        embed.set_footer(text=f'Quarx: {user_data["quarx"]} | Profit: {inc}\nThis data will expire in {jdata["config"]["delete_after"]["default"]} seconds.')

        await ctx.message.delete()
        await ctx.send(embed=embed, delete_after=jdata['config']['delete_after']['default'])


def setup(bot):
    bot.add_cog(Mining(bot))