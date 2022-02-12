import discord

from config import jdata


def error_tpl(ctx, desc):
    embed = discord.Embed(description=desc, color=int(jdata['config']['colors']['error'], 16))
    embed.set_author(name=f'[{ctx.author.name}] Error', icon_url=jdata['config']['icons']['error'])
    return embed