from cogs.utils.time import now
from config import jdata


def trmprint(msg: str, type: str=None, time: bool=True):
    if type not in jdata['config']['colors']['trm']:
        type = None

    prefix, suffix = '', ''
    
    if type != None:
        trm_config = jdata['config']['colors']['trm']
        prefix, suffix = trm_config[type], trm_config['base']

    if time:
        prefix += f'[{now()}] '
    
    print(prefix + msg + suffix)