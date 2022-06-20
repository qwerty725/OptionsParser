import pycurl
import certifi
import requests
import json
from io import BytesIO
class Stock:
    def __init__(self, ticker, mark, premium, profitPercent, premiumPercentofProfit):
        self.ticker = ticker
        self.mark = mark
        self.premium = premium
        self.profitPercent = profitPercent
        self.premiumPercentofProfit = premiumPercentofProfit
if __name__ == "__main__":
    # Creating a buffer as the cURL is not allocating a buffer for the network response
    stockList = []
    url = "https://api.tdameritrade.com/v1/marketdata/chains?apikey=IXAAAISWNKMXP0ENJEEYPRWO400NJVED&symbol=AMD&contractType=CALL&strikeCount=2&fromDate=2022-06-18&toDate=2022-06-30"
    headers = "Authorization: "
    resp = requests.get(url)
    dict = json.loads(resp.content)
    currentPrice = dict['underlyingPrice']
    print("currentPrice: {}".format(currentPrice))
    volatility = dict['volatility']
    symbol = dict['symbol']
    #print(dict['callExpDateMap']['2022-06-24:5']['78.0'])
    for key, value in dict['callExpDateMap'].items():
        date = key
        print(date)
        for strike, data in value.items():
            numStrike = float(strike)
            if numStrike > currentPrice:
                bid = data[0]['bid']
                ask = data[0]['ask']
                mark = data[0]['mark']
                bidSize = data[0]['bidSize']
                askSize = data[0]['askSize']
                breakeven = numStrike + mark
                profit = breakeven - currentPrice
                profitPercent = profit/currentPrice * 100
                premiumPercentofProfit = mark/profit * 100
                print("strike: {}".format(numStrike))
                print("percent: {}".format(profitPercent))
                print("profit: {}".format(profit))
                print("premium: {}".format(mark))
                print("premium percent of profit: {}".format(premiumPercentofProfit))
    #for each in dict.items():
    #    print(each)
    #print(dict.items())
    #print(resp)