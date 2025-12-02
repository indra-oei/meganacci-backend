from pydantic_settings import BaseSettings;

class Settings(BaseSettings):
    PROJECT_NAME: str = "Meganacci API"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_KEY: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()