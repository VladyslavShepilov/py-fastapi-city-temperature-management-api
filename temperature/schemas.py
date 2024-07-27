from datetime import datetime
from pydantic import BaseModel, conint


class Temperature(BaseModel):
    id: conint(gt=0)
    temperature: float
    date_time: datetime
    city_id: conint(gt=0)

    class Config:
        from_attributes = True


class TemperatureIn(BaseModel):
    temperature: float
    date_time: datetime = datetime.now()
    city_id: conint(gt=0)

    class Config:
        from_attributes = True
