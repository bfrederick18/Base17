from cogs.utils.time import now

def trmprint(msg: str, color=None):
    if color == None:
        print(f'{now()}: {msg}')
    else:
        if color == 'error':
            print('\033[31m' + ' Failed: NotEnoughtFuelShip.' + '\033[0m')