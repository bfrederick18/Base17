from cogs.utils.embed import send_error_embed, send_dialogue_embed
from cogs.utils.trm import trmprint
from config import jdata
from replit import db


def update_dlg_id(user_id, chosen_dlg):
    if 'after' not in chosen_dlg:
        return
        
    old_dlg_id = db['users'][user_id]['dialogue_id']
        
    if 'flag' in chosen_dlg['after']:
        flag = chosen_dlg['after']['flag']['name']
        db['users'][user_id]['flags'].append(flag)
        trmprint(f'[{user_id}] Added \'{flag}\' flag.')
        
    if 'dialogue' in chosen_dlg['after']:
        for tag in ['major', 'minor', 'sub']:
            db['users'][user_id]['dialogue_id'][tag] = chosen_dlg['after']['dialogue'][tag]
        
        new_dlg_id = db['users'][user_id]['dialogue_id']
        
        trmprint(f'[{user_id}] Updated dialogue_id from \
({old_dlg_id["major"]}, {old_dlg_id["minor"]}, {old_dlg_id["sub"]}) to \
({new_dlg_id["major"]}, {new_dlg_id["minor"]}, {new_dlg_id["sub"]}).')

        new_chosen_dlg = jdata['game_data']['dialogue'][new_dlg_id['major']][new_dlg_id['minor']][new_dlg_id['sub']]
        if 'before' in new_chosen_dlg:
            if 'flag' in new_chosen_dlg['before']:
                flag = new_chosen_dlg['before']['flag']['name']
                db['users'][user_id]['flags'].append(flag)
                trmprint(f'[{user_id}] Added \'{flag}\' flag.')

async def send_dlg(ctx):
    user_id = str(ctx.author.id)
    trmprint(f'[{user_id}] Entered send_dlg.')
    
    if user_id in db['users'].keys():
        user_dlg_id = db['users'][user_id]['dialogue_id']
        lang_chosen_dlg = jdata[jdata['config']['chosen_language']]['dialogue'][user_dlg_id['major']][user_dlg_id['minor']][user_dlg_id['sub']]
    
        if 'description' in lang_chosen_dlg.keys() and 'author' in lang_chosen_dlg.keys():
            await send_dialogue_embed(ctx, lang_chosen_dlg)
            trmprint(f'[{user_id}] Sent dialogue ({user_dlg_id["major"]}, {user_dlg_id["minor"]}, {user_dlg_id["sub"]}).')

            jdata_chosen_dlg = jdata['game_data']['dialogue'][user_dlg_id['major']][user_dlg_id['minor']][user_dlg_id['sub']]
            trmprint(f'[{user_id}] Defined jdata_chosen_dlg')
            
            if 'await' not in jdata_chosen_dlg.keys():
                trmprint(f'[{user_id}] Entered if scope.')
                
                update_dlg_id(user_id, jdata_chosen_dlg)
                
                await send_dlg(ctx)
                trmprint(f'[{user_id}] Done with send_dlg recursion.')
            else:
                trmprint(f'[{user_id}] Waiting on input.')
        else:
            await send_error_embed(ctx, 'dlg_no_desc_or_author')
    else:
        await send_error_embed(ctx, 'not_registered')