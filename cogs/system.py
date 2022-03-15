from cogs.utils.embed import send_error_embed
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

        user_dlg_id = db['users'][user_id]['dialogue_id']

        print(f'{now()}: Checking if "{self.jump.name}" command is unlocked.')
        unlocked = True
        for tag in ['major', 'minor', 'sub']:
            if int(user_dlg_id[tag]) < int(jdata['game_data']['commands'][self.jump.name]['unlock']['dialogue'][tag]):
                unlocked = False
                
        print(f'{now()}: "{self.jump.name}" command is {"unlocked" if unlocked else "locked"}.')
        if not unlocked:
            await send_error_embed(ctx, 'command_locked')
            return

        
        if 'ship' in db['users'][user_id]['piloting']:
            ship_id = db['users'][user_id]['piloting'][len('ship_'):]  # ship_0 -> 0
            ship = db['users'][user_id]['ships'][ship_id]

            x_dist = int(x) - ship['coords']['x']
            y_dist = int(y) - ship['coords']['y']
            raw_dist = (x_dist ** 2 + y_dist ** 2) ** (1/2)
            dist = round(raw_dist)
            fuel = ship['fuel']

            print(f'{now()}: Jumping ship "{ship_id}" from ({ship["coords"]["x"]},{ship["coords"]["y"]}) to ({x},{y}), a distance of {dist} (raw_dist: {round(raw_dist, 4)}) with {fuel} unit(s) of fuel.')
            
            print(dist)
            if dist > fuel:
                
                return
        else:
            # Send Error Message Not Enought Fuel
            return 


def setup(bot):
    bot.add_cog(System(bot))