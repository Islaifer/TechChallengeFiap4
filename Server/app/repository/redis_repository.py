from app.core.config.redis_connection import get_redis_connection
from app.dtos.historic_price import HistoricPrice
from typing import Any, Dict
import json


class RedisRepository:
    def __init__(self):
        self.redis = get_redis_connection()

    async def get_all(self, ty: str):
        values = await self.redis.hvals(ty)

        return [
            HistoricPrice.model_validate(json.loads(v))
            for v in values
        ]

    async def save_all(self, ty: str, mapper: Dict[str, Any]):
        data_to_set = {
            k: json.dumps(v, default=str)
            for k, v in mapper.items()
        }

        await self.redis.hset(ty, mapping=data_to_set)

    async def has_values(self, ty: str) -> int:
        return await self.redis.hlen(ty)