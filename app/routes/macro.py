# app/routes/macro.py

from fastapi import APIRouter, HTTPException
from app.services import macro_service

router = APIRouter()

@router.get("/gdp/{country}")
def get_gdp_data(country: str, start_date: str, end_date: str):
    """Fetch GDP data for a specific country"""
    try:
        gdp_data = macro_service.get_gdp_data(country, start_date, end_date)
        return gdp_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/gdp")
def get_gdp_data(country: str, start_date: str, end_date: str):
    """Fetch GDP data for a specific country"""
    try:
        gdp_data = macro_service.get_gdp_data(country, start_date, end_date)
        return gdp_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/inflation")
def get_inflation_data(country: str, start_date: str, end_date: str):
    """Fetch inflation data for a specific country"""
    try:
        inflation_data = macro_service.get_inflation_data(country, start_date, end_date)
        return inflation_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
