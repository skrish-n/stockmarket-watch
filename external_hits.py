from datetime import datetime

import requests
from run import alphavantage_api_key


def get_stock_quote(symbol):
    print('#####Entering get_stock_quote#####')
    quoteUrl = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=' + symbol + '&apikey=' + alphavantage_api_key
    r = requests.get(quoteUrl)

    if r.status_code == 200:
        stock_data = r.json()
        ticker_symbol = stock_data['Global Quote']['01. symbol']
        price_change = float(stock_data['Global Quote']['09. change'])
        percent_change = stock_data['Global Quote']['10. change percent']
        percent_change_converted = float(percent_change[:len(percent_change)-1])
        price = float(stock_data['Global Quote']['05. price'])

        #Creating json structure:
        json_data = {
            'stockName' : ticker_symbol,
            'lastPulledPrice' : price,
            'priceChange': price_change,
            'percentChange': percent_change_converted
        }
        print('#####Exiting get_stock_quote success#####')
        return json_data
    print('#####Exiting get_stock_quote fail#####')
    return False

def get_stock_quote_new(symbol):
    print('#####Entering get_stock_quote#####')
    quoteURL = "https://finnhub.io/api/v1/quote?symbol=" + symbol + "&token=bt8b6hv48v6srkbhggl0"
    r = requests.get(quoteURL)

    if r.status_code == 200:
        stock_data = r.json()
        ticker_symbol = symbol
        price_change = float(stock_data['c']) - float(stock_data['pc'])
        percent_change = (price_change/stock_data['pc'])*100;
        current_price = float(stock_data['c'])
        current_time = datetime.now()
        print(current_time)
        #Creating json structure:
        json_data = {
            'stockName' : ticker_symbol,
            'lastPulledPrice' : current_price,
            'priceChange': price_change,
            'percentChange': percent_change,
            'lastModified': current_time
        }
        print('#####Exiting get_stock_quote success#####')
        return json_data
    print('#####Exiting get_stock_quote fail#####')
    return False



if __name__ == '__main__':
    print(get_stock_quote_new('ADBE'))
