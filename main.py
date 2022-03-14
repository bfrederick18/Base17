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
    print(f'{now()}: Trying to load "{extension}" cog.')
    bot.load_extension(f'cogs.{extension}')
    print(f'{now()}: Loaded "{extension}" cog.')


def unload(extension):
    print(f'{now()}: Trying to unload "{extension}" cog.')
    bot.unload_extension(f'cogs.{extension}')
    print(f'{now()}: Unloaded "{extension}" cog.')


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


@tasks.loop(seconds=60)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status_cycle)))
    print(f'{now()}: Online: {round(bot.latency * 1000)}ms.')


@bot.command()
@commands.is_owner()
async def loadcog(ctx, extension):
    try:
        load(extension)
        await ctx.message.delete()
        await send_success_embed(ctx, f'Loaded "{extension}" cog.')
    except commands.ExtensionAlreadyLoaded as e:
        print(f'{now()}: *loadcog* Error: {e}')
        await send_error_embed(ctx, 'cog_already_loaded')


@bot.command()
@commands.is_owner()
async def unloadcog(ctx, extension):
    try:
        unload(extension)
        await ctx.message.delete()
        await send_success_embed(ctx, f'Unloaded "{extension}" cog.')
    except commands.ExtensionNotLoaded as e:
        print(f'{now()}: *unloadcog* Error: {e}')
        await send_error_embed(ctx, 'cog_not_loaded')


@bot.command()
@commands.is_owner()
async def reloadcog(ctx, extension):
    unload(extension)
    load(extension)
    await ctx.message.delete()
    await send_success_embed(ctx, f'Reloaded "{extension}" cog.')


@bot.event
async def on_member_join(member):
    return


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


keep_alive()
print('Running bot')
bot.run(token)