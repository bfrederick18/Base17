import discord

from config import jdata
from replit import db


def error_tpl(ctx, desc):  # Embed Error Template
    user_id = str(ctx.author.id)
    
    embed = discord.Embed(description=desc, color=int(jdata['config']['colors']['embed']['error'], 16))
    embed.set_author(name=f'[{db["users"][user_id]["username"]}] Error' if user_id in db['users'].keys() else 'Error',
                     icon_url=jdata['config']['icons']['error'])
    return embed


def success_tpl(ctx, desc):  # Embed Success Template
    user_id = str(ctx.author.id)
    
    embed = discord.Embed(description=desc, color=int(jdata['config']['colors']['embed']['success'], 16))
    embed.set_author(name=f'[{db["users"][user_id]["username"]}] Success' if user_id in db['users'].keys() else 'Success',
                     icon_url=jdata['config']['icons']['success'])
    return embed


def dialogue_tpl(author, desc, footer):  # Embed Dialogue Template
    if desc == '':
        embed = discord.Embed(color=int(jdata['config']['colors']['embed']['dialogue'], 16))
    else:
        embed = discord.Embed(description=desc, color=int(jdata['config']['colors']['embed']['dialogue'], 16))
        
    if author != '':
        embed.set_author(name=author)
    if footer != '':
        embed.set_footer(text=footer)
    return embed


async def send_success_embed(ctx, desc):
    await ctx.send(embed=success_tpl(ctx, desc), delete_after=jdata['config']['delete_after']['success'])


async def send_error_embed(ctx, error_name):
    await ctx.send(embed=error_tpl(ctx, jdata[jdata['config']['chosen_language']]['errors'][error_name]))


async def send_dlg_error_embed(ctx, jdata_chosen_dlg):
    await ctx.send(embed=error_tpl(ctx, jdata_chosen_dlg['await']['checks']['error_text']))


async def send_dialogue_embed(ctx, lang_chosen_dlg):
    await ctx.send(embed=dialogue_tpl(eval(lang_chosen_dlg['author']), eval(lang_chosen_dlg['description']), eval(lang_chosen_dlg['footer'])))