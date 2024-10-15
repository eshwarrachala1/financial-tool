# app/services/stock_service.py

import requests
import os
from app.config import settings

BASE_URL = "https://www.alphavantage.co/query"

def get_realtime_stock_data(symbol: str):
    """Fetch real-time stock data from Alpha Vantage"""
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": settings.ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if "Global Quote" in data:
        return data["Global Quote"]
    else:
        raise ValueError("Error fetching real-time data for the stock symbol.")

def get_historical_stock_data(symbol: str, start_date: str, end_date: str):
    """Fetch historical stock data from Alpha Vantage"""
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "outputsize": "full",
        "apikey": settings.ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    # Filter data by start_date and end_date
    if "Time Series (Daily)" in data:
        time_series = data["Time Series (Daily)"]
        filtered_data = {date: value for date, value in time_series.items() if start_date <= date <= end_date}
        return filtered_data
    else:
        raise ValueError("Error fetching historical data for the stock symbol.")
