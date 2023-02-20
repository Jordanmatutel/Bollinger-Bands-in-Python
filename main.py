import time
import pandas as pd
import ccxt
import statistics
import matplotlib.pyplot as plt

period = 20
smas = [0] * period
upperBands = [0] * period
lowerBands = [0] * period


#Stablish the forever-loop to keep the script working
while True:

    pauseTime = 60

    #We use this in order to calculate the SMA.
    def sma(prices, period):
        if len(prices) < period:
            return None
        else:
            return float(sum(prices[-period:])) / float(period)


    #We put the market and the broker database from where we want the data
    market = "BTC/USDT"
    exchange = ccxt.binance({"Public Key":"XXXXX", "Secret Key":"XXXXX"})
    prices = exchange.fetch_ohlcv(symbol=market, timeframe="1m", limit=period)
    closing_prices = [candle[4] for candle in prices]
    closing = pd.DataFrame(closing_prices)
    closing = closing.astype(float)

    #We input the last 20 prices using the data from the CCXT exchange. In this case
    #We are using the prices from Binance. We also input the period we want to work with.

    date = [None] * period
    for i in range(0, period):
        date[i] = i

    dates = pd.DataFrame(date)
    dates = dates.astype(int)
    # We stablish the current SMA using the period and we add to the database

    c = sma(closing_prices, period)
    smas[1:] = smas[:-1]
    smas[0] = c

    #Now that we got the current price and the SMA, we start calculating the upper band and the lower band
    stdev = statistics.stdev(closing_prices)
    upperBand = sma(closing_prices, period) + (2 * stdev)
    lowerBand = sma(closing_prices, period) - (2 * stdev)

    upperBands[1:] = upperBands[:-1]
    upperBands[0] = upperBand

    lowerBands[1:] = lowerBands[:-1]
    lowerBands[0] = lowerBand

    #Now that we got the dataframes for the prices, the SMA and the bands we can now
    #plot the graph showing the bands of bollinger

    chart = plt.plot(date, closing)
    plt.plot(date, smas)
    plt.plot(date, upperBands)
    plt.plot(date, lowerBands)
    plt.xlabel('Dates')
    plt.ylabel('Prices')
    plt.title('Bollinger Bands using Python')
    plt.show()

    print(smas)
    print(smas.__len__())
    time.sleep(1)