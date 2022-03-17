import dictdiffer
import json
import os

from cogs.utils.embed import send_error_embed, send_success_embed
from cogs.utils.time import now
from config import jdata, reload_json
from discord.ext import commands
from replit import db
from replit.database import dumps


class Master(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    async def send_debug(self, ctx, message, args, arg_num):
        await ctx.send(message, delete_after=jdata['config']['delete_after']['debug'] if (len(args) < (arg_num + 1)) or args[arg_num] != 'perm' else 2000000)
    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{now()}: Master cog is online.')


    @commands.command()
    @commands.is_owner()
    async def reloadjson(self, ctx, extension, perm_arg=''):
        old_dict = jdata[extension]

        print(f'{now()}: Reloading {extension}.json...')
        reload_json(extension)
        print(f'{now()}: Done.')
        await ctx.message.delete()

        new_dict = jdata[extension]
        
        edits = []
        for diff in list(dictdiffer.diff(old_dict, new_dict)):
            edits.append(diff)

        print(f'{now()}: Edits: {edits}')
        await self.send_debug(ctx, edits, [perm_arg], 0)


    @commands.command()
    @commands.is_owner()
    async def db(self, ctx, *args):
        try:
            delete_msg = True
            
            if args[0] in db.keys():
                if args[1] in db[args[0]].keys():
                    if args[2] == 'reset' and args[4] == 'confirm':
                        db[args[0]][args[1]][args[3]] = {}
                        await send_success_embed(ctx, f'Reset "{args[3]}" in "{args[1]}" in "{args[0]}".')
                    elif args[2] == 'set':
                        db[args[0]][args[1]][args[3]] = args[4]
                        await send_success_embed(ctx, f'Set "{args[3]}" in "{args[1]}" in "{args[0]}" to "{args[4]}".')
                    else:
                        await send_error_embed(ctx, 'invalid_arguments')
                        delete_msg = False
                        
                elif args[1] == 'all':
                    await self.send_debug(ctx, f'```"{args[0]}": {json.dumps(json.loads(dumps(db[args[0]])), indent=4)}```', args, 2)
                elif args[1] == 'keys':
                    await self.send_debug(ctx, f'```{list(db[args[0]].keys())}```', args, 2)
                elif args[1] == 'val':
                    await self.send_debug(ctx, f'```{json.dumps(json.loads(dumps(db[args[0]][args[2]])), indent=4)}```', args, 3)
                elif args[1] == 'reset' and args[3] == 'confirm':
                    db[args[0]][args[2]] = {}
                    await send_success_embed(ctx, f'Reset "{args[2]}" in "{args[0]}".')
                elif args[1] == 'set':
                    db[args[0]][args[2]] = args[3]
                    await send_success_embed(ctx, f'Set "{args[2]}" in "{args[0]}" to "{args[3]}".')
                elif args[1] == 'del' and args[3] == 'confirm':
                    del db[args[0]][args[2]]
                    await send_success_embed(ctx, f'Deleted "{args[2]}" in "{args[0]}".')
                else:
                    await send_error_embed(ctx, 'invalid_arguments')
                    delete_msg = False
                    
            elif args[0] == 'all':
                for key in db.keys():
                    await self.send_debug(ctx, f'```"{key}": {json.dumps(json.loads(dumps(db[key])), indent=4)}```', args, 1)
            elif args[0] == 'keys':
                await self.send_debug(ctx, f'```{list(db.keys())}```', args, 1)
            elif args[0] == 'val':
                await self.send_debug(ctx, f'```{json.dumps(json.loads(dumps(db[args[1]])), indent=4)}```', args, 2)
            elif args[0] == 'reset' and args[2] == 'confirm':
                db[args[1]] = {}
                await send_success_embed(ctx, f'Reset "{args[1]}".')
            elif args[0] == 'del' and args[2] == 'confirm':
                del db[args[1]]
                await send_success_embed(ctx, f'Deleted "{args[1]}".')
            elif args[0] == 'base' and args[1] == 'confirm' and args[2] == 'confirm':
                db['users'] = {}
                db['systems'] = {}
                await send_success_embed(ctx, f'Reset "db" back to base state.')
            else:
                await send_error_embed(ctx, 'invalid_arguments')
                delete_msg = False

            if delete_msg:
                await ctx.message.delete()
                
        except IndexError as e:
            print(f'{now()}: IndexError: {e}: args = {args}')
            await send_error_embed(ctx, 'missing_arguments')

    
    @commands.command()
    @commands.is_owner()
    async def trm(self, ctx, *args):
        try:
            if args[0] == 'clear':
                os.system('clear')  # Might not want to delete everyting because keeping a log is important...
                # print('\n' * 100)
                print(jdata['config']['banner'] + '\n')
        except IndexError as e:
            print(f'{now()}: IndexError: {e}: args = {args}')
            await send_error_embed(ctx, 'missing_arguments')


    @commands.command()
    @commands.is_owner()
    async def pgrm(self, ctx, *args):
        try:
            delete_msg = True
            
            if args[0] == 'text':
                if args[1] in jdata['pgrm']['texts'].keys():
                    text = jdata['pgrm']['texts'][args[1]]
                    offset = len('``````')
                    while len(text) > (2000 - offset):
                        await ctx.send(f'```{text[0:(2000 - offset)]}```')
                        text = text[(2000 - offset):len(text)]
                    await ctx.send(f'```{text}```')
                else:
                    await send_error_embed(ctx, 'invalid_arguments')
                    delete_msg = False
            elif args[0] == 'link':
                if args[1] in jdata['pgrm']['links'].keys():
                    await ctx.send(f'```{jdata["pgrm"]["links"][args[1]]}```')
            else:
                await send_error_embed(ctx, 'invalid_arguments')
                delete_msg = False

            if delete_msg:
                await ctx.message.delete()
            
        except IndexError as e:
            print(f'{now()}: IndexError: {e}: args = {args}')
            await send_error_embed(ctx, 'missing_arguments')

def setup(bot):
    bot.add_cog(Master(bot))