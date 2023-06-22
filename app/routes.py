from flask import render_template
from app import app, db
from app.models import Yesterday

import yfinance as yf
import pandas as pd
import numpy as np
import sqlite3

global signal
signal = 1

def start():
    signal = 1
    return

def stop():
    signal = 0
    app.app_context().push()
    conn = sqlite3.connect('instance/db.sqlite3')
    cursor = conn.cursor()
    for index in range(len(df2)):
        update = "UPDATE yesterday SET yesterday = ? WHERE name = ?"
        values = (df2.loc[index, 'Value'], df2.loc[index, 'Company'])
        cursor.execute(update, values)
    conn.commit()
    conn.close()
    return

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    global df2
    df = yf.download(tickers = ["ACCELYA.NS", "AFFLE.NS", "DEEPAKFERT.NS", "FEDERALBNK.NS", "UJJIVANSFB.NS", "ITC.NS", "TATASTEEL.NS", "HINDALCO.NS", "MPHASIS.NS", "AMARAJABAT.NS"], period="1d")['Adj Close']
    df.columns = ["Accelya Solutions", "Affle", "Amara Raja Batteries", "Deepak Fertilizers", "Federal Bank", "Hindalco", "ITC", "Mphasis", "Tata Steel", "Ujjivan"]
    df = df.transpose()
    df.reset_index(inplace = True)
    df.columns = ['Company', 'Price']
    mf = yf.download(tickers = ['0P0000K1D7.BO', '0P0000U9KG.BO'], period="1mo")['Adj Close'].iloc[-1]
    mf.index = ['Aditya Birla Sun Life Medium Term (G)', 'Axis Gold Fund (G)']
    df1 = pd.DataFrame({"Company": mf.index, "Price": mf.values})
    df2 = pd.concat([df,df1], ignore_index = True)
    df2['Invested'] = [1378.39, 1975.41, 3100.65, 5581.1, 2533.48, 4709.48, 2262.48, 8094.28, 2064.92, 3046.28, 5999.70, 4999.75]
    df2['Units'] = [1, 2, 5, 10, 20, 11, 5, 4, 19, 81, 183.8, 277.105]
    df2['Value'] = df2['Price'] * df2['Units']
    df2['Returns'] = df2["Value"] - df2["Invested"]
    df_sum = pd.DataFrame({'Company': ['Total'], 'Value': [df2['Value'].sum()], 'Invested': [df2['Invested'].sum()], 'Returns': [df2['Value'].sum() - df2['Invested'].sum()]})
    df2 = pd.concat([df2, df_sum], ignore_index = True)

    for index, stock in enumerate(Yesterday.query.all()):
        df2.loc[index, 'Yesterday'] = stock.yesterday

    df2['Gain Today'] = df2['Value'] - df2['Yesterday']
    df2['Gain Today %'] = 100 * df2['Gain Today']/ df2['Invested']
    
    return render_template('home.html', title = 'Stocks', df = df2, signal = signal)