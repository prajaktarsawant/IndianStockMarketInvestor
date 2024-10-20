import yfinance as yf
import numpy as np
import pandas as pd

# Function to fetch stock data from yfinance
def get_stock_data(stock_symbol, start="2020-01-01", end=None):
    data = yf.download(stock_symbol, start=start, end=end, interval="1d")
    return data

# Function to implement the moving average crossover strategy
def moving_average_strategy(data, short_window=50, long_window=200):
    data['Short_MA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()
    
    # Generate buy/sell signals
    data['Signal'] = 0
    data['Signal'][short_window:] = np.where(data['Short_MA'][short_window:] > data['Long_MA'][short_window:], 1, 0)
    data['Position'] = data['Signal'].diff()  # Ensure this line is present
    
    return data
