# app/routes/sentiment.py

from fastapi import APIRouter, HTTPException
from app.services import sentiment_service

router = APIRouter()

@router.get("/{symbol}")
async def get_sentiment_analysis(symbol: str):
    """Fetch sentiment analysis for a specific stock symbol"""
    try:
        sentiment_data = sentiment_service.get_stock_sentiment(symbol)
        return sentiment_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))