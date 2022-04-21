import os

import discord

from cogs.utils.embed import send_error_embed, send_success_embed
from cogs.utils.trm import trmprint
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
    trmprint(jdata['config']['banner'] + '\n', time=False)
    trmprint(f'Logging in as {bot.user}.')
    c, l = os.get_terminal_size()
    trmprint(f'Terminal Size: ({c}, {l}).')
    trmprint('Starting status loop.')
    change_status.start()
    trmprint('Loading cogs.')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await send_error_embed(ctx, 'missing_arguments')

    trmprint(f'Unhandled Command Error: {error}')


@tasks.loop(seconds=150)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status_cycle)))


@bot.command()
@commands.is_owner()
async def loadcog(ctx, extension):
    try:
        trmprint(f'Loading \'cogs.{extension}\'...', end=' ', flush=True)
        load(extension)
        await ctx.message.delete()
        await send_success_embed(ctx, eval(jdata[jdata['config']['chosen_language']]['successes']['cog_loaded']))
        trmprint('Success.', type='success', time=False)
        
    except commands.ExtensionAlreadyLoaded as e:
        trmprint(f' Failed: {e}, {type(e)}', type='failed', time=False)
        await send_error_embed(ctx, 'cog_already_loaded')
    except commands.ExtensionNotFound as e:
        trmprint(f' Failed: {e}, {type(e)}', type='failed', time=False)
        await send_error_embed(ctx, 'cog_not_found')


@bot.command()
@commands.is_owner()
async def unloadcog(ctx, extension):
    try:
        trmprint(f'Unloading \'cogs.{extension}\'...', end=' ', flush=True)
        unload(extension)
        await ctx.message.delete()
        await send_success_embed(ctx, eval(jdata[jdata['config']['chosen_language']]['successes']['cog_unloaded']))
        trmprint('Success.', type='success', time=False)
        
    except commands.ExtensionNotLoaded as e:
        trmprint(f'Failed: {e}, {type(e)}', type='failed', time=False)
        await send_error_embed(ctx, 'cog_not_loaded')
    except commands.ExtensionNotFound as e:
        trmprint(f'Failed: {e}, {type(e)}', type='failed', time=False)
        await send_error_embed(ctx, 'cog_not_found')


@bot.command()
@commands.is_owner()
async def reloadcog(ctx, extension):
    try:
        trmprint(f'Reloading \'cogs.{extension}\'...', end=' ', flush=True)
        unload(extension)
        load(extension)
        await ctx.message.delete()
        await send_success_embed(ctx, eval(jdata[jdata['config']['chosen_language']]['successes']['cog_reloaded']))
        trmprint('Success.', type='success', time=False)
        
    except commands.ExtensionNotLoaded as e:
        trmprint(f'Failed: {e}, {type(e)}', type='failed', time=False)
        await send_error_embed(ctx, 'cog_not_loaded')
    except commands.ExtensionNotFound as e:
        trmprint(f'Failed: {e}, {type(e)}', type='failed', time=False)
        await send_error_embed(ctx, 'cog_not_found')


@bot.command()
@commands.is_owner()
async def reloadall(ctx):
    pass


@bot.event
async def on_member_join(member):
    return


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        cogname = filename[:-3]
        bot.load_extension(f'cogs.{cogname}')

keep_alive()
print('Running bot')
bot.run(token)