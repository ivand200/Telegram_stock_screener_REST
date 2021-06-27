import urllib.request, urllib.parse, urllib.error
import json
import requests
import yahoo_fin.stock_info as si
from yahoo_fin.stock_info import get_data, tickers_sp500, tickers_nasdaq, tickers_other, get_quote_table
import pandas as pd
import yfinance as yf

# Define previous month
from datetime import datetime, timedelta
now = datetime.now()
lastmonth = now - timedelta(weeks=5)
endoflastmonth = lastmonth.replace(day=28)
month_ago = endoflastmonth.strftime("%Y-%m-%d")
start_ = now - timedelta(weeks=120)
start_time = start_.strftime("%Y-%m-%d")

def sort_mom(elem):
    return elem[2]


def ma10(series: pd.Series, ma):
    """
    Takes a times series of asset returns
    Computes and returns a DataFrame that contains:
    the wealth index
    the previous peaks
    perecent drawdowns
    """
    series['MA10'] = series['Close'].rolling(ma).mean()
    series['Shares'] = [1 if series.loc[ei, 'Close'] > series.loc[ei, 'MA10'] else 0 for ei in series.index]
    series['Close1'] = series['Close'].shift(-1)
    series['Change'] = (series['Close1'] - series['Close']) / series['Close']
    series['Profit'] = [series.loc[ei, 'Change'] if series.loc[ei, 'Shares'] == 1 else 0 for ei in series.index]
    series['Wealth'] = 1000 * (1 + series['Profit']).cumprod()
    return series['Wealth']


def drawdown(series: pd.Series):
    wealth_index = 1000 * (1 + series.pct_change()).cumprod()
    previous_peaks = wealth_index.cummax()
    drawdowns = (wealth_index - previous_peaks) / previous_peaks
    return drawdowns


def test(share, ma):
    ticker = yf.Ticker(share)
    ticker = ticker.history(start="2001-01-01", end=month_ago, interval="1mo")
    ticker = ticker[ticker["Close"].notna()]
    profit = round(ma10(ticker, ma), 2)
    max_drawdown = round(drawdown(profit).min(), 2)
    return f"Max drawdown: {max_drawdown}\nProfit: {profit[-2]}"

def get_avg_momentum(index):
    """Get Momentum_12_2 list"""
    url = requests.get(f"http://ivand200.pythonanywhere.com/{index}/").json()
    lst = list()
    count = 0
    for item in url:
        symbol = item["symbol"]
        name = item["name"]
        momentum = item["avg_momentum"]
        newtuple = symbol, name, momentum
        lst.append(newtuple)
    #lst.sort(key=sort_mom, reverse=True)
    short_lst = lst[:20]
    best_list = "\n".join(str(el) for el in short_lst)
    best_20 = best_list.replace("(","").replace(")","").replace("'", "")
    return best_20


def get_div():
    """Get dividend stocks list"""
    url = requests.get(f"http://ivand200.pythonanywhere.com/divs/").json()
    lst = list()
    for item in url:
        symbol = item["symbol"]
        name = item["name"]
        div = item["div_p"]
        newtuple = symbol, name, div
        lst.append(newtuple)
    #lst.sort(key=sort_mom, reverse=True)
    short_lst = lst[:20]
    best_list = "\n".join(str(el) for el in short_lst)
    best_20 = best_list.replace("(","").replace(")","").replace("'", "")
    return best_20


def get_etf(etf):
    """Get Momentum_12_1 by etf"""
    url = requests.get(f"http://ivand200.pythonanywhere.com/etf/{etf}").json()
    name  = url["name"]
    mom = url["momentum_12_1"]
    ma = url["ma10"]
    return f"{name}, \nMomentum: {mom}, \nMA10: {ma}"


def get_etf_momentum():
    """Get momentum for ETF"""
    result = []
    url = requests.get(f"http://ivand200.pythonanywhere.com/etf/").json()
    for item in url:
        name = item["name"]
        symbol = item["symbol"]
        momentum = item["momentum_12_1"]
        ma10 = item["ma10"]
        newtuple = symbol, name, momentum, ma10
        result.append(newtuple)
    #result.sort(key=sort_mom, reverse=True)
    best_list = "\n".join(str(el) for el in result)
    best_20 = best_list.replace("(","").replace(")","").replace("'", "")
    return best_20


def add_article(text, username):
    """Post article"""
    url = "http://ivand200.pythonanywhere.com/notes/"
    payload = {
    "text": f"{text}",
    "user": f"{username}"
    }
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    return r.text

def last_article():
    """Show last 20 articles"""
    url = requests.get("http://ivand200.pythonanywhere.com/notes/").json()
    lst = list()
    for item in url:
        id = item["id"]
        text = item["text"]
        name = item["user"]
        newtuple = id, text, name
        lst.append(newtuple)
    last_list = "\n".join(str(el) for el in lst[:20])
    last_20 = last_list.replace("(","").replace(")","").replace("'", "")
    return last_20

def del_article(id):
    """Delete article by id"""
    url = f"http://ivand200.pythonanywhere.com/notes/{id}"
    headers = {'Content-type': 'application/json'}
    r = requests.delete(url, headers=headers)
    return r.text
