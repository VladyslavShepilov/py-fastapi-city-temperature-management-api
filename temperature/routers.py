from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from settings import Settings, get_settings

from temperature import crud, schemas


router = APIRouter()


@router.post("/temperatures/update/", response_model=list[schemas.Temperature])
async def update_temperature_records(
    db: AsyncSession = Depends(get_db),
    settings: Settings = Depends(get_settings)
):
    return await crud.add_new_records(db, settings)
