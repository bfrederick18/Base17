import dictdiffer
import json

from cogs.utils.embed import error_tpl, send_success
from cogs.utils.time import now
from config import jdata, reload_json
from discord.ext import commands
from replit import db
from replit.database import dumps


class Master(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    async def send_debug(self, ctx, message, perm_arg):
        await ctx.send(message, delete_after=jdata['config']['delete_after']['debug'] if perm_arg != 'perm' else 2000000)
    

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
        await self.send_debug(ctx, edits, perm_arg)


    @commands.command()
    @commands.is_owner()
    async def db(self, ctx, *args):
        try:
            if args[0] in db.keys():
                if args[1] == 'all':
                    await self.send_debug(ctx, f'```"{args[0]}": {json.dumps(json.loads(dumps(db[args[0]])), indent=4)}```', args[2])
                elif args[1] == 'keys':
                    await self.send_debug(ctx, f'```{list(db[args[0]].keys())}```', args[2])
                elif args[1] == 'val':
                    await self.send_debug(ctx, f'```{json.dumps(json.loads(dumps(db[args[0]][args[2]])), indent=4)}```', args[3])
                elif args[1] == 'reset':
                    db[args[0]][args[2]] = {}
                    await send_success(ctx, f'Reset "{args[2]}" in "{args[0]}".')
                elif args[1] == 'del' and args[3] == 'confirm':
                    del db[args[0]][args[2]]
                    await send_success(ctx, f'Deleted "{args[2]}" in "{args[0]}".')
            elif args[0] == 'all':
                for key in db.keys():
                    await ctx.send(f'```"{key}": {json.dumps(json.loads(dumps(db[key])), indent=4)}```', delete_after=jdata['config']['delete_after']['debug'] if len(args) < 2 or args[1] != 'perm' else 2000000)
            elif args[0] == 'keys':
                await self.send_debug(ctx, f'```{list(db.keys())}```', args[1])
            elif args[0] == 'val':
                await self.send_debug(ctx, f'```{json.dumps(json.loads(dumps(db[args[1]])), indent=4)}```', args[2])
            elif args[0] == 'reset':
                db[args[1]] = {}
                await send_success(ctx, f'Reset "{args[1]}".')
            elif args[0] == 'del' and args[2] == 'confirm':
                del db[args[1]]
                await send_success(ctx, f'Deleted "{args[1]}".')
            await ctx.message.delete()
        except IndexError as e:
            print(f'{now()}: {e}: args = {args}')
            await ctx.send(embed=error_tpl(ctx, jdata[jdata['config']['chosen_language']]['errors']['missing_arguments']))


def setup(bot):
    bot.add_cog(Master(bot))