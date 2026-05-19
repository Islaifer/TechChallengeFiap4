from datetime import date
from pydantic import BaseModel, Field

class HistoricPrice(BaseModel):
    date_time: date = Field(default_factory=date.today)
    close: float = Field(0)
    high: float = Field(0)
    low: float = Field(0)
    open: float = Field(0)
    volume: int = Field(0)