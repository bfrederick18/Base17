import json
import pytz

from os import listdir
from itertools import cycle

jdata = {}


def load_all_json():
    jsons = listdir("json/")

    filenames = []
    for file in jsons:
        filenames.append(file[:-len('.json')])
    filenames.sort()

    dicts = []
    for file in filenames:
        print(f'{file}.json: Opened...', end='', flush=True)
        with open(f'json/{file}.json', 'r') as f:
            dict_data = json.load(f)
            dicts.append(dict_data)
        print(f' Closed.')

    return dict(zip(filenames, dicts))


def reload_json(filename):
    with open(f'json/{filename}.json', 'r') as f:
        jdata[filename] = json.load(f)


jdata = load_all_json()
# print(json.dumps(jdata, indent=4))

status_cycle = cycle(jdata['config']['status'])
three_dots_cycle = cycle(jdata['config']['three_dots'])
tz = pytz.timezone(jdata['config']['tz'])