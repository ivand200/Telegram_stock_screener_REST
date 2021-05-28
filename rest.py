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
    lst = list()
    count = 0
    for item in data:
        symbol = item["symbol"]
        name = item["name"]
        momentum = item["momentum_12_2"]
        newtuple = symbol, name, momentum
        lst.append(newtuple)

    lst.sort(key=sort_mom, reverse=True)
    short_lst = lst[:20]
    best_list = "\n".join(str(el) for el in short_lst)
    best_20 = best_list.replace("(","").replace(")","").replace("'", "")
    return best_20


def get_div():
    """Get dividend stocks list"""
    url = (f"https://pacific-hamlet-85745.herokuapp.com/divs/")
    fhand = urllib.request.urlopen(url).read()
    data = json.loads(fhand)
    lst = list()
    for item in data:
        symbol = item["symbol"]
        name = item["name"]
        div = item["div_p"]
        newtuple = symbol, name, div
        lst.append(newtuple)
    lst.sort(key=sort_mom, reverse=True)
    short_lst = lst[:20]
    best_list = "\n".join(str(el) for el in short_lst)
    best_20 = best_list.replace("(","").replace(")","").replace("'", "")
    return best_20


def get_etf(etf):
    """Get Momentum_12_1 by etf"""
    url = (f"https://pacific-hamlet-85745.herokuapp.com/etf/{etf}/")
    fhand = urllib.request.urlopen(url).read()
    data = json.loads(fhand)
    name  = data["name"]
    mom = data["momentum_12_1"]
    ma = data["ma10"]
    return f"{name}, \nMomentum: {mom}, \nMA10: {ma}"


def get_etf_momentum():
    """Get momentum for ETF"""
    lst = ["SHV", "IVV", "EFA", "AGG"]
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
    result.sort(key=sort_mom, reverse=True)
    best_list = "\n".join(str(el) for el in result)
    best_20 = best_list.replace("(","").replace(")","").replace("'", "")
    return best_20



def get_low_range(index):
    """1 if price trade at low for last 5 years"""
    url = (f"https://pacific-hamlet-85745.herokuapp.com/{index}/")
    fhand = urllib.request.urlopen(url).read()
    data = json.loads(fhand)
    lst = list()
    for item in data:
        if item["low_range"] == 1:
            symbol = item["symbol"]
            name = item["name"]
            newtuple = symbol, name
            lst.append(newtuple)
    best_list = "\n".join(str(el) for el in lst[:20])
    best_20 = best_list.replace("(","").replace(")","").replace("'", "")
    return best_20
