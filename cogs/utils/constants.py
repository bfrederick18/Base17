import pytz

from itertools import cycle


prefix = '.'
banner = ''' ____                 _ _____ 
| __ )  __ _ ___  ___/ |___  |
|  _ \ / _` / __|/ _ \ |  / / 
| |_) | (_| \__ \  __/ | / /  
|____/ \__,_|___/\___|_|/_/   '''

status = cycle(['._.', 'o.o'])
three_dots = cycle(['.', '.', '.\n'])
ore_icons = ['https://i.postimg.cc/xCNFhrzq/ore4.png', 'https://i.postimg.cc/Sscfcm9L/ore6.png']

missing_arguments_error = 'Please include all required arguments. Check *help* for usage.'
start_requires_nick_error = '*Start* requires a nickname. Check *help* for usage.'
already_registered_error = 'You already used *start* to register before. Check *help* for usage.'
not_registered_error = 'You have not registered used *start* yet. Check *help* for usage.'
no_users_error = 'There appears to be no users. Ask a bot admin for help.'

tz = pytz.timezone('America/Vancouver')