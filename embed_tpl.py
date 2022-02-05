import constants as c
import discord


def error_tpl(ctx, desc):
    embed = discord.Embed(description=desc, color=discord.Color.red())
    embed.set_author(name=f'[{ctx.author.name}] Error', icon_url='https://i.postimg.cc/P5LQBHL1/4691426-x-icon.png')
    return embed