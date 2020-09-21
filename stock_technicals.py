#!/usr/bin/env python
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)

import requests, external_hits
from run import dbConnection, db_stock_dump


def getStockQuote(symbol):
    quoteUrl = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=" + symbol + "&apikey=TPTE05D3FRVY8IR6"
    r = requests.get(quoteUrl)

    if (r.status_code != 200):
        return None
    data = r.json()
    price = float(data['Global Quote']['05. price'])
    print(data['Global Quote']['05. price'])
    return price

def getStockQuoteNew(symbol):
    quoteURL = "https://finnhub.io/api/v1/quote?symbol=" + symbol + "&token=bt8b6hv48v6srkbhggl0"

    res = requests.get(quoteURL)
    if (res.status_code !=200):
        return None

    data = res.json()
    current_price = float(data['c'])
    print(current_price)
    return current_price


def main():
    # get the stock quote of company:
    symbols = ["ADBE", "HAVELLS.NS", "CUB.NS", "NELCO.NS"]
    alertPrice = [350, 610, 215, 230]
    for i in range(len(symbols)):
        price = getStockQuote(symbols[i])

        if price > alertPrice[i]:
            print("My stock is above my safe price. Exiting now..")
        else:
            print("Stock is below safe price. Alert!")
            # Try to send email
            message = " The " + symbols[i] + " stock price:" + str(price)
            sendEmail(message)

            # Main Logic

    quit()


@jwt_required
def add_user_stock_details(json_data, user_name):
    print('#####Entering add_user_stock_details####')
    fetch_result = dbConnection.find_one({'username': user_name, 'stockDetails.ticker': json_data['ticker']})
    if fetch_result is None:
        try:
            dbConnection.update({'username': user_name}, {'$push': {'stockDetails': json_data}})
        except:
            print('#####Exiting add_user_stock_details fail#####')
            return False
    else:
        print('#####Exiting add_user_stock_details success without updates#####')
        return 0
    print('#####Exiting add_user_stock_details success with updates#####')
    return 1


def add_to_stock_dump(json_data):
    print('#####Entering add_to_stock_dump####')
    ticker_symbol = json_data['ticker']
    fetch_stock_result = db_stock_dump.find_one({'stockName': ticker_symbol})
    if fetch_stock_result is None:
        try:
            json_db_stock_dump = external_hits.get_stock_quote_new(ticker_symbol)
            db_stock_dump.insert_one(json_db_stock_dump)
        except:
            print('#####Exiting add_to_stock_dump fail1#####')
            return False
    print('#####Exiting add_to_stock_dump success#####')
    return True
