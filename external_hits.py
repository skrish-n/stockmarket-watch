from datetime import datetime
from app.models import Stockdump
import requests



def get_stock_quote(symbol):
    print('#####Entering get_stock_quote#####')
    quoteUrl = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=' + symbol + '&apikey=' + app.config['ALPHAVANTAGE_KEY']
    r = requests.get(quoteUrl)

    if r.status_code == 200:
        stock_data = r.json()
        ticker_symbol = stock_data['Global Quote']['01. symbol']
        price_change = float(stock_data['Global Quote']['09. change'])
        percent_change = stock_data['Global Quote']['10. change percent']
        percent_change_converted = float(percent_change[:len(percent_change) - 1])
        price = float(stock_data['Global Quote']['05. price'])

        # Creating json structure:
        json_data = {
            'stockName': ticker_symbol,
            'lastPulledPrice': price,
            'priceChange': price_change,
            'percentChange': percent_change_converted
        }
        print('#####Exiting get_stock_quote success#####')
        return json_data
    print('#####Exiting get_stock_quote fail#####')
    return False


def get_stock_quote_new(symbol, is_new):
    from run import app
    print('#####Entering get_stock_quote() function#####')
    quote_url = "https://finnhub.io/api/v1/quote?symbol=" + symbol + "&token=" + app.config['FINNHUB_KEY']
    r = requests.get(quote_url)

    if r.status_code == 200:
        print('API Success')
        stock_data = r.json()
        ticker_symbol = symbol
        price_change = float(stock_data['c']) - float(stock_data['pc'])
        percent_change = (price_change / stock_data['pc']) * 100;
        current_price = float(stock_data['c'])
        current_time = datetime.now()
        print(current_time)
        # Creating json structure:
        new_stock=""
        if is_new is 1:
            # Creating document structure:

            new_stock = Stockdump(ticker=ticker_symbol,last_pulled_price=current_price,last_pulled_date=current_time,price_change=price_change,
                                  updated_at=current_time,created_at=current_time)
        else:
            new_stock = Stockdump(ticker=ticker_symbol, last_pulled_price=current_price, last_pulled_date=current_time,
                                  price_change=price_change,
                                  updated_at=current_time)
        print('#####Exiting get_stock_quote() success#####')
        return new_stock
    else:
        print('#####Exiting get_stock_quote() fail#####')
        return False


if __name__ == '__main__':
    print(get_stock_quote_new('ADBE'))
