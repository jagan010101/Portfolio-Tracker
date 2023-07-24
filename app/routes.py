from flask import render_template
from app import app
from app.models import Yesterday

import yfinance as yf
import pandas as pd
import sqlite3

def update():
    app.app_context().push()
    conn = sqlite3.connect('instance/db.sqlite3')
    cursor = conn.cursor()
    for index in range(len(df3)):
        update = "UPDATE yesterday SET yesterday = ? WHERE name = ?"
        values = (df3.loc[index, 'Value'], df3.loc[index, 'Company'])
        cursor.execute(update, values)
    conn.commit()
    conn.close()
    return

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():

    df = yf.download(tickers = ["ACCELYA.NS", "AFFLE.NS", "DEEPAKFERT.NS", "FEDERALBNK.NS", "UJJIVANSFB.NS", "ITC.NS", "TATASTEEL.NS", "HINDALCO.NS", "MPHASIS.NS", "SBIN.NS", "AMARAJABAT.NS"], period="1d")['Adj Close']
    df.columns = ["Accelya Solutions", "Affle", "Amara Raja Batteries", "Deepak Fertilizers", "Federal Bank", "Hindalco", "ITC", "Mphasis", "State Bank of India", "Tata Steel", "Ujjivan"]
    df = df.transpose()
    df.reset_index(inplace = True)
    df.columns = ['Company', 'Price']

    mf1 = yf.download(tickers = '0P0000K1D7.BO', period="1mo")['Adj Close'].iloc[-1]
    mf2 = yf.download(tickers = '0P0000U9KG.BO', period="1mo")['Adj Close'].iloc[-1] 

    df.loc[len(df)] = ['Aditya Birla Sun Life Medium Term (G)', mf1]
    df.loc[len(df)] = ['Axis Gold (G)', mf2]
    df['Invested'] = [1378.39, 1975.41, 3100.65, 5581.1, 2533.48, 4709.48, 2262.48, 4402.58, 2857.5, 2064.92, 3046.28, 5999.70, 4999.75]
    df['Units'] = [1, 2, 5, 10, 20, 11, 5, 2, 5, 19, 81, 183.8, 277.105]
    df['Value'] = df['Price'] * df['Units']
    df['Returns'] = df["Value"] - df["Invested"]
    df_sum = pd.DataFrame({'Company': ['Total'], 'Value': [df['Value'].sum()], 'Invested': [df['Invested'].sum()], 'Returns': [df['Value'].sum() - df['Invested'].sum()]})
    df = pd.concat([df, df_sum], ignore_index = True)

    df_db = pd.DataFrame({'Company': [0] * len(df), 'Yesterday': [0] * len(df)})

    for index, stock in enumerate(Yesterday.query.all()):
        df_db.loc[index, 'Yesterday'] = stock.yesterday
        df_db.loc[index, 'Company'] = stock.name

    df = pd.merge(df, df_db, how='inner')
    
    df['Gain Today'] = df['Value'] - df['Yesterday']
    df['Gain Today %'] = 100 * df['Gain Today']/ df['Invested']

    global df3
    df3 = df

    return render_template('home.html', title = 'Stocks', df = df)