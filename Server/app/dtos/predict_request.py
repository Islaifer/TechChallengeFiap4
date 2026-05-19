from pydantic import BaseModel, Field
from app.dtos.historic_price import HistoricPrice

class PredictRequest(BaseModel):
    how_many_days: int = Field(0)
    historic_data: list[HistoricPrice] = Field(default_factory=list)
