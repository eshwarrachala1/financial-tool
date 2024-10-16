# app/services/macro_service.py

import requests
from app.config import settings

# Base URL for the FRED API
FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

def get_gdp_data(country: str, start_date: str, end_date: str):
    """Fetch GDP data for a specific country between start_date and end_date"""
    # FRED uses specific series IDs for different economic indicators.
    # For example, in the U.S., the GDP series ID is "GDP".
    series_id = get_gdp_series_id(country)

    if not series_id:
        raise ValueError("GDP data not available for the specified country.")

    params = {
        "series_id": series_id,
        "api_key": settings.FRED_API_KEY,
        "file_type": "json",
        "observation_start": start_date,
        "observation_end": end_date,
    }

    response = requests.get(FRED_BASE_URL, params=params)
    data = response.json()

    if "observations" in data:
        return data["observations"]
    else:
        raise ValueError("Error fetching GDP data from FRED.")


def get_inflation_data(country: str, start_date: str, end_date: str):
    """Fetch inflation data (CPI) for a specific country between start_date and end_date"""
    # FRED uses different series IDs for CPI (inflation rate)
    # For example, "CPIAUCSL" is the Consumer Price Index for All Urban Consumers in the U.S.
    series_id = get_inflation_series_id(country)

    if not series_id:
        raise ValueError("Inflation data not available for the specified country.")

    params = {
        "series_id": series_id,
        "api_key": settings.FRED_API_KEY,
        "file_type": "json",
        "observation_start": start_date,
        "observation_end": end_date,
    }

    response = requests.get(FRED_BASE_URL, params=params)
    data = response.json()

    if "observations" in data:
        return data["observations"]
    else:
        raise ValueError("Error fetching inflation data from FRED.")


def get_gdp_series_id(country: str):
    """Map the country to its respective FRED series ID for GDP"""
    # In this example, we only handle the U.S. GDP, but you can add mappings for other countries
    gdp_series = {
        "US": "GDP",  # U.S. Gross Domestic Product
        # Add more mappings for other countries here
    }
    return gdp_series.get(country.upper())


def get_inflation_series_id(country: str):
    """Map the country to its respective FRED series ID for CPI (inflation)"""
    # In this example, we handle the U.S. inflation rate, but you can expand this.
    inflation_series = {
        "US": "CPIAUCSL",  # U.S. Consumer Price Index for All Urban Consumers
        # Add more mappings for other countries here
    }
    return inflation_series.get(country.upper())
