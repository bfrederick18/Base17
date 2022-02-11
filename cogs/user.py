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
        user_id = ctx.author.id
        if user_id not in db['users'].keys():
            user_data = {
                'username': ctx.author.name,
                'prefix': "",
                'quarx': 0,
                'coords': {
                    'x': 0,
                    'y': 0
                },
                'ships': {},
                'colonies': {},
                'dialogue_id': {
                    'major': -1,
                    'minor': 0,
                    'sub': 0
                }
            }
            db['users'][ctx.author.id] = user_data
            
            embed = discord.Embed(color=discord.Color.dark_gray())
            embed.set_author(name=f'[{user_data["username"]}] Done starting.')
            embed.set_footer(text=f'Quarx: {user_data["quarx"]}\nShips: {len(user_data["ships"].keys())} | Colonies: {len(user_data["colonies"].keys())}')
            await ctx.send(embed=embed)
            return
        await ctx.send(embed=error_tpl(ctx, jdata[jdata['config']['chosen_language']]['errors']['already_registered']))


    @commands.command(aliases=['i', 'inv', 'data'])
    async def info(self, ctx):
        user_id = ctx.author.id
        if user_id not in db['users'].keys():
            await ctx.send(embed=error_tpl(ctx, jdata[jdata['config']['chosen_language']]['errors']['not_registered']))
            return

        user_data = db['users'][user_id]
        embed = discord.Embed(
            description=f'Quarx: {user_data["quarx"]}\nShips: {len(user_data["ships"])}\n Colonies: {len(user_data["colonies"])}',
            color=discord.Color.dark_gray())
        embed.set_author(name=f'[{user_data["username"]}] Personal Data.',
                            icon_url=jdata['config']['success_icon'])
        embed.set_footer(text=f'This data will expire in {jdata["config"]["expire_seconds"]} seconds.')
        await ctx.message.delete()
        await ctx.send(embed=embed, delete_after=jdata['config']['expire_seconds'])


    @commands.command(aliases=['in'])
    async def input(self, ctx, input):
        
        return


def setup(bot):
    bot.add_cog(User(bot))