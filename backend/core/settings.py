from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEV_MODE: bool = False
    VECTOR_CONFIG_MAP_PATH: str = ""
    LOG_LEVEL: str = "INFO"


settings = Settings()
