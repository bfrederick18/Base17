from cogs.utils.embed import dialogue_tpl, error_tpl
from cogs.utils.time import now
from config import jdata
from replit import db


def update_dlg_id(user_id, chosen_dlg):
    db['users'][user_id]['dialogue_id']['major'] = chosen_dlg['next']['dialogue']['major']
    db['users'][user_id]['dialogue_id']['minor'] = chosen_dlg['next']['dialogue']['minor']
    db['users'][user_id]['dialogue_id']['sub'] = chosen_dlg['next']['dialogue']['sub']


async def send_dlg(ctx):
    user_id = str(ctx.author.id)
    if user_id in db['users'].keys():
        user_dlg_id = db['users'][user_id]['dialogue_id']
        en_chosen_dlg = jdata['en']['dialogue'][user_dlg_id['major']][user_dlg_id['minor']][user_dlg_id['sub']]
    
        if 'description' in en_chosen_dlg.keys() and 'author' in en_chosen_dlg.keys():
            await ctx.send(embed=dialogue_tpl(eval(en_chosen_dlg['author']), eval(en_chosen_dlg['description']), eval(en_chosen_dlg['footer'])))
            print(f'{now()}: [{user_id}] Sent dialogue (0, 0, 0).')

            jdata_chosen_dlg = jdata['game_data']['dialogue'][user_dlg_id['major']][user_dlg_id['minor']][user_dlg_id['sub']]
            print(f'{now()}: [{user_id}] Defined jdata_chosen_dlg')
            
            if 'input' not in jdata_chosen_dlg.keys():
                print(f'{now()}: [{user_id}] Entered if scope.')
                
                update_dlg_id(user_id, jdata_chosen_dlg)
                print(f'{now()}: [{user_id}] Updated major, minor, and sub.')
                
                await send_dlg(ctx)
                print(f'{now()}: [{user_id}] Done with send_dlg recursion.')
            else:
                print(f'{now()}: [{user_id}] Waiting on input.')
        else:
            await ctx.send(embed=error_tpl(ctx, jdata[jdata['config']['chosen_language']]['errors']['dlg_no_desc_or_author']))
    else:
        await ctx.send(embed=error_tpl(ctx, jdata[jdata['config']['chosen_language']]['errors']['not_registered']))