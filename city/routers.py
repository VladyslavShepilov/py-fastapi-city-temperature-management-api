from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db

from city import crud, schemas


router = APIRouter()


@router.get("/city/", response_model=list[schemas.City])
async def get_all_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db=db)


@router.get("/city/{city_id}/", response_model=schemas.City)
async def get_city_by_id(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_city_by_id(db=db, city_id=city_id)


@router.post("/city/", response_model=schemas.City)
async def create_city(city: schemas.CityIn, db: AsyncSession = Depends(get_db)):
    return await crud.create_city(db=db, city=city)


@router.delete("/city/{city_id}/", response_model=dict)
async def delete_city_by_id(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_city_by_id(city_id=city_id, db=db)
