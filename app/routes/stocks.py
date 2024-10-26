# app/routes/stocks.py

from fastapi import APIRouter, HTTPException
from app.services import stock_service
from app.models.stock_model import RealTimeStockData, HistoricalStockData
import yfinance as yf
import pandas as pd
import ta

router = APIRouter()

@router.get("/{symbol}", response_model=RealTimeStockData)
def get_stock_data(symbol: str):
    """Fetch real-time stock data for a given symbol"""
    try:
        stock_data = stock_service.get_realtime_stock_data(symbol)
        return RealTimeStockData(**stock_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @router.get("/{symbol}/historical", response_model=HistoricalStockData) 
@router.get("/{symbol}/historical", response_model=HistoricalStockData)
def get_historical_stock_data(symbol: str, start_date: str, end_date: str):
    """
    Fetch historical stock data for a specific symbol between start_date and end_date.
    """
    try:
        historical_data = stock_service.get_historical_stock_data(symbol, start_date, end_date)
        return HistoricalStockData(symbol=symbol, data=historical_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.get("/trend/{symbol}", response_model=RealTimeStockData)
def get_stock_data(symbol: str):
    """Fetch real-time stock data for a given symbol"""
    try:
        stock_data = stock_service.get_stock_data(symbol)
        return RealTimeStockData(**stock_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
