# app/models/stock_model.py

from pydantic import BaseModel, Field
from typing import List, Dict

class RealTimeStockData(BaseModel):
    symbol: str = Field(..., example="AAPL")
    open: float = Field(..., example=135.67)
    high: float = Field(..., example=137.25)
    low: float = Field(..., example=133.12)
    price: float = Field(..., example=136.21)
    volume: int = Field(..., example=98348392)
    latest_trading_day: str = Field(..., example="2023-10-13")
    previous_close: float = Field(..., example=134.87)
    change: float = Field(..., example=1.34)
    change_percent: str = Field(..., example="0.99%")

    class Config:
        schema_extra = {
            "example": {
                "symbol": "AAPL",
                "open": 135.67,
                "high": 137.25,
                "low": 133.12,
                "price": 136.21,
                "volume": 98348392,
                "latest_trading_day": "2023-10-13",
                "previous_close": 134.87,
                "change": 1.34,
                "change_percent": "0.99%"
            }
        }


class HistoricalStockData(BaseModel):
    symbol: str = Field(..., example="AAPL")
    data: Dict[str, Dict[str, float]] = Field(
        ...,
        example={
            "2023-10-10": {
                "open": 135.5,
                "high": 137.0,
                "low": 134.5,
                "close": 136.0,
                "adjusted_close": 136.0,
                "volume": 80000000
            },
            "2023-10-09": {
                "open": 134.0,
                "high": 136.0,
                "low": 133.0,
                "close": 135.0,
                "adjusted_close": 135.0,
                "volume": 75000000
            }
        }
    )

    class Config:
        schema_extra = {
            "example": {
                "symbol": "AAPL",
                "data": {
                    "2023-10-10": {
                        "open": 135.5,
                        "high": 137.0,
                        "low": 134.5,
                        "close": 136.0,
                        "adjusted_close": 136.0,
                        "volume": 80000000
                    },
                    "2023-10-09": {
                        "open": 134.0,
                        "high": 136.0,
                        "low": 133.0,
                        "close": 135.0,
                        "adjusted_close": 135.0,
                        "volume": 75000000
                    }
                }
            }
        }
