import discord

from config import jdata


def error_tpl(ctx, desc):
    embed = discord.Embed(description=desc, color=discord.Color.red())
    embed.set_author(name=f'[{ctx.author.name}] Error', icon_url=jdata['config']['error_icon'])
    return embed