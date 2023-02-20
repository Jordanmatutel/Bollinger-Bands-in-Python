import time
import pandas as pd
import ccxt
import statistics
import matplotlib.pyplot as plt

#We establish the period of our study. The period will create more lists with the same
#amount of data.

period = 20
smas = [0] * period
upperBands = [0] * period
lowerBands = [0] * period


#Stablish the forever-loop to keep the script working.
#Every iteration will have his freeze time (60s this time), in order to not overload CCXT and the data
while True:

    #We create the function to calculate the SMA. The period needs to be equal to the amount of prices.
    def sma(prices, period):
        if len(prices) < period:
            return None
        else:
            return float(sum(prices[-period:])) / float(period)


    #We put the market and the broker database from where we want the data.
    #You can add your API as well to make one strategy.
    #We take the closing price in 1m dataframe to use it on our study.
    market = "BTC/USDT"
    exchange = ccxt.binance({"Public Key":"XXXXX", "Secret Key":"XXXXX"})
    prices = exchange.fetch_ohlcv(symbol=market, timeframe="1m", limit=period)
    closing_prices = [candle[4] for candle in prices]
    closing = pd.DataFrame(closing_prices)
    closing = closing.astype(float)

    #Now we make one list with the lenght of our period selection to fit it on our chart.

    date = [None] * period
    for i in range(0, period):
        date[i] = i


    #We need to calculate the SMA with the periods we choose in order to
    #put it as the middle band. Every SMA will be saved on our list smas.
    c = sma(closing_prices, period)
    smas[1:] = smas[:-1]
    smas[0] = c

    #Now we calculate the standar deviation in order to calculate the bollinger bands.
    #We use the statistics library to calculate the bands.
    #After that, we save the data in our variables.
    stdev = statistics.stdev(closing_prices)
    upperBand = sma(closing_prices, period) + (2 * stdev)
    lowerBand = sma(closing_prices, period) - (2 * stdev)

    upperBands[1:] = upperBands[:-1]
    upperBands[0] = upperBand

    lowerBands[1:] = lowerBands[:-1]
    lowerBands[0] = lowerBand

    #Now that we got the dataframes for the prices, the SMA and the bands we can now
    #plot the graph showing the bands of bollinger.

    if smas[-1] > 0:
        chart = plt.plot(date, closing, color = "green", label = f"Last {period} prices")
        plt.plot(date, smas, color = "orange", label = f"SMA of {period} periods")
        plt.plot(date, upperBands, color = "blue", label = f"Upper Band of {period} period")
        plt.plot(date, lowerBands, color = "blue", label = f"Lower Band of {period} period")
        plt.xlabel('Dates')
        plt.ylabel('Prices')
        plt.title('Bollinger Bands using Python')
        plt.show()

    time.sleep(60)