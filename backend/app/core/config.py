import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load environment variables from the .env file in the current directory
load_dotenv()



class CommonSettings(BaseSettings):
    APP_NAME: str = 'Real Time Chat APP'
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    HOST: str = os.environ.get('DB_HOST')
    PORT: int = int(os.environ.get('DB_PORT'))


class DatabaseSettings(BaseSettings):
    DB_NAME: str = os.environ.get('DB_NAME')


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)



# class Settings(BaseSettings):

#     API_V1_STR: str = '/api/v1'
   
#     JWT_SECRET_KEY: str =os.environ.get('JWT_SECRET_KEY')
#     SECRET_KEY: str =os.environ.get('SECRET_KEY')
#     ALGORITHM: str =os.environ.get('ALGORITHM')
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))

settings = Settings()

