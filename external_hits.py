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
