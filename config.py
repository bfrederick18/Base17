import json
import pytz

from os import listdir
from itertools import cycle


global data
data = {}


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

    # print(json.dumps(data, indent=4))


def reload_json(filename):
    with open(f'json/{filename}.json', 'r') as f:
        data[filename] = json.load(f)


data = load_all_json()

status_cycle = cycle(data['config']['status'])
three_dots_cycle = cycle(data['config']['three_dots'])
tz = pytz.timezone(data['config']['tz'])