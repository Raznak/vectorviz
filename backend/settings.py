from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEV_MODE: bool = False


settings = Settings()
