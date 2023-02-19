import time
import pandas as pd
import ccxt
import math
import matplotlib


#Stablish the forever-loop to keep the script working
while True:

    #We use this in case we want to manage the quantity of data we use.
    def deleteData(Data, period):
        if Data[period]:
            del Data[-1]
        return Data

    #We use this in order to calculate the SMA.
    def sma(prices, period):
        x = sum(prices[-period:]) / period
        return x


    #We put the market and the broker database from where we want the data
    market = "BTC/USDT"

    exchange = ccxt.binance({"Public Key":"XXXXX", "Secret Key":"XXXXX"})

    #We input the last 20 prices using the data from the CCXT exchange. In this case
    #We are using the prices from Binance. We also input the period we want to work with.

    #currentPrice = exchange.fetch_ohlcv(market, timeframe='1m')
    period = 20
    prices = exchange.fetch_trades(symbol='BTC/USDT', limit=period)
    date = [None] * period

    for i in range(1, period):
        date[i] = i


    # We stablish the current SMA using the period and we add to the database
    smas = []
    smas.__add__(sma(prices, period))

    deleteData(prices,period)
    deleteData(smas, period)

    #Now that we got the current price and the SMA, we start calculating the upper band and the lower band
    stdev = math.sqrt(prices)
    upperBand = sma(prices, period) + (2 * stdev)
    lowerBand = sma(prices, period) - (2 * stdev)

    upperBands = []
    upperBands.__add__(upperBand)
    deleteData(upperBands, period)

    lowerBands = []
    lowerBands.__add__(lowerBand)
    deleteData(lowerBands, period)


    result = {"Dates":[date], "Prices":[prices],"SMA":[smas],
              "Upper Band":[upperBands], "Lower Band":[lowerBands]}

    df = pd.Dataframe (result)

    #Now that we got the dataframes for the prices, the SMA and the bands we can now
    #plot the graph showing the bands of bollinger

    chart = df.plot(x = "Dates", y = "Prices", label = f"Last {period} Prices")
    df.plot(x = "Dates", y = "SMA", label = f"The {period} SMA", ax = chart)
    df.plot(x = "Dates", y = "Upper Bands", label = f"The {period} Upper Band", ax = chart)
    df.plot(x = "Dates", y = "Lower Bands", label = f"The {period} Lower Band", ax = chart)

    df.xlabel('Dates')
    df.ylabel('Prices')
    df.title('Bollinger Bands using Python')
    df.show()

    time.sleep(60)