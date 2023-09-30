import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load environment variables from the .env file in the current directory
load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    API_V1_STR: str = '/api/v1'
    DB_HOST: str =os.environ.get('DB_HOST')
    DB_PORT: str =os.environ.get('DB_PORT')
    DB_NAME: str =os.environ.get('DB_NAME')
    JWT_SECRET_KEY: str =os.environ.get('JWT_SECRET_KEY')
    SECRET_KEY: str =os.environ.get('SECRET_KEY')
    ALGORITHM: str =os.environ.get('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))

settings = Settings()
