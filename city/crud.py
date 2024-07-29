from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from city import schemas, models


async def get_all_cities(db: AsyncSession) -> list[schemas.City]:
    query = select(models.City)
    result = await db.execute(query)
    city_list = result.scalars().all()
    return [schemas.City.from_orm(city) for city in city_list]


async def get_city_by_id(db: AsyncSession, city_id: int) -> schemas.City:
    query = select(models.City).filter(models.City.id == city_id)
    result = await db.execute(query)
    city = result.scalar_one_or_none()
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return schemas.City.from_orm(city)


async def create_city(db: AsyncSession, city: schemas.CityIn) -> schemas.City:
    query = select(models.City).filter(models.City.name == city.name)
    result = await db.execute(query)
    city_exists = result.scalar_one_or_none()
    if city_exists:
        raise HTTPException(status_code=400, detail="City already exists!")

    query = (
        insert(models.City)
        .values(name=city.name, additional_info=city.additional_info)
        .returning(models.City.id)
    )
    result = await db.execute(query)
    await db.commit()

    new_city_id = result.scalar()
    new_city = schemas.City(
        id=new_city_id, name=city.name, additional_info=city.additional_info
    )

    return schemas.City.from_orm(new_city)


async def delete_city_by_id(db: AsyncSession, city_id: int) -> dict[str]:
    delete_query = delete(models.City).filter(models.City.id == city_id)
    result = await db.execute(delete_query)
    await db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="City not found")

    return {"detail": "City deleted successfully"}
