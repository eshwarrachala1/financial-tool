# app/services/stock_service.py

import requests
from app.config import settings
from fastapi import HTTPException
import yfinance as yf
import pandas as pd
import ta



def get_stock_trend_data(symbol: str) -> dict:
    """
    Fetch real-time stock data from Alpha Vantage and calculate technical indicators
    """
     
    stockdata = {}
    indicators = calculate_indicators(symbol)
     
    return indicators


def get_stock_data(ticker, period="1y"):
    # Fetch data for the past year by default
    stock_data = yf.download(ticker, period=period)
    return stock_data

def calculate_indicators(ticker:str):
    
    data = get_stock_data(ticker)
    
    indicators = {}

    # P/E Ratio (use TTM, if available, or a placeholder)
    ticker_data = yf.Ticker(ticker)
    indicators['P/E Ratio'] = ticker_data.info.get('trailingPE', 'N/A')

    # P/B Ratio
    indicators['P/B Ratio'] = ticker_data.info.get('priceToBook', 'N/A')

    # Convert 'Close' column to 1D Series if necessary
    close_prices = data['Close'].squeeze()  # Ensures data is 1D

    # Relative Strength Index (RSI)
    data['RSI'] = ta.momentum.RSIIndicator(close=close_prices).rsi()
    indicators['RSI'] = data['RSI'].iloc[-1]  # Most recent value

    # 50-day and 200-day Moving Averages
    data['50_MA'] = close_prices.rolling(window=50).mean()
    data['200_MA'] = close_prices.rolling(window=200).mean()
    indicators['50-day MA'] = data['50_MA'].iloc[-1]
    indicators['200-day MA'] = data['200_MA'].iloc[-1]

    # Support and Resistance: Simple Check
    indicators['Support'] = data['Low'].min()
    indicators['Resistance'] = data['High'].max()

    # Bollinger Bands
    bollinger = ta.volatility.BollingerBands(close=close_prices)
    data['Upper Band'] = bollinger.bollinger_hband()
    data['Lower Band'] = bollinger.bollinger_lband()
    indicators['Upper Band'] = data['Upper Band'].iloc[-1]
    indicators['Lower Band'] = data['Lower Band'].iloc[-1]

    # MACD
    macd = ta.trend.MACD(close=close_prices)
    data['MACD'] = macd.macd()
    data['Signal Line'] = macd.macd_signal()
    indicators['MACD'] = data['MACD'].iloc[-1]
    indicators['Signal Line'] = data['Signal Line'].iloc[-1]

    # Earnings and Dividend Yield
    indicators['EPS (ttm)'] = ticker_data.info.get('trailingEps', 'N/A')
    indicators['Dividend Yield'] = ticker_data.info.get('dividendYield', 'N/A')

    return indicators