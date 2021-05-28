import urllib.request, urllib.parse, urllib.error
import json

import yahoo_fin.stock_info as si
from yahoo_fin.stock_info import get_data, tickers_sp500, tickers_nasdaq, tickers_other, get_quote_table

def sort_mom(elem):
    return elem[2]


def get_mom(index):
    """Get Momentum_12_2 list"""
    url = (f"https://pacific-hamlet-85745.herokuapp.com/{index}/")
    fhand = urllib.request.urlopen(url).read()
    data = json.loads(fhand)
    return data

def get_low_range(index):
    url = (f"https://pacific-hamlet-85745.herokuapp.com/{index}/")
    fhand = urllib.request.urlopen(url).read()
    data = json.loads(fhand)
    return data

def get_etf(etf):
    """Get Momentum_12_1 by etf"""
    url = (f"https://pacific-hamlet-85745.herokuapp.com/etf/{etf}/")
    fhand = urllib.request.urlopen(url).read()
    data = json.loads(fhand)
    return data


def get_etf_momentum():
    """Get momentum for ETF"""
    result = []
    url = (f"https://pacific-hamlet-85745.herokuapp.com/etf/")
    fhand = urllib.request.urlopen(url).read()
    data = json.loads(fhand)
    for item in data:
        name = item["name"]
        symbol = item["symbol"]
        momentum = item["momentum_12_1"]
        newtuple = symbol, name, momentum
        result.append(newtuple)
    return result

print(get_etf_momentum())
