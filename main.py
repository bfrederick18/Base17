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
    if ('user' + str(ctx.author.id)) not in db.keys():
        if nick == '':
            await ctx.send(embed=error_tpl(ctx, c.start_requires_nick_error), delete_after=60.0)
            return

        user_data = {
            'id': ctx.author.id,
            'nick': nick,
            'bal': 0,
            'ships': [],
            'colonies': [],
        }
        db['user' + str(ctx.author.id)] = user_data
        await ctx.send('Done starting.')
    else:
        await ctx.send(embed=error_tpl(ctx, c.already_registered_error), delete_after=60.0)


@bot.command(aliases=['i'])
async def info(ctx):
    user = 'user' + str(ctx.author.id)
    if user not in db.keys():
        await ctx.send(embed=error_tpl(ctx, c.not_registered_error), delete_after=60.0)
    else:
        data = db[user]
        await ctx.send(f'{data["nick"]}\'s Info\nSilver: {data["bal"]}')


@bot.command(aliases=['m'])
async def mine(ctx):
    user = 'user' + str(ctx.author.id)
    if user not in db.keys():
        await ctx.send(embed=error_tpl(ctx, c.not_registered_error), delete_after=60.0)
    else:
        inc = 1
        bal = db[user]['bal']
        bal += 1
        db[user]['bal'] = bal
        embed = discord.Embed(
            description=f'Mined a profit of **{inc}** credit.',
            color=discord.Color.dark_gray())
        embed.set_author(name=f'[{ctx.author.name}] Successfully mined.',
                         icon_url=c.ore_icons[random.randint(0, 1)])
        embed.set_footer(text=f'Credit: {bal} | Profit: {inc}')
        await ctx.message.delete()
        await ctx.send(embed=embed, delete_after=60.0)


@bot.command(aliases=['_d'])  # PRIVATE
async def _debug(ctx, arg1='', arg2='', arg3='', arg4=''):
    if arg1 == 'id':
        await ctx.send(f'{ctx.author.id}')
    elif arg1 == 'db':  # DATABASE
        if arg2 == 'keys':
            await ctx.send(db.keys())
        elif arg2 == 'val' or arg2 == 'value':
            await ctx.send(db[arg3])
        elif arg2 == 'set':
            db[arg3] = arg4
        elif arg2 == 'del':
            del db[arg3]


@bot.event
async def on_member_join(member):
    return


bot.run(token)