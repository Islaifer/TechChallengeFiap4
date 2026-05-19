from datetime import datetime, timedelta
from app.core.config import settings
from app.repository.redis_repository import RedisRepository
from app.dtos.historic_price import HistoricPrice
from app.service.predict_service import PredictService
from app.core.neural_network.model import get_neural_network, get_x_scaler, get_y_scaler
from typing import Any
import yfinance as yf
import pandas as pd

redis_repository = None
predict_service = None

async def init():
    global redis_repository
    global predict_service
    redis_repository = RedisRepository()

    model = get_neural_network()
    x_scaler = get_x_scaler()
    y_scaler = get_y_scaler()
    predict_service = PredictService(model, redis_repository, x_scaler, y_scaler)

    await get_disney_asset()

def get_predict_service():
    global predict_service
    return predict_service

async def get_disney_asset():
    global redis_repository
    
    if not settings.USE_REDIS:
        return

    if await redis_repository.has_values("HISTORIC"):
        return
    
    ticker_disney = "DIS"

    data = yf.download(
        ticker_disney,
        period="95d",
        interval="1d",
        auto_adjust=False
    )

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(1)
        
    historic_prices = [
        HistoricPrice(
            date_time=index.date(),
            close=row["Close"],
            high=row["High"],
            low=row["Low"],
            open=row["Open"],
            volume=row["Volume"]
        )
        for index, row in data.iterrows()
    ]

    historic_dict: dict[str, Any] = {
        item.date_time.isoformat(): item.model_dump()
        for item in historic_prices
    }
    await redis_repository.save_all("HISTORIC", historic_dict)



    