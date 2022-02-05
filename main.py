import constants as c
from datetime import datetime
import discord
from discord.ext import commands, tasks
from embed_tpl import error_tpl
import math
import os
import pytz
import random
from replit import db


token = os.environ['TOKEN']  # DON'T TOUCH
bot = commands.Bot(command_prefix=c.prefix)
alive_count = 0
tz = pytz.timezone('America/Vancouver')


def now():
    return f'{datetime.now(tz).strftime("%Y/%m/%d %H:%M:%S")} {str(math.trunc(int(datetime.now(tz).strftime("%f")) / 100)).zfill(4)}'


@bot.event
async def on_ready():
    print(c.banner + '\n')
    print(f'{now()}: Logged in as {bot.user}.')
    change_status.start()
    print(f'{now()}: Started status loop.')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=error_tpl(ctx, c.missing_arguments_error), delete_after=60.0)
    print(error)


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(c.status)))
    print(f'{next(c.three_dots)}', end='', flush=True)


@bot.command(aliases=['p'])
async def ping(ctx):
    await ctx.message.delete()
    await ctx.send(f'Pong: {round(bot.latency * 1000)}ms.')


@bot.command()
async def clear(ctx, amount: int):
    await ctx.message.delete()
    deleted = await ctx.channel.purge(limit=amount)
    # await ctx.send(f'Cleared {len(deleted)} message(s) by {ctx.author.mention}')


@bot.command(aliases=['join', 'register'])
async def start(ctx, nick=''):
    user_id = str(ctx.author.id)
    if user_id not in db['users'].keys():
        if nick == '':
            await ctx.send(embed=error_tpl(ctx, c.start_requires_nick_error), delete_after=60.0)
            return

        user_data = {
            'nick': nick,
            'bal': 0,
            'ships': {},
            'colonies': {},
        }
        db['users'][int(ctx.author.id)] = user_data
        await ctx.send('Done starting.')
        return
    await ctx.send(embed=error_tpl(ctx, c.already_registered_error), delete_after=60.0)


@bot.command(aliases=['i'])
async def info(ctx):
    user_id = str(ctx.author.id)
    if user_id not in db['users'].keys():
        await ctx.send(embed=error_tpl(ctx, c.not_registered_error), delete_after=60.0)
        return
    data = db['users'][user_id]
    await ctx.send(f'{data["nick"]}\'s Info\nSilver: {data["bal"]}')


@bot.command(aliases=['m'])
async def mine(ctx):
    if 'users' not in db.keys():
        await ctx.send(embed=error_tpl(ctx, c.no_users_error))  # Do not delete
        return
    user_id = str(ctx.author.id)
    if user_id not in db['users'].keys():
        await ctx.send(embed=error_tpl(ctx, c.not_registered_error), delete_after=60.0)
        return
    
    inc = 1
    db['users'][user_id]['bal'] += inc
    bal = db['users'][user_id]['bal']
    embed = discord.Embed(
        description=f'Mined a profit of **{inc}** credit.',
        color=discord.Color.dark_gray())
    embed.set_author(name=f'[{ctx.author.name}] Successfully mined.',
                        icon_url=c.ore_icons[random.randint(0, 1)])
    embed.set_footer(text=f'Credit: {bal} | Profit: {inc}')
    await ctx.message.delete()
    await ctx.send(embed=embed, delete_after=60.0)


@bot.event
async def on_member_join(member):
    return


bot.run(token)