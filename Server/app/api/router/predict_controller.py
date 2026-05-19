from fastapi import APIRouter, Depends
from app.dtos.predict_request import PredictRequest
from app.dtos.predict_response import PredictResponse
from app.service.predict_service import PredictService
from app.core.startup.bootstrap import get_predict_service

router = APIRouter(prefix="/predict", tags=["Predict"])

@router.post("", response_model=PredictResponse)
async def register(request: PredictRequest, service = Depends(get_predict_service)):
    """
    Rote feita para predição de valores do ativo Disney

    Parameters
    ----------
    Request contendo o histórico de 90 dias atrás e quantos dias será a previsão (quanto mais dias, menor preciso fica)

    Returns
    -------
    Retorno das predições

    """
    predict = await service.predict(request)
    return predict