from cogs.utils.time import now
from config import jdata


def trmprint(msg: str, type: str=None, time: bool=True, end='\n', flush=False):
    if type not in jdata['config']['colors']['trm']:
        type = None

    prefix, suffix = '', ''
    
    if type != None:
        trm_config = jdata['config']['colors']['trm']
        prefix, suffix = f'\033[{trm_config[type]}m', f'\033[{trm_config["base"]}m'

    if time:
        prefix += f'[{now()}] '
    
    print(prefix + msg + suffix, end=end, flush=flush)