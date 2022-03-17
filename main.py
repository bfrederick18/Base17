import os

import discord

from cogs.utils.embed import send_error_embed, send_success_embed
from cogs.utils.time import now
from config import jdata, status_cycle
from discord.ext import commands, tasks
from server import keep_alive


token = os.environ['TOKEN']  # DON'T TOUCH
bot = commands.Bot(command_prefix=jdata['config']['prefix'])


def load(extension):
    bot.load_extension(f'cogs.{extension}')

def unload(extension):
    bot.unload_extension(f'cogs.{extension}')


@bot.event
async def on_ready():
    os.system('clear')
    print(jdata['config']['banner'] + '\n')
    print(f'{now()}: Logging in as {bot.user}.')
    c, l = os.get_terminal_size()
    print(f'{now()}: Terminal Size: ({c}, {l}).')
    print(f'{now()}: Starting status loop.')
    change_status.start()
    print(f'{now()}: Loading cogs.')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await send_error_embed(ctx, 'missing_arguments')
    print(f'{now()}: Unhandled Command Error: {error}')


@tasks.loop(seconds=150)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status_cycle)))


@bot.command()
@commands.is_owner()
async def loadcog(ctx, extension):
    try:
        print(f'{now()}: Loading \'cogs.{extension}\'...', end='', flush=True)
        load(extension)
        await ctx.message.delete()
        await send_success_embed(ctx, eval(jdata[jdata['config']['chosen_language']]['successes']['cog_loaded']))
        print(' Success.')
    except commands.ExtensionAlreadyLoaded as e:
        print('\033[31m' + f' Failed: {e}' + '\033[0m')
        await send_error_embed(ctx, 'cog_already_loaded')


@bot.command()
@commands.is_owner()
async def unloadcog(ctx, extension):
    try:
        print(f'{now()}: Unloading \'cogs.{extension}\'...', end='', flush=True)
        unload(extension)
        await ctx.message.delete()
        await send_success_embed(ctx, eval(jdata[jdata['config']['chosen_language']]['successes']['cog_unloaded']))
        print(' Success.')
    except commands.ExtensionNotLoaded as e:
        print('\033[31m' + f' Failed: {e}' + '\033[0m')
        await send_error_embed(ctx, 'cog_not_loaded')


@bot.command()
@commands.is_owner()
async def reloadcog(ctx, extension):
    try:
        print(f'{now()}: Reloading \'cogs.{extension}\'...', end='', flush=True)
        unload(extension)
        load(extension)
        await ctx.message.delete()
        await send_success_embed(ctx, eval(jdata[jdata['config']['chosen_language']]['successes']['cog_reloaded']))
        print(' Success.')
    except commands.ExtensionNotLoaded as e:
        print('\033[31m' + f' Failed: {e}' + '\033[0m')
        await send_error_embed(ctx, 'cog_not_loaded')


@bot.event
async def on_member_join(member):
    return


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


keep_alive()
print('Running bot')
bot.run(token)