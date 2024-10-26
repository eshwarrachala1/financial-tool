# app/services/stock_service.py

import requests
from app.config import settings
from datetime import datetime
from fastapi import HTTPException




def get_realtime_stock_data(symbol: str):
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
    
def get_stock_data(symbol: str):
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
       
def get_historical_stock_data(symbol: str, start_date: str, end_date: str):
    """
    Fetch historical stock data for the given symbol between start_date and end_date.
    """
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "apikey": settings.ALPHA_VANTAGE_API_KEY_FREE,
        "outputsize": "full",  # Fetch the full history of the stock
    }

    try:
        response = requests.get(settings.STOCK_BASE_URL, params=params)
        data = response.json()

        # Check if there are any API errors like rate limiting or invalid symbols
        if "Note" in data:
            raise ValueError("API rate limit exceeded. Please try again later.")
        elif "Error Message" in data:
            raise ValueError(f"Invalid API call: {data['Error Message']}")
        elif "Information" in data:
            raise ValueError(f"Information: {data['Information']}")

        # Ensure that the "Time Series (Daily)" key exists in the response
        if "Time Series (Daily)" not in data:
            raise KeyError(f"'Time Series (Daily)' not found in response: {data}")

        time_series = data["Time Series (Daily)"]

        # Filter the data based on the date range
        filtered_data = {}
        for date, daily_data in time_series.items():
            if start_date <= date <= end_date:
                filtered_data[date] = {
                    "open": float(daily_data.get("1. open", 0.0)),
                    "high": float(daily_data.get("2. high", 0.0)),
                    "low": float(daily_data.get("3. low", 0.0)),
                    "close": float(daily_data.get("4. close", 0.0)),
                    "adjusted_close": float(daily_data.get("5. adjusted close", 0.0)),
                    "volume": int(daily_data.get("6. volume", 0)),
                }

        # If no data is found in the specified range, raise an error
        if not filtered_data:
            raise ValueError("No data available for the specified date range.")

        return filtered_data

    except requests.exceptions.RequestException as e:
        # Log request exceptions (network issues, timeouts, etc.)
        raise HTTPException(status_code=500, detail=f"Error fetching data from Alpha Vantage: {str(e)}")
    except KeyError as e:
        # Handle missing keys in the response
        raise HTTPException(status_code=500, detail=f"Key error: {str(e)}")
    except ValueError as e:
        # Handle value errors like API rate limits or missing data
        raise HTTPException(status_code=500, detail=f"Value error: {str(e)}")
    except Exception as e:
        # Catch all other exceptions and log them
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")