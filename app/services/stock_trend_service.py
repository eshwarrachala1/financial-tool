# app/services/stock_service.py

import requests
from app.config import settings
from datetime import datetime
from fastapi import HTTPException




def get_stock_trend_data(symbol: str):
    """Fetch real-time stock data from Alpha Vantage and map it to our Pydantic model"""
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": settings.ALPHA_VANTAGE_API_KEY_FREE
    }
    response = requests.get(settings.STOCK_BASE_URL, params=params)
    data = response.json()

    # Check if the data contains the 'Global Quote' key
    if "Global Quote" in data:
        raw_data = data["Global Quote"]

        # Map the incoming keys to the expected fields
        stock_data = {
            "symbol": raw_data.get("01. symbol"),
            "open": float(raw_data.get("02. open")),
            "high": float(raw_data.get("03. high")),
            "low": float(raw_data.get("04. low")),
            "price": float(raw_data.get("05. price")),
            "volume": int(raw_data.get("06. volume")),
            "latest_trading_day": raw_data.get("07. latest trading day"),
            "previous_close": float(raw_data.get("08. previous close")),
            "change": float(raw_data.get("09. change")),
            "change_percent": raw_data.get("10. change percent")
        }
        return stock_data
    else:
        raise ValueError("Error fetching real-time data for the stock symbol.")