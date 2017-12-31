import requests
from json import loads
from statistics import median
from statistics import mode
import pickle
from pprint import pprint
from fuzzywuzzy.fuzz import ratio

item_names = pickle.load(open("item_names.pickle", "rb"))


def find_url(search_string):
    if search_string in item_names:
        return item_names[search_string]
    else:
        scores = []
        for key, value in item_names.items():
            scores.append(
                [ratio(key.lower(), search_string.lower()), key, value])
        scores = sorted(scores, reverse=True, key=lambda x: x[0])
        return scores[0]


def item_lookup(search_url):
    # Build url for getting item purchases
    url = 'https://api.warframe.market/v1/items/{}/orders'
    url = url.format(search_url)

    # Send web request
    print('Getting data from server.')
    print('Request url : {}'.format(url))
    r = requests.get(url)

    # Convert json data which was returned into a python object
    print('Converting from json.')
    data = loads(r.text)

    return data


def get_totals(data):
    print('Looking through data to collect prices for each type of order.')
    buys, sells = [], []
    for order in data:
        if order['order_type'] == 'sell':
            sells.append(order['platinum'])
        elif order['order_type'] == 'buy':
            buys.append(order['platinum'])
    return (buys, sells)


def display_array(arr, label):
    print(label)
    print('Count  : {}'.format(len(arr)))
    print('Max    : {}'.format(max(arr)))
    print('Min    : {}'.format(min(arr)))
    print('Mode   : {}'.format(mode(arr)))
    print('Median : {}'.format(median(arr)))
    print('')

if __name__=='main':
    input_text = 'Cool'
    string_search =find_url(input_text)
    data = item_lookup(string_search[2])
    bought, sold = get_totals(data['payload']['orders'])
    print('\nItem data: {}'.format(string_search[1]))
    display_array(sold, 'Sold')
    display_array(bought, 'Buy')
