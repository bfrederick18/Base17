import random
import re

import discord

from cogs.utils.embed import send_error_embed, send_dlg_error_embed, send_dialogue_embed
from cogs.utils.time import now
from config import jdata
from discord.ext import commands
from replit import db


class User(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    def update_dlg_id(self, user_id, chosen_dlg):
        old_dlg_id = db['users'][user_id]['dialogue_id']

        if 'after' in chosen_dlg:
            if 'flag' in chosen_dlg['after']:
                flag = chosen_dlg['after']['flag']['name']
                db['users'][user_id]['flags'].append(flag)
                print(f'{now()}: [{user_id}] Added \'{flag}\' flag.')
                
            if 'dialogue' in chosen_dlg['after']:
                for tag in ['major', 'minor', 'sub']:
                    db['users'][user_id]['dialogue_id'][tag] = chosen_dlg['after']['dialogue'][tag]
                
                new_dlg_id = db['users'][user_id]['dialogue_id']
                
                print(f'{now()}: [{user_id}] Updated dialogue_id from \
({old_dlg_id["major"]}, {old_dlg_id["minor"]}, {old_dlg_id["sub"]}) to \
({new_dlg_id["major"]}, {new_dlg_id["minor"]}, {new_dlg_id["sub"]}).')

                new_chosen_dlg = jdata['game_data']['dialogue'][new_dlg_id['major']][new_dlg_id['minor']][new_dlg_id['sub']]
                if 'before' in new_chosen_dlg:
                    if 'flag' in new_chosen_dlg['before']:
                        flag = new_chosen_dlg['before']['flag']['name']
                        db['users'][user_id]['flags'].append(flag)
                        print(f'{now()}: [{user_id}] Added \'{flag}\' flag.')

    async def send_dlg(self, ctx):
        user_id = str(ctx.author.id)
        print(f'{now()}: [{user_id}] Entered send_dlg.')
        
        if user_id in db['users'].keys():
            user_dlg_id = db['users'][user_id]['dialogue_id']
            lang_chosen_dlg = jdata[jdata['config']['chosen_language']]['dialogue'][user_dlg_id['major']][user_dlg_id['minor']][user_dlg_id['sub']]
        
            if 'description' in lang_chosen_dlg.keys() and 'author' in lang_chosen_dlg.keys():
                await send_dialogue_embed(ctx, lang_chosen_dlg)
                print(f'{now()}: [{user_id}] Sent dialogue ({user_dlg_id["major"]}, {user_dlg_id["minor"]}, {user_dlg_id["sub"]}).')
    
                jdata_chosen_dlg = jdata['game_data']['dialogue'][user_dlg_id['major']][user_dlg_id['minor']][user_dlg_id['sub']]
                print(f'{now()}: [{user_id}] Defined jdata_chosen_dlg')
                
                if 'await' not in jdata_chosen_dlg.keys():
                    print(f'{now()}: [{user_id}] Entered if scope.')
                    
                    self.update_dlg_id(user_id, jdata_chosen_dlg)
                    
                    await self.send_dlg(ctx)
                    print(f'{now()}: [{user_id}] Done with send_dlg recursion.')
                else:
                    print(f'{now()}: [{user_id}] Waiting on input.')
            else:
                await send_error_embed(ctx, 'dlg_no_desc_or_author')
        else:
            await send_error_embed(ctx, 'not_registered')


    def gen_starting_coords(self, user_id):
        (x, y) = (0, 0)

        clear = False
        while not clear:
            (x, y) = (
                random.randint(jdata['game_data']['systems']['width']['min'], jdata['game_data']['systems']['width']['max']),
                random.randint(jdata['game_data']['systems']['height']['min'], jdata['game_data']['systems']['height']['max'])
                )
            print(f'{now()}: [{user_id}] Rolled ({x}, {y})')
            
            clear = True
            for i in range(x - 1, x + 2): # (x - 1) to (x + 1) inclusive
                for j in range(y - 1, y + 2):  # (y - 1) to (y + 1) inclusive
                    if (i == x) and (j == y):  # Not (x, y)
                        continue
                    print(f'{now()}: [{user_id}] Checking ({i}, {j})')
                    if str(i) in db['systems'].keys() and str(j) in db['systems'][str(i)].keys():
                        clear = False
                        print(f'{now()}: [{user_id}] Conflict on ({i}, {j})')
                        
        print(f'{now()}: [{user_id}] Returning ({x}, {y})')
        return (x, y)


    def gen_system_data(self, user_id):
        print(f'{now()}: [{user_id}] system_types: {jdata["game_data"]["systems"]["system_types"]}: {len(jdata["game_data"]["systems"]["system_types"])}')
        print(f'{now()}: [{user_id}] system_types_roll_table: {jdata["game_data"]["systems"]["system_types_roll_table"]}: {len(jdata["game_data"]["systems"]["system_types_roll_table"])}')
        
        system_data = {
            'allegiance': 'alien',
            'type': jdata['game_data']['systems']['system_types_roll_table'][random.randint(0, len(jdata['game_data']['systems']['system_types_roll_table']) - 1)],
            'stars': {},
            'planets': {}
        }
        return system_data


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{now()}: User cog is online.')


    @commands.command(aliases=['i', 'inv', 'data'])
    async def info(self, ctx):
        user_id = str(ctx.author.id)
        if user_id not in db['users'].keys():
            await send_error_embed(ctx, 'not_registered')
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
            (x, y) = self.gen_starting_coords(user_id)
            
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
            print(f'{now()}: [{user_id}] Created user_data.')
            
            db['users'][str(ctx.author.id)] = user_data
            print(f'{now()}: [{user_id}] Set user_data.')
            
            system_data = self.gen_system_data(user_id)
            
            print(f'{now()}: [{user_id}] Created system_data.')

            if str(x) not in db['systems'].keys():
                db['systems'][str(x)] = {}

            db['systems'][str(x)][str(y)] = system_data
            
            print(f'{now()}: [{user_id}] Set system_data.')

            await self.send_dlg(ctx)
            return
            
        await send_error_embed(ctx, 'already_registered')

    
    @commands.command(aliases=['in'])
    async def input(self, ctx, *, input):
        user_id = str(ctx.author.id)
        if user_id in db['users'].keys():
            user_dlg_id = db['users'][user_id]['dialogue_id']
            jdata_chosen_dlg = jdata['game_data']['dialogue'][user_dlg_id['major']][user_dlg_id['minor']][user_dlg_id['sub']]

            if 'await' in jdata_chosen_dlg.keys():
                if 'case' in jdata_chosen_dlg['await'] and not jdata_chosen_dlg['await']['case']:
                    input = input.lower()
                if 'checks' in jdata_chosen_dlg['await'].keys():
                    if 'regex' in jdata_chosen_dlg['await']['checks'].keys():
                        regex = jdata_chosen_dlg['await']['checks']['regex']
                        print(f'{now()}: [{user_id}] Tries to match "{input}" to "{regex}".',
                              end='',
                              flush=True)
                        if not re.match(regex, input):
                            await send_dlg_error_embed(ctx, jdata_chosen_dlg)
                            print('\033[31m' + f' Failed.' + '\033[0m')
                            return
                        print(' Success.')
                    elif 'array' in jdata_chosen_dlg['await']['checks'].keys():
                        array = jdata_chosen_dlg['await']['checks']['array']
                        print(f'{now()}: [{user_id}] Checking if "{input}" is in "{array}".',
                              end='',
                              flush=True)
                        if input not in array:
                            await send_dlg_error_embed(ctx, jdata_chosen_dlg)
                            print('\033[31m' + f' Failed.' + '\033[0m')
                            return
                        print(' Success.')
                

                print(f'{now()}: [{user_id}] Setting {jdata_chosen_dlg["await"]["name"]} = "{input}"...',
                      end='',
                      flush=True)
                #try:
                exec(f'{jdata_chosen_dlg["await"]["name"]} = "{input}"')
                # except:
                    # print('\033[31m' + f' Failed: {}' + '\033[0m')
                print(' Success.')

                self.update_dlg_id(user_id, jdata_chosen_dlg)
                
                await self.send_dlg(ctx)
                print(f'{now()}: [{user_id}] Done with send_dlg recursion.')
            else:
                await send_error_embed(ctx, 'dlg_no_input')
            return
            
        await send_error_embed(ctx, 'not_registered')


    @commands.command(aliases=['dlg'])
    async def dialogue(self, ctx):
        await ctx.message.delete()
        await self.send_dlg(ctx)
        return


def setup(bot):
    bot.add_cog(User(bot))