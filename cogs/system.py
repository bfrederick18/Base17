from cogs.utils.embed import send_error_embed
from cogs.utils.time import now
from discord.ext import commands
from replit import db


class System(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{now()}: System cog is online.')


    @commands.command()
    async def jump(self, ctx):
        if 'users' not in db.keys():
            await send_error_embed(ctx, 'no_users')
            return

        user_id = str(ctx.author.id)
        if user_id not in db['users'].keys():
            await send_error_embed(ctx, 'not_registered')
            return

        user_dlg_id = db['users'][user_id]['dialogue_id']
        
        await ctx.message.delete()
        await ctx.send(f'Pong: {round(self.bot.latency * 1000)}ms.')


def setup(bot):
    bot.add_cog(System(bot))