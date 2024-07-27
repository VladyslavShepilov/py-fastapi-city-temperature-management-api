from pydantic import (
    BaseModel,
    conint,
    ValidationError,
    field_validator
    )


class City(BaseModel):
    id: conint(gt=0)
    name: str
    additional_info: str = None

    class Config:
        from_attributes = True


class CityIn(BaseModel):
    name: str
    additional_info: str = None

    class Config:
        from_attributes = True

    @field_validator("name")
    def validate_name(cls, v):
        if not v.strip():
            raise ValidationError("Name can't be empty")
        return v
