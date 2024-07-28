from datetime import datetime
import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from temperature.models import Temperature as TemperatureModel
from temperature.schemas import Temperature, TemperatureOut, TemperatureIn
from city import crud as city_crud
from city.models import City as CityModel
from settings import Settings


async def get_all_temperature_data(db: AsyncSession) -> list[Temperature]:
    query = select(TemperatureModel)
    result = await db.execute(query)
    temperature_list = result.scalars().all()
    return [Temperature.from_orm(temperature) for temperature in temperature_list]


async def get_temperature_data_by_city_id(db: AsyncSession, city_id: int) -> list[TemperatureOut]:
    query = (
        select(
            CityModel.name.label("city"),
            TemperatureModel.temperature,
            TemperatureModel.date_time,
        )
        .filter(CityModel.id == city_id)
        .join(TemperatureModel, TemperatureModel.city_id == CityModel.id)
        .order_by(TemperatureModel.date_time.asc())
    )
    result = await db.execute(query)
    temperature_list = result.all()
    return [
        TemperatureOut(
            city=row.city, temperature=row.temperature, date_time=row.date_time
        )
        for row in temperature_list
    ]


async def get_temperature_from_api(
    city_id: int, city_name: str, settings: Settings
) -> TemperatureIn:
    api_url = settings.weather_api_url
    api_key = settings.weather_api_key
    city_name = city_name.capitalize()
    params = {"key": api_key, "q": city_name}

    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, params=params)
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Error while fetching data"
        )

    data = response.json()
    date_time = datetime.strptime(
        data.get("current", {}).get("last_updated"), "%Y-%m-%d %H:%M"
    )
    temperature = data.get("current", {}).get("temp_c")

    return TemperatureIn(temperature=temperature, date_time=date_time, city_id=city_id)


async def create_record(
    city_id: int, city_name: str, db: AsyncSession, settings: Settings
) -> Temperature:
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

    return Temperature.from_orm(temperature)


async def add_new_records(
        db: AsyncSession,
        settings: Settings
) -> list[Temperature]:
    city_list = await city_crud.get_all_cities(db)
    inserted_records = []

    for city in city_list:
        recorded_temperature = await create_record(city.id, city.name, db, settings)
        inserted_records.append(recorded_temperature)
    return inserted_records
