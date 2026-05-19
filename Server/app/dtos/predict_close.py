from pydantic import BaseModel, Field

class PredictClose(BaseModel):
    close: float = Field(0)
    date_time: str = Field("")