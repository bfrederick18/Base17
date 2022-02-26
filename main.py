import os

import discord

from cogs.utils.embed import send_error, send_success
from cogs.utils.time import now
from config import jdata, status_cycle
from discord.ext import commands, tasks


token = os.environ['TOKEN']  # DON'T TOUCH
bot = commands.Bot(command_prefix=jdata['config']['prefix'])
alive_count = 0


@bot.event
async def on_ready():
    print(jdata['config']['banner'] + '\n')
    print(f'{now()}: Logging in as {bot.user}.')
    print(f'{now()}: Starting status loop.')
    change_status.start()
    print(f'{now()}: Loading cogs.')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await send_error(ctx, 'missing_arguments')
    print(f'{now()}: Error: {error}')


@tasks.loop(seconds=60)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status_cycle)))
    print(f'{now()}: Online.')


@bot.command()
@commands.is_owner()
async def loadcog(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.message.delete()
    await send_success(ctx, f'Loaded cog "{extension}".')


@bot.command()
@commands.is_owner()
async def unloadcog(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.message.delete()
    await send_success(ctx, f'Unloaded cog "{extension}".')


@bot.command()
@commands.is_owner()
async def reloadcog(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.message.delete()
    await send_success(ctx, f'Reloaded cog "{extension}".')


@bot.event
async def on_member_join(member):
    return


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(token)