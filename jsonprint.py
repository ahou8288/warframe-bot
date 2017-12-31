import json
import os
from pprint import pprint
from multiprocessing import Pool
import pickle

folder_dir = './warframeitems/items/'

item_names = os.listdir(folder_dir)
# print(item_names)

def process_json(name):
    f = open(folder_dir + name, 'r')
    text = f.read()
    data = json.loads(text)
    return (data['en']['item_name'],data['url_name'])

results = Pool(4).map(process_json, item_names)

output = {key: value for (key, value) in results}

# pprint(output)

pickle.dump( output, open( "item_names.pickle", "wb" ) )