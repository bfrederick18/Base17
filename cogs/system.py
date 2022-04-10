from cogs.utils.embed import send_error_embed, send_success_embed
from cogs.utils.time import now
from config import jdata
from discord.ext import commands
from replit import db


class System(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{now()}: System cog is online.')


    @commands.command()
    async def jump(self, ctx, x, y):
        if 'users' not in db.keys():
            await send_error_embed(ctx, 'no_users')
            return
 
        user_id = str(ctx.author.id)
        if user_id not in db['users'].keys():
            await send_error_embed(ctx, 'not_registered')
            return

        print(f'{now()}: Checking if "{self.jump.name}" command is unlocked...',
              end='',
              flush=True)
        
        if 'cmd_jump_unlocked' not in db['users'][user_id]['flags']:
            print('\033[31m' + f' Failed: "{self.jump.name}" command is locked.' + '\033[0m')
            await send_error_embed(ctx, 'command_locked')
            return
            
        print(' Success.')

        # if 'ship' in db['users'][user_id]['piloting']:
        ship_id = db['users'][user_id]['piloting'][len('ship_'):]  # ship_0 -> 0
        ship = db['users'][user_id]['ships'][ship_id]

        x_dist = int(x) - ship['coords']['x']
        y_dist = int(y) - ship['coords']['y']
        raw_dist = (x_dist ** 2 + y_dist ** 2) ** (1/2)
        dist = round(raw_dist)
        fuel = ship['fuel']

        print(f'{now()}: Jumping ship "{ship_id}" from ({ship["coords"]["x"]},{ship["coords"]["y"]}) to ({x},{y}), a distance of {dist} (raw_dist: {round(raw_dist, 4)}) with {fuel} unit(s) of fuel...', end='', flush=True)
        
        if dist > fuel:
            print('\033[31m' + ' Failed: NotEnoughtFuelShip.' + '\033[0m')
            await send_error_embed(ctx, 'not_enough_fuel_ship')
            return
        
        db['users'][user_id]['ships'][ship_id]['fuel'] = fuel - dist
        db['users'][user_id]['ships'][ship_id]['coords']['x'] = int(x)
        db['users'][user_id]['ships'][ship_id]['coords']['y'] = int(y)

        await ctx.message.delete()
        await send_success_embed(ctx, eval(jdata[jdata['config']['chosen_language']]['successes']['jump_ship']))
        print(' Success.')


def setup(bot):
    bot.add_cog(System(bot))