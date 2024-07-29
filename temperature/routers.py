from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from settings import Settings, get_settings

from temperature import crud, schemas


router = APIRouter()


@router.get("/temperature/", response_model=list[schemas.Temperature])
async def get_all_temperature_records(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_temperature_data(db)


@router.get("/temperature/{city_id}/", response_model=list[schemas.TemperatureOut])
async def get_temperature_data_by_city_id(
    city_id: int, db: AsyncSession = Depends(get_db)
):
    temperatures = await crud.get_temperature_data_by_city_id(db=db, city_id=city_id)
    if not temperatures:
        raise HTTPException(status_code=404, detail="City not found")
    return temperatures


@router.post("/temperature/update/", response_model=list[schemas.Temperature])
async def update_temperature_records(
    db: AsyncSession = Depends(get_db), settings: Settings = Depends(get_settings)
):
    return await crud.add_new_records(db, settings)
