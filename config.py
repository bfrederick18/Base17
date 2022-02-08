import json
from os import listdir


jsons = listdir("json/")
print(jsons)

filenames = []
for file in jsons:
    filenames.append(file[:-5])

print(filenames)
filenames.sort()
print(filenames)

dicts = []
for file in filenames:
    with open(f'json/{file}.json', 'r') as f:
        dict_data = json.load(f)
        dicts.append(dict_data)

data = dict(zip(filenames, dicts))

print(data)