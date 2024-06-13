from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEV_MODE: bool = False
    VECTOR_URLS: str
    LOG_LEVEL: str = "INFO"


settings = Settings()
