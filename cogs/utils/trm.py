from cogs.utils.time import now
from config import jdata

def trmprint(msg: str, color=None, time=True):
    if color == None:
        print(f'{now()}:' + f' {msg}')
        return

    trm_config = jdata['config']['colors']['trm']
    print(trm_config['error'] + msg + trm_config['base'])