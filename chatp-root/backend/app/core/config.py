import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load environment variables from the .env file in the current directory
load_dotenv()


class CommonSettings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    ORIGINS: list[str] = [
        'http://localhost',
        'http://localhost:8080',
        'http://localhost:5173',
    ]
    APP_NAME: str = os.environ.get('APP_NAME')
    DEBUG_MODE: bool = os.environ.get('DEBUG_MODE')


class TokenSettings(BaseSettings):
    # created by '$ openssl rand -hex 32'
    JWT_SECRET_KEY: str = os.environ.get('SECRET_KEY')
    ALGORITHM: str = os.environ.get('ALGORITHM')
    # 60 minutes * 24 hours * 7 days = 7 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))


class ServerSettings(BaseSettings):
    HOST: str = os.environ.get('DB_HOST')
    PORT: int = int(os.environ.get('DB_PORT'))


class DatabaseSettings(BaseSettings):
    DB_NAME: str = os.environ.get('DB_NAME')


class CollectionSettings(BaseSettings):
    USERS_COLLECTION: str = os.environ.get('USERS_COLLECTION')
    PRIVATE_CHAT_COLLECTION: str = os.environ.get('PRIVATE_CHAT_COLLECTION')
    GROUP_CHAT_COLLECTION: str = os.environ.get('GROUP_CHAT_COLLECTION')


class Settings(CommonSettings, TokenSettings, ServerSettings, DatabaseSettings, CollectionSettings):
    model_config = SettingsConfigDict(case_sensitive=True)


# class Settings(BaseSettings):

#     API_V1_STR: str = '/api/v1'

#     JWT_SECRET_KEY: str =os.environ.get('JWT_SECRET_KEY')
#     SECRET_KEY: str =os.environ.get('SECRET_KEY')
#     ALGORITHM: str =os.environ.get('ALGORITHM')
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))
settings = Settings()
