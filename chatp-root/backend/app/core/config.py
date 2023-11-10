import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load environment variables from the .env file in the current directory
load_dotenv()


class CommonSettings(BaseSettings):
    API_V_STR: str = os.environ.get('API_V_STR')
    ORIGINS: list[str] = os.environ.get("ALLOWED_ORIGINS").split(',')
    API_ORIGIN: str = os.environ.get('API_ORIGIN')
    FRONTEND_LOGIN_URL: str = os.environ.get('FRONTEND_LOGIN_URL')
    APP_NAME: str = os.environ.get('APP_NAME')
    DEBUG_MODE: bool = os.environ.get('DEBUG_MODE', False)


class TokenSettings(BaseSettings):
    # created by '$ openssl rand -hex 32'
    JWT_SECRET_KEY: str = os.environ.get('JWT_SECRET_KEY')
    ALGORITHM: str = os.environ.get('ALGORITHM')
    ACCESS_TOKEN_SUBJECT_KEY: str = 'id'
    # 60 minutes * 24 hours * 7 days = 7 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))   
    ACTIVATION_SECRET_KEY: str = os.environ.get('ACTIVATION_SECRET_KEY')


class ServerSettings(BaseSettings):
    HOST: str = os.environ.get('DB_HOST')
    PORT: int = int(os.environ.get('DB_PORT'))


class DatabaseSettings(BaseSettings):
    DB_NAME: str = os.environ.get('DB_NAME')


class CollectionSettings(BaseSettings):
    USERS_COLLECTION: str = os.environ.get('USERS_COLLECTION')
    PRIVATE_CHAT_COLLECTION: str = os.environ.get('PRIVATE_CHAT_COLLECTION')
    GROUP_CHAT_COLLECTION: str = os.environ.get('GROUP_CHAT_COLLECTION')

class CelerySettings(BaseSettings):
    CELERY_BROKER_URL: str = os.environ.get('CELERY_BROKER')
    CELERY_RESULT_BACKEND: str = os.environ.get('CELERY_BACKEND')

class EmailSettings(BaseSettings):
    SENDER_EMAIL: str = os.environ.get('SENDER_EMAIL')
    EMAIL_PASSWORD: str= os.environ.get('EMAIL_PASSWORD')

class Settings(
    CommonSettings, 
    TokenSettings, 
    ServerSettings, 
    DatabaseSettings, 
    CollectionSettings,
    CelerySettings,
    EmailSettings
    ):
    model_config = SettingsConfigDict(case_sensitive=True)



settings = Settings()

