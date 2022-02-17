import random

import discord

from cogs.utils.embed_tpl import error_tpl, dialogue_tpl
from cogs.utils.time import now
from config import jdata
from discord.ext import commands
from replit import db


class User(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    async def send_dlg(self, ctx):
        user_id = str(ctx.author.id)
        if user_id in db['users'].keys():
            user_dlg_id = db['users'][user_id]['dialogue_id']
            en_chosen_dlg = jdata['en']['dialogue'][user_dlg_id['major']][user_dlg_id['minor']][user_dlg_id['sub']]
        
            if 'description' in en_chosen_dlg.keys() and 'author' in en_chosen_dlg.keys():
                await ctx.send(embed=dialogue_tpl(eval(en_chosen_dlg['author']), eval(en_chosen_dlg['description']), eval(en_chosen_dlg['footer'])))
                print(f'{now()}: [{user_id}] Sent dialogue.')

                jdata_chosen_dlg = jdata['game_data']['dialogue'][user_dlg_id['major']][user_dlg_id['minor']][user_dlg_id['sub']]
                print(f'{now()}: [{user_id}] Defined jdata_chosen_dlg')
                
                if 'input' not in jdata_chosen_dlg.keys():
                    print(f'{now()}: [{user_id}] Entered if scope.')
                    
                    db['users'][user_id]['dialogue_id']['major'] = jdata_chosen_dlg['next']['dialogue']['major']
                    db['users'][user_id]['dialogue_id']['minor'] = jdata_chosen_dlg['next']['dialogue']['minor']
                    db['users'][user_id]['dialogue_id']['sub'] = jdata_chosen_dlg['next']['dialogue']['sub']
                    print(f'{now()}: [{user_id}] Updated major, minor, and sub.')
                    
                    await self.send_dlg(ctx)
                    print(f'{now()}: [{user_id}] Done with send_dlg recursion.')
                else:
                    print(f'{now()}: [{user_id}] Waiting on input.')
            else:
                await ctx.send(embed=error_tpl(ctx, jdata[jdata['config']['chosen_language']]['errors']['dlg_no_desc_or_author']))
        else:
            await ctx.send(embed=error_tpl(ctx, jdata[jdata['config']['chosen_language']]['errors']['not_registered']))

    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{now()}: User cog is online.')


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
                    'major': '0',
                    'minor': '0',
                    'sub': '0'
                },
                'occupation': '',
                'skills': {}
            }
            db['users'][str(ctx.author.id)] = user_data

            await self.send_dlg(ctx)
            return
            
        await ctx.send(embed=error_tpl(ctx, jdata[jdata['config']['chosen_language']]['errors']['already_registered']))

    
    @commands.command(aliases=['in'])
    async def input(self, ctx, input):
        user_id = str(ctx.author.id)
        if user_id in db['users'].keys():
            user_dlg_id = db['users'][user_id]['dialogue_id']
            jdata_chosen_dlg = jdata['game_data']['dialogue'][user_dlg_id['major']][user_dlg_id['minor']][user_dlg_id['sub']]
        return


    @commands.command(aliases=['dlg'])
    async def dialogue(self, ctx):
        await self.send_dlg(ctx)
        return


def setup(bot):
    bot.add_cog(User(bot))