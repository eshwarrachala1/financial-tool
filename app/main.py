# app/main.py

from fastapi import FastAPI
from app.routes import stocks, macro, sentiment

app = FastAPI(
    title="Financial Market API",
    description="API for fetching macro and microeconomic data for stocks",
    version="1.0.0"
)

# Register routes for stocks, macroeconomics, and sentiment analysis
app.include_router(stocks.router, prefix="/api/stocks")
app.include_router(macro.router, prefix="/api/macro")
app.include_router(sentiment.router, prefix="/api/sentiment")

@app.get("/")
def root():
    return {"message": "Welcome to the Financial Market API"}
