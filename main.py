import os

import discord

from cogs.utils.embed_tpl import error_tpl
from cogs.utils.time import now
from config import data, status_cycle, three_dots_cycle
from discord.ext import commands, tasks


token = os.environ['TOKEN']  # DON'T TOUCH
bot = commands.Bot(command_prefix=data['config']['prefix'])
alive_count = 0


@bot.event
async def on_ready():
    print(data['config']['banner'] + '\n')
    print(f'{now()}: Logging in as {bot.user}.')
    print(f'{now()}: Starting status loop.')
    change_status.start()
    print(f'{now()}: Loading cogs.')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=error_tpl(ctx, data[data['config']['chosen_language']]['missing_arguments_error']))
    print(f'{now()}: "{error}"')


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status_cycle)))
    print(f'{next(three_dots_cycle)}', end='', flush=True)


@bot.command()
@commands.is_owner()
async def loadcog(ctx, extension):
    bot.load_extension(f'cogs.{extension}')


@bot.command()
@commands.is_owner()
async def unloadcog(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')


@bot.command()
@commands.is_owner()
async def reloadcog(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')


@bot.event
async def on_member_join(member):
    return


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(token)