import random

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
    async def start(self, ctx, username=''):
        user_id = str(ctx.author.id)
        if user_id not in db['users'].keys():
            (x, y) = (
                random.randint(jdata['config']['sectors']['width']['min'], jdata['config']['sectors']['width']['max']),
                random.randint(jdata['config']['sectors']['height']['min'], jdata['config']['sectors']['height']['max'])
            )
            
            user_data = {
                'username': ctx.author.name,
                'prefix': '',
                'quarx': 0,
                'coords': {
                    'x': x,
                    'y': y
                },
                'ships': {},
                'colonies': {},
                'dialogue_id': {
                    'major': 0,
                    'minor': 0,
                    'sub': 0
                },
                'occupation': '',
                'skills': {}
            }
            db['users'][str(ctx.author.id)] = user_data
            
            embed = discord.Embed(color=int(jdata['config']['colors']['info'], 16))
            embed.set_author(name=f'[{user_data["username"]}] Done starting.', icon_url=jdata['config']['icons']['success'])
            embed.set_footer(text=f'Quarx: {user_data["quarx"]}\nShips: {len(user_data["ships"].keys())} | Colonies: {len(user_data["colonies"].keys())}')
            await ctx.send(embed=embed)
            return
        await ctx.send(embed=error_tpl(ctx, jdata[jdata['config']['chosen_language']]['errors']['already_registered']))


    @commands.command(aliases=['i', 'inv', 'data'])
    async def info(self, ctx):
        user_id = str(ctx.author.id)
        if user_id not in db['users'].keys():
            await ctx.send(embed=error_tpl(ctx, jdata[jdata['config']['chosen_language']]['errors']['not_registered']))
            return

        user_data = db['users'][user_id]
        embed = discord.Embed(
            description=f'Quarx: {user_data["quarx"]}\nShips: {len(user_data["ships"])}\n Colonies: {len(user_data["colonies"])}',
            color=int(jdata['config']['colors']['info'], 16))
        embed.set_author(name=f'[{user_data["username"]}] Personal Data.', icon_url=jdata['config']['icons']['success'])
        embed.set_footer(text=f'This data will expire in {jdata["config"]["delete_after"]["default"]} seconds.')
        await ctx.message.delete()
        await ctx.send(embed=embed, delete_after=jdata['config']['delete_after']['default'])


    @commands.command(aliases=['in'])
    async def input(self, ctx, input):
        
        return


def setup(bot):
    bot.add_cog(User(bot))