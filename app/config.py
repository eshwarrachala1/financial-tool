# app/config.py


from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    ALPHA_VANTAGE_API_KEY: str = os.getenv("ALPHA_VANTAGE_API_KEY", "your_default_api_key_here")
    FRED_API_KEY: str = os.getenv("FRED_API_KEY", "24d1429f341bc77ad7c75056652328d8")

settings = Settings()

