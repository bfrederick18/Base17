import json
import pytz

from os import listdir
from itertools import cycle


jdata = {}


def load_all_json():
    jsons = listdir("json/")

    filenames = []
    for file in jsons:
        filenames.append(file[:-5])

    filenames.sort()

    dicts = []
    for file in filenames:
        with open(f'json/{file}.json', 'r') as f:
            dict_data = json.load(f)
            dicts.append(dict_data)

    return dict(zip(filenames, dicts))

    # print(json.dumps(jdata, indent=4))


def reload_json(filename):
    with open(f'json/{filename}.json', 'r') as f:
        jdata[filename] = json.load(f)


jdata = load_all_json()

status_cycle = cycle(jdata['config']['status'])
three_dots_cycle = cycle(jdata['config']['three_dots'])
tz = pytz.timezone(jdata['config']['tz'])