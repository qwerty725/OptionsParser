import pycurl
import certifi
import requests
import json
import csv
import time
import datetime
class Stock:
    def __init__(self, ticker, mark, profitPercent, premiumPercentofProfit, volatility, currentPrice):
        self.ticker = ticker
        self.mark = mark
        self.profitPercent = profitPercent
        self.premiumPercentofProfit = premiumPercentofProfit
        self.volatility = volatility
        self.currentPrice = currentPrice
if __name__ == "__main__":
    today = datetime.date.today()
    saturday = today + datetime.timedelta( (5-today.weekday()) % 7 )
    print(saturday)
    # Creating a buffer as the cURL is not allocating a buffer for the network response
    stockList = []
    f = open("spy500.csv",'r')
    reader = csv.reader(f,delimiter=',')
    headers = "Authorization: "
    #default to AMD just bc
    url = "https://api.tdameritrade.com/v1/marketdata/chains?apikey=IXAAAISWNKMXP0ENJEEYPRWO400NJVED&symbol=PPG&contractType=CALL&strikeCount=2&fromDate=2022-06-18&toDate=2022-06-30"
    resp = requests.get(url)
    dict = json.loads(resp.content)
    print(dict)
    timer = time.time()
    requestsInMin = 0
    for line in reader:
        try:
            url = "https://api.tdameritrade.com/v1/marketdata/chains?apikey=IXAAAISWNKMXP0ENJEEYPRWO400NJVED&symbol=" \
                + line[0] + "&contractType=CALL&strikeCount=2&fromDate=2022-06-18&toDate=2022-06-30"
            #print(line[0])
            if requestsInMin >= 120:
                time.sleep(61 - (time.time() - timer))
                timer = time.time()
                requestsInMin = 0
            resp = requests.get(url)
            requestsInMin += 1
            dict = json.loads(resp.content)
            currentPrice = dict['underlyingPrice']
            #print("currentPrice: {}".format(currentPrice))
            volatility = dict['volatility']
            symbol = dict['symbol']
            #print(dict['callExpDateMap']['2022-06-24:5']['78.0'])
            for key, value in dict['callExpDateMap'].items():
                date = key
                #print(date)
                for strike, data in value.items():
                    numStrike = float(strike)
                    #print("strike : {} price: {}".format(numStrike, currentPrice))
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
                        stockList.append(Stock(symbol, mark, profitPercent, premiumPercentofProfit, volatility, currentPrice))
                        """ print("strike: {}".format(numStrike))
                        print("percent: {}".format(profitPercent))
                        print("profit: {}".format(profit))
                        print("premium: {}".format(mark))
                        print("premium percent of profit: {}".format(premiumPercentofProfit)) """
        except Exception as e:
            print(e)
    stockList.sort(key=lambda x: x.profitPercent, reverse=True)
    for i in range(15):
        print(stockList[i].ticker + "; price - " + str(stockList[i].currentPrice) + "; profit percent - " + str(stockList[i].profitPercent) + "; mark - " + str(stockList[i].mark))
    print(len(stockList))
    #for each in dict.items():
    #    print(each)
    #print(dict.items())
    #print(resp)