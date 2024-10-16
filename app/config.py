# app/config.py


from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    ALPHA_VANTAGE_API_KEY: str = os.getenv("ALPHA_VANTAGE_API_KEY", "MC4H76494O522TUH")
    ALPHA_VANTAGE_API_KEY_FREE: str = os.getenv("ALPHA_VANTAGE_API_KEY_FREE", "B9MY23DBA79Y6GO6")    
    FRED_API_KEY: str = os.getenv("FRED_API_KEY", "24d1429f341bc77ad7c75056652328d8")
    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "3beb7c68474c420eabef776c94fc7618") 
    
    MACRO_BASE_URL: str = os.getenv("MACRO_BASE_URL", "https://api.stlouisfed.org/fred/series/observations")
    NEWS_API_BASE_URL: str = os.getenv("NEWS_API_BASE_URL", "https://newsapi.org/v2/everything")
    STOCK_BASE_URL: str = os.getenv("STOCK_BASE_URL", "https://www.alphavantage.co/query")

settings = Settings()

