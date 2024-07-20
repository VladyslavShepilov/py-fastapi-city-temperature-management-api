from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str
    database_url: str = "sqlite+aiosqlite:///./weather.db"

    class Config:
        env_file = ".env"


settings = Settings()
