import urllib.request, urllib.parse, urllib.error
from datetime import datetime, timedelta
import json
import csv
import yfinance as yf
import yahoo_fin.stock_info as si
from yahoo_fin.stock_info import get_data, tickers_sp500, tickers_nasdaq, tickers_other, get_quote_table
import pandas as pd
import numpy as np
import requests
import re



# Define previous month
now = datetime.now()
lastmonth = now - timedelta(weeks=5)
endoflastmonth = lastmonth.replace(day=28)
month_ago = endoflastmonth.strftime("%Y-%m-%d")
start_ = now - timedelta(weeks=120)
start_time = start_.strftime("%Y-%m-%d")



def drawdown(series: pd.Series):
    wealth_index = 1000 * (1 + series.pct_change()).cumprod()
    previous_peaks = wealth_index.cummax()
    drawdowns = (wealth_index - previous_peaks) / previous_peaks
    return drawdowns

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


def test(share, ma):
    ticker = yf.Ticker(share)
    ticker = ticker.history(start="2001-01-01", end=month_ago, interval="1mo")
    ticker = ticker[ticker["Close"].notna()]
    profit = round(ma10(ticker, ma), 2)
    max_drawdown = round(drawdown(profit).min(), 2)
    return f"Max drawdown: {max_drawdown}\nProfit: {profit[-2]}"

data = {}
data["ma"] = 10
data["ticker"] = "MMM"
print(test(data["ticker"], data["ma"]))

"""
x =
url = "http://127.0.0.1:8000/articles/"
payload = {"link": f"{x}"}

r = requests.post(url, data=json.dumps(payload))
print(r.text)
"""
"""
x = "vbrt43"
payload = {"link": f"{x}"}
r = requests.post("http://127.0.0.1:8000/articles/", data=payload)
print(r.text)
"""
"""
url = "http://127.0.0.1:8000/articles/"
payload = {'link': f'{x}'}
headers = {"accept": "application/json", "Content-Type": "application/json"}
response = requests.request("POST", url, data=payload, headers=headers)
print(response.text)
print(payload)
"""
