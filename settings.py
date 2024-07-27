from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str
    database_url: str = "sqlite+aiosqlite:///./weather.db"
    weather_api_url: str = "https://api.weatherapi.com/v1/current.json?"
    weather_api_key: str = "e4148f854b944f268c3152823242404"

    class Config:
        env_file = ".env"


settings = Settings()


def get_settings() -> Settings:
    return settings
