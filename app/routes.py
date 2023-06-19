from flask import render_template
from app import app
from app.models import Yesterday

import yfinance as yf
import plotly.graph_objs as plotly
import pandas as pd
import numpy as np
import sqlite3

global signal
signal = 1

class Portfolio:
    def __init__(self, name, ticker, amount, shares):
        self.name = name
        self.ticker = ticker
        self.amount = amount
        self.shares = shares
        self.value = None

def start():
    signal = 1
    return

def stop():
    signal = 0
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    for stock in df.itterows():
        cursor.execute('''UPDATE yesterday SET yesterday = stock["Value"] WHERE name = stock["Company"]''')
    conn.commit()
    conn.close()
    return

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    global df

    if signal == 1:
        stock_values = []
        stock_names = []
        stock_amount = []

        def returns(portfolio_list, price):
            for stock in portfolio_list:
                stock.value = (stock.shares) * price.loc[stock.name]
            return

        stocks = yf.download(tickers = ["ACCELYA.NS", "AFFLE.NS", "DEEPAKFERT.NS", "FEDERALBNK.NS", "UJJIVANSFB.NS", "ITC.NS", "TATASTEEL.NS", "HINDALCO.NS", "MPHASIS.NS", "AMARAJABAT.NS"], period="1d")
        mutual_funds_price = yf.download(tickers = ['0P0000K1D7.BO', '0P0000U9KG.BO'], period="1mo")['Adj Close'].iloc[-1]
        mutual_funds_price = mutual_funds_price.values
        mutual_funds_price = mutual_funds_price.tolist()
        price = stocks["Adj Close"].values
        columns = ["Accelya Solutions", "Affle", "Amara Raja Batteries", "Deepak Fertilizers", "Federal Bank", "Hindalco", "ITC", "Mphasis", "Tata Steel", "Ujjivan", "Aditya Birla Sun Life Medium Term (G)", "Axis Gold (G)"]
        price = price.tolist()
        price = price.pop(0)
        price_list = price + mutual_funds_price
        price = pd.DataFrame(columns, price + mutual_funds_price)
        
        portfolio_list = [Portfolio("Accelya Solutions", "ACCELYA.NS", 1378.39, 1), Portfolio("Affle", "AFFLE.NS", 1975.41, 2), Portfolio("Amara Raja Batteries", "AMARAJABAT.NS", 3100.65, 5),
                        Portfolio("Deepak Fertilizers", "DEEPAKFERT.NS", 5581.10, 10), Portfolio("Federal Bank", "FEDERALBNK.NS", 2533.48, 20), Portfolio("Hindalco", "HINDALCO.NS", 4709.48, 11),
                        Portfolio("ITC", "ITC.NS", 2262.48, 5), Portfolio("Mphasis", "MPHASIS.NS", 8094.28, 4), Portfolio("Tata Steel", "TATASTEEL.NS", 2064.92, 19), Portfolio("Ujjivan", "UJJIVANSFB.NS", 3046.28, 81),
                        Portfolio("Aditya Birla Sun Life Medium Term (G)", "0P0000K1D7.BO", 5999.70, 183.8), Portfolio("Axis Gold (G)", "0P0000XVTX.BO", 4999.75, 277.105)]

        price.reset_index(inplace = True)
        price.set_index([0], inplace = True)
        price.columns = ['Price']
        price.rename_axis('Company', inplace = True)

        returns(portfolio_list, price)

        for stock in portfolio_list:
            stock_names.append(stock.name)
            stock_values.append(stock.value.Price)
            stock_amount.append(stock.amount)
        
        df = pd.DataFrame(list(zip(stock_names, price_list, stock_values, stock_amount)), columns = ["Company", "Price", "Value", "Invested"])
        df["Return"] = df.apply(lambda x: 100 * (x["Value"] / x["Invested"] - 1), axis = 1)
        df['Return'] = df['Return'].astype(float)
        #df = pd.concat([df, df[['Value','Invested']].sum()], ignore_index = True)
        df = df.append(df[['Value','Invested']].sum(), ignore_index = True)
        df["Return"][df.shape[0] - 1] = round(100 * (df["Value"][df.shape[0] - 1] / df["Invested"][df.shape[0] - 1] - 1), 2)
        df["Return"] = df["Return"].apply(lambda x: round(x, 2))
        df["Value"] = df["Value"].apply(lambda x: round(x, 2))
        df["Company"][df.shape[0] - 1] = "Total"
        df["Yesterday"] = 0

        for index, stock in enumerate(Yesterday.query.all()):
            df["Yesterday"][index] = stock.yesterday
        
        df["Returns Today"] = df["Value"] - df["Yesterday"]
        df["Today Percentage"] = 100 * (df["Returns Today"] / df["Yesterday"])
    
    return render_template('home.html', title='Stocks', df = df, signal = signal)


