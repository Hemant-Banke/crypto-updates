from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
from .models import Room, Exchanges

import requests
import asyncio
import json
from asgiref.sync import sync_to_async
from collections import defaultdict


def index(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    rooms = Room.objects.order_by("title")

    # Render that in the index template
    return render(request, "index.html", {
        "rooms": rooms,
    })


def exchange_list(request):
    """
    Lists the exchanges used by coingecko
    """
    return render(request, "exchanges.html", {})


def fetch(url):
    r = requests.get(url)
    return r.json()


@sync_to_async
def req_data():
    import re

    exchanges = Exchanges.objects.all()
    data = defaultdict(list)

    for exchange in exchanges:
        if (exchange.is_all_coins):

            exc_sym_format = exchange.symbol_format.split('{symbol}')
            exc_sym_pre = len(exc_sym_format[0])
            exc_sym_app = len(exc_sym_format[1])

            price_data = []
            # Get price data
            price_data = fetch(exchange.price_endpoint)

            # add price data to dictionary
            price_datatype = exchange.price_datatype

            # get price path
            if (price_datatype['path'] and price_datatype['path'] != ''):
                path = price_datatype['path'].split('.')
                for i in range(len(path)):
                    price_data = price_data[path[i]]

            for symbol in price_data:
                has_usdt = exchange.has_usdt

                # naming
                name = symbol[price_datatype['name']]
                name_bin = re.sub(r'\W+', '', name)
                name_bin = name_bin.upper()

                if (exc_sym_app > 0):
                    name_bin = name_bin[exc_sym_pre : -1*exc_sym_app]
                else:
                    name_bin = name_bin[exc_sym_pre : ]

                if (not has_usdt):
                    last3 = name_bin[len(name_bin)-3 :]
                    name_bin = name_bin + 'T' if (last3 == 'USD') else name_bin

                # Per exchange checks
                is_valid = True
                # Volume > 0
                volume = float(symbol[price_datatype['volume']] if price_datatype['volume'] else '')
                is_valid &= volume > 0

                if (is_valid):
                    data[name_bin].append({
                        'name' : name,
                        'price' : float(symbol[price_datatype['price']]),
                        'volume' : volume,
                        'bid' : symbol[price_datatype['bid']] if price_datatype['bid'] else '',
                        'ask' : symbol[price_datatype['ask']] if price_datatype['ask'] else '',
                        'exchange' : exchange.exchange_name,
                        'exchange_id' : exchange.id,
                    })

    # sort each symbol
    symbols = defaultdict(lambda: defaultdict(list))
    for symbol in data:
        if len(data[symbol]) >= 2:
            # Sort the multiple exchanges
            sorted_symbol = sorted(data[symbol], key=lambda k: k['price'])

            # Validate for symbol
            is_valid = True
            # Profit > 3% for end exchanges
            profit = (sorted_symbol[-1]['price'] - sorted_symbol[0]['price'])*100/sorted_symbol[0]['price']
            is_valid &= profit > 3

            if (is_valid):
                symbols[symbol]['data'] = [sorted_symbol[0], sorted_symbol[-1]]
                symbols[symbol]['is_new'] = True

    return json.dumps(symbols)
