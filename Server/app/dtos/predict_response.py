from pydantic import BaseModel, Field
from app.dtos.predict_close import PredictClose

class PredictResponse(BaseModel):
    used_manual_history: bool = Field(False)
    warn: str = Field("")
    result: list[PredictClose] = Field(default_factory=list)
    