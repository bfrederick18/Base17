import random
import re

import discord

from cogs.utils.dlg import send_dlg, update_dlg_id
from cogs.utils.embed import send_error_embed, send_dlg_error_embed
from cogs.utils.trm import trmprint
from config import jdata
from discord.ext import commands
from replit import db


class User(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    def gen_starting_coords(self, user_id):
        (x, y) = (0, 0)

        trmprint(f'[{user_id}] Rolled: ', end=' ', flush=True)
        clear = False
        while not clear:
            (x, y) = (
                random.randint(jdata['game_data']['systems']['width']['min'], jdata['game_data']['systems']['width']['max']),
                random.randint(jdata['game_data']['systems']['height']['min'], jdata['game_data']['systems']['height']['max'])
                )
            trmprint(f'({x}, {y})', time=False)
            trmprint(f'[{user_id}] Checking:', end=' ', flush=True)
            clear = True
            for i in range(x - 1, x + 2): # (x - 1) to (x + 1) inclusive
                for j in range(y - 1, y + 2):  # (y - 1) to (y + 1) inclusive
                    isLast = ((i == (x + 1)) and (j == (y + 1)))
                    
                    trmprint(f'({i}, {j}):', time=False, end=' ', flush=True)
                    if str(i) in db['systems'].keys() and str(j) in db['systems'][str(i)].keys():
                        clear = False
                        trmprint(f'N', type='failed', time=False, 
                                 end=('\n' if isLast else ', '), flush=(False if isLast else True))
                        continue

                    trmprint(f'Y', type='success', time=False, 
                             end=('\n' if isLast else ', '), flush=(False if isLast else True))

            if not clear:
                trmprint(f'[{user_id}] Rerolled:', end=' ', flush=True)
                
        trmprint(f'[{user_id}] Returning ({x}, {y})')
        return (x, y)


    def gen_system_data(self, user_id):
        types = jdata["game_data"]["systems"]["system_types"]
        roll_table = jdata["game_data"]["systems"]["system_types"]
        
        roll_counts = {}
        for i in roll_table:
            roll_counts[i] = roll_counts.get(i, 0) + 1
            
        trmprint(f'[{user_id}] system_types: {types}: {len(types)}')
        trmprint(f'[{user_id}] system_types_roll_table: {roll_counts}: {len(roll_table)}')
        
        system_data = {
            'allegiance': 'alien',
            'type': jdata['game_data']['systems']['system_types_roll_table'][random.randint(0, len(jdata['game_data']['systems']['system_types_roll_table']) - 1)],
            'stars': {},
            'planets': {}
        }
        return system_data


    @commands.Cog.listener()
    async def on_ready(self):
        trmprint(f'User cog is online.')


    @commands.command(aliases=['i', 'inv', 'data'])
    async def info(self, ctx):
        user_id = str(ctx.author.id)
        if user_id not in db['users'].keys():
            await send_error_embed(ctx, 'not_registered')
            return

        user_data = db['users'][user_id]
        embed = discord.Embed(
            description=f'Quarx: {user_data["quarx"]}\nShips: {len(user_data["ships"])}\n Colonies: {len(user_data["colonies"])}',
            color=int(jdata['config']['colors']['embed']['info'], 16))
        embed.set_author(name=f'[{user_data["username"]}] Personal Data.', icon_url=jdata['config']['icons']['success'])
        embed.set_footer(text=f'This data will expire in {jdata["config"]["delete_after"]["default"]} seconds.')
        await ctx.message.delete()
        await ctx.send(embed=embed, delete_after=jdata['config']['delete_after']['default'])


    @commands.command(aliases=['join', 'register'])
    async def start(self, ctx, username=''):
        user_id = str(ctx.author.id)
        if user_id not in db['users'].keys():
            (x, y) = self.gen_starting_coords(user_id)

            trmprint(f'[{user_id}] Initializing user_data...', end=' ', flush=True)
            user_data = {
                'username': 'Unknown',
                'prefix': '',
                'quarx': 0,
                'piloting': 'ship_0',
                'ships': {
                    '0': {
                        'name': 'Nomad',
                        'nickname': 'Unknown',
                        'coords': { 
                            'x': x, 
                            'y': y 
                        },
                        'fuel': 1
                    }
                },
                'next_ship': 1,
                'colonies': {},
                'dialogue_id': { 'major': '0', 'minor': '0', 'sub': '0' },
                'occupation': 'Unknown',
                'skills': {},
                'flags': []
            }
            trmprint('Success.', type='success', time=False)

            trmprint(f'[{user_id}] Setting user_data...', end=' ', flush=True)
            db['users'][str(ctx.author.id)] = user_data
            trmprint('Success.', type='success', time=False)
            
            system_data = self.gen_system_data(user_id)
            trmprint(f'[{user_id}] Created system_data.')

            if str(x) not in db['systems'].keys():
                db['systems'][str(x)] = {}

            db['systems'][str(x)][str(y)] = system_data
            
            trmprint(f'[{user_id}] Set system_data.')

            await send_dlg(ctx)
            return
            
        await send_error_embed(ctx, 'already_registered')

    
    @commands.command(aliases=['in'])
    async def input(self, ctx, *, input):
        user_id = str(ctx.author.id)
        if user_id in db['users'].keys():
            user_dlg_id = db['users'][user_id]['dialogue_id']
            jdata_chosen_dlg = jdata['game_data']['dialogue'][user_dlg_id['major']][user_dlg_id['minor']][user_dlg_id['sub']]

            if 'await' in jdata_chosen_dlg.keys() and 'type' in jdata_chosen_dlg['await'].keys():
                if jdata_chosen_dlg['await']['type'] == 'str':
                    if 'case' in jdata_chosen_dlg['await'] and not jdata_chosen_dlg['await']['case']:
                        input = input.lower()
                        
                    if 'checks' in jdata_chosen_dlg['await'].keys():
                        if 'regex' in jdata_chosen_dlg['await']['checks'].keys():
                            regex = jdata_chosen_dlg['await']['checks']['regex']
                            trmprint(f'[{user_id}] Tries to match "{input}" to "{regex}"...', end=' ', flush=True)
                            if not re.match(regex, input):
                                await send_dlg_error_embed(ctx, jdata_chosen_dlg)
                                trmprint('Failed.', type='failed', time=False)
                                return
                            trmprint('Success.', type='success', time=False)
                        elif 'array' in jdata_chosen_dlg['await']['checks'].keys():
                            array = jdata_chosen_dlg['await']['checks']['array']
                            trmprint(f'[{user_id}] Checking if "{input}" is in "{array}"...', end=' ', flush=True)
                            if input not in array:
                                await send_dlg_error_embed(ctx, jdata_chosen_dlg)
                                trmprint('Failed.', type='failed', time=False)
                                return
                            trmprint('Success.', type='success', time=False)
                            
                elif jdata_chosen_dlg['await']['type'] == 'int':
                    pass
                

                trmprint(f'[{user_id}] Setting {jdata_chosen_dlg["await"]["name"]} = "{input}"...', end=' ', flush=True)
                #try:
                exec(f'{jdata_chosen_dlg["await"]["name"]} = "{input}"')
                # except:
                    # print('\033[31m' + f' Failed: {}' + '\033[0m')
                trmprint('Success.', type='success', time=False)

                update_dlg_id(user_id, jdata_chosen_dlg)
                
                await send_dlg(ctx)
                trmprint(f'[{user_id}] Done with send_dlg recursion.')
            else:
                await send_error_embed(ctx, 'dlg_no_input')
            return
            
        await send_error_embed(ctx, 'not_registered')


    @commands.command(aliases=['dlg'])
    async def dialogue(self, ctx):
        await ctx.message.delete()
        await send_dlg(ctx)
        return


def setup(bot):
    bot.add_cog(User(bot))