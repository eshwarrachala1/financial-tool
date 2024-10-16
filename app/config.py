# app/config.py


from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    ALPHA_VANTAGE_API_KEY: str = os.getenv("ALPHA_VANTAGE_API_KEY", "MC4H76494O522TUH")
    FRED_API_KEY: str = os.getenv("FRED_API_KEY", "24d1429f341bc77ad7c75056652328d8")
    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "3beb7c68474c420eabef776c94fc7618") 

settings = Settings()

