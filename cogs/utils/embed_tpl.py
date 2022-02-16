import discord

from config import jdata
from replit import db


def error_tpl(ctx, desc):
    user_id = str(ctx.author.id)
    
    embed = discord.Embed(description=desc, color=int(jdata['config']['colors']['error'], 16))
    embed.set_author(name=f'[{db["users"][user_id]["username"]}] Error', icon_url=jdata['config']['icons']['error'])
    return embed

def dialogue_tpl(author, desc):
    if desc == '':
        embed = discord.Embed(color=int(jdata['config']['colors']['error'], 16))
    else:
        embed = discord.Embed(description=desc, color=int(jdata['config']['colors']['error'], 16))
        
    if author != '':
        embed.set_author(name=author)
    return embed