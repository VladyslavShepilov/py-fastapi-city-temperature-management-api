from datetime import datetime
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from temperature.models import Temperature as TemperatureModel
from temperature.schemas import Temperature as TemperatureSchema, TemperatureIn
from city import crud as city_crud
from settings import Settings


async def get_temperature_from_api(
    city_id: int,
    city_name: str,
    settings: Settings
) -> TemperatureIn:
    api_url = settings.weather_api_url
    api_key = settings.weather_api_key
    city_name = city_name.capitalize()
    params = {"key": api_key, "q": city_name}

    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error while fetching data")

    data = response.json()
    date_time = datetime.strptime(data.get("current", {}).get("last_updated"), "%Y-%m-%d %H:%M")
    temperature = data.get("current", {}).get("temp_c")

    return TemperatureIn(
        temperature=temperature,
        date_time=date_time,
        city_id=city_id
    )


async def create_record(
    city_id: int,
    city_name: str,
    db: AsyncSession,
    settings: Settings
):
    temperature_in = await get_temperature_from_api(city_id, city_name, settings)
    temperature_data = temperature_in.dict()
    temperature = TemperatureModel(**temperature_data)
    db.add(temperature)
    try:
        await db.commit()
        await db.refresh(temperature)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Could not insert temperature data")

    return TemperatureSchema.from_orm(temperature)


async def add_new_records(db: AsyncSession, settings: Settings):
    city_list = await city_crud.get_all_cities(db)
    inserted_records = []

    for city in city_list:
        recorded_temperature = await create_record(city.id, city.name, db, settings)
        inserted_records.append(recorded_temperature)
    return inserted_records
