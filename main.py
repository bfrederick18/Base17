import cogs.utils.constants as c
import json
import os

import discord

from cogs.utils.embed_tpl import error_tpl
from cogs.utils.time import now
from config import data
from discord.ext import commands, tasks


config_data = data['config']
language_data = data[config_data['chosen_language']]
game_data = data['game_data']

token = os.environ['TOKEN']  # DON'T TOUCH
bot = commands.Bot(command_prefix=config_data['prefix'])
alive_count = 0


@bot.event
async def on_ready():
    print(config_data['banner'] + '\n')
    print(f'{now()}: Logging in as {bot.user}.')
    print(f'{now()}: Starting status loop.')
    change_status.start()
    print(f'{now()}: Loading cogs.')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=error_tpl(ctx, c.missing_arguments_error), delete_after=60.0)
    print(f'{now()}: "{error}"')


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(c.status)))
    print(f'{next(c.three_dots)}', end='', flush=True)


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')


@bot.event
async def on_member_join(member):
    return


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(token)