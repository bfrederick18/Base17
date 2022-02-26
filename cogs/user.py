import random
import re

import discord

from cogs.utils.embed import send_error, send_dlg_error, send_dialogue_embed
from cogs.utils.time import now
from config import jdata
from discord.ext import commands
from replit import db


class User(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    def update_dlg_id(self, user_id, chosen_dlg):
        old_dlg = db['users'][user_id]['dialogue_id']
        db['users'][user_id]['dialogue_id']['major'] = chosen_dlg['next']['dialogue']['major']
        db['users'][user_id]['dialogue_id']['minor'] = chosen_dlg['next']['dialogue']['minor']
        db['users'][user_id]['dialogue_id']['sub'] = chosen_dlg['next']['dialogue']['sub']
        print(f'{now()}: [{user_id}] Updated dialogue_id from \
({old_dlg["major"]}, {old_dlg["minor"]}, {old_dlg["sub"]}) to \
({db["users"][user_id]["dialogue_id"]["major"]}, \
{db["users"][user_id]["dialogue_id"]["minor"]}, \
{db["users"][user_id]["dialogue_id"]["sub"]}).')


    async def send_dlg(self, ctx):
        print(f'{now()}: Entered send_dlg.')
        
        user_id = str(ctx.author.id)
        if user_id in db['users'].keys():
            user_dlg_id = db['users'][user_id]['dialogue_id']
            lang_chosen_dlg = jdata[jdata['config']['chosen_language']]['dialogue'][user_dlg_id['major']][user_dlg_id['minor']][user_dlg_id['sub']]
        
            if 'description' in lang_chosen_dlg.keys() and 'author' in lang_chosen_dlg.keys():
                await send_dialogue_embed(ctx, lang_chosen_dlg)
                print(f'{now()}: [{user_id}] Sent dialogue ({user_dlg_id["major"]}, {user_dlg_id["minor"]}, {user_dlg_id["sub"]}).')
    
                jdata_chosen_dlg = jdata['game_data']['dialogue'][user_dlg_id['major']][user_dlg_id['minor']][user_dlg_id['sub']]
                print(f'{now()}: [{user_id}] Defined jdata_chosen_dlg')
                
                if 'input' not in jdata_chosen_dlg.keys():
                    print(f'{now()}: [{user_id}] Entered if scope.')
                    
                    self.update_dlg_id(user_id, jdata_chosen_dlg)
                    
                    await self.send_dlg(ctx)
                    print(f'{now()}: [{user_id}] Done with send_dlg recursion.')
                else:
                    print(f'{now()}: [{user_id}] Waiting on input.')
            else:
                await send_error(ctx, 'dlg_no_desc_or_author')
        else:
            await send_error(ctx, 'not_registered')
    

    def gen_starting_coords(self):
        (x, y) = (
                random.randint(jdata['config']['sectors']['width']['min'], jdata['config']['sectors']['width']['max']),
                random.randint(jdata['config']['sectors']['height']['min'], jdata['config']['sectors']['height']['max'])
            )

        clear = False
        while not clear:
            for i in range(x - 1, x + 2): # (x - 1) to (x + 1) inclusive
                for j in range(y - 1, y + 2):
                    if i == x and j == y:
                        break
                    # Check if system i, j is occupied (maybe checking system type? : evil, neutral, player)
    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{now()}: User cog is online.')


    @commands.command(aliases=['i', 'inv', 'data'])
    async def info(self, ctx):
        user_id = str(ctx.author.id)
        if user_id not in db['users'].keys():
            await send_error(ctx, 'not_registered')
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
                'username': '',
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
            
        await send_error(ctx, 'already_registered')

    
    @commands.command(aliases=['in'])
    async def input(self, ctx, *, input):
        user_id = str(ctx.author.id)
        if user_id in db['users'].keys():
            user_dlg_id = db['users'][user_id]['dialogue_id']
            jdata_chosen_dlg = jdata['game_data']['dialogue'][user_dlg_id['major']][user_dlg_id['minor']][user_dlg_id['sub']]

            if 'input' in jdata_chosen_dlg.keys():
                print(f'{now()}: [{user_id}] Tries to match "{input}" to "{jdata_chosen_dlg["input"]["name"]}".')
                if 'checks' in jdata_chosen_dlg['input'].keys() and not re.match(jdata_chosen_dlg['input']['checks']['regex'], input):
                    await send_dlg_error(ctx, jdata_chosen_dlg)
                    print(f'{now()}: [{user_id}] Error.')
                    return
                print(f'{now()}: [{user_id}] Success.')
                
                print(f'{now()}: [{user_id}] Tries {jdata_chosen_dlg["input"]["name"]} = "{input}".')
                exec(f'{jdata_chosen_dlg["input"]["name"]} = "{input}"')
                print(f'{now()}: [{user_id}] Success.')

                self.update_dlg_id(user_id, jdata_chosen_dlg)
                
                await self.send_dlg(ctx)
                print(f'{now()}: [{user_id}] Done with send_dlg recursion.')
            else:
                await send_error(ctx, 'dlg_no_input')
            return
            
        await send_error(ctx, 'already_registered')


    @commands.command(aliases=['dlg'])
    async def dialogue(self, ctx):
        await ctx.message.delete()
        await self.send_dlg(ctx)
        return


def setup(bot):
    bot.add_cog(User(bot))