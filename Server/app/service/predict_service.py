from app.core.neural_network.model import NeuralNetwork
from app.dtos.predict_request import PredictRequest
from app.dtos.historic_price import HistoricPrice
from app.dtos.predict_response import PredictResponse
from app.dtos.predict_close import PredictClose
from app.repository.redis_repository import RedisRepository
from sklearn.preprocessing import MinMaxScaler
from datetime import timedelta
from app.core.config import settings
import numpy as np
import torch

class PredictService:
    def __init__(self, model: NeuralNetwork, repository: RedisRepository, x_scaler: MinMaxScaler, y_scaler: MinMaxScaler):
        self.model = model
        self.redis_repository = repository
        self.x_scaler = x_scaler
        self.y_scaler = y_scaler

        self.model.eval()

    async def predict(self, request: PredictRequest):
        used_manual_history = False
        skip_predict = False
        warn = ""
        historic = []
        days = request.how_many_days

        if request.historic_data and len(request.historic_data) >= 90:
            used_manual_history = True
            request.historic_data.sort(key=lambda x: x.date_time)
            historic = request.historic_data[-90:]

        elif settings.USE_REDIS:
            warn = "Para usar histórico manual, precisa de enviar no mínimo 90 dados de histórico"
            values: list[HistoricPrice] = await self.redis_repository.get_all("HISTORIC")
            values.sort(key=lambda x: x.date_time)
            historic = values[-90:]

        else:
            warn = "Redis desabilitado, para previsão é NECESSÁRIO passar histórico de no mínimo 90 dias."
            skip_predict = True

        if skip_predict:
            response = PredictResponse()
            response.used_manual_history = used_manual_history
            response.warn = warn
            response.result = []

            return response

        data = np.array([
            [p.close, p.high, p.low, p.open, p.volume]
            for p in historic
        ])

        data_scaled = self.x_scaler.transform(data)
        data_tensor = torch.FloatTensor(data_scaled).unsqueeze(0)

        with torch.no_grad():
            result = []
            for _ in range(days):
                predict = self.model(data_tensor)
                predict_scaled_value = predict.squeeze().item()
                predict_true_value = self.y_scaler.inverse_transform(predict.numpy()).squeeze().item()

                last = data[-1]
                new_fake_value = np.array([
                    predict_scaled_value,
                    last[1],
                    last[2],
                    last[0],
                    last[4] 
                ])

                data_tensor = data_tensor[:, 1:, :]
                new_fake_value_tensor = torch.FloatTensor(new_fake_value).view(1,1,5)
                data_tensor = torch.cat([data_tensor, new_fake_value_tensor], dim=1)
                
                result.append(predict_true_value)

        response = PredictResponse()
        response.used_manual_history = used_manual_history
        response.warn = warn

        date = historic[-1].date_time + timedelta(days=1)
        closes: list[PredictClose] = []
        for val in result:
            close = PredictClose()
            close.close = val
            close.date_time = date

            date += timedelta(days=1)
            closes.append(close)

        response.result = closes

        return response