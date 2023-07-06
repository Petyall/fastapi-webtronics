from pydantic import BaseSettings

class Settings(BaseSettings):
    SMTP_HOST:str
    SMTP_PORT:int
    SMTP_USER:str
    SMTP_PASS:str

    SECRET_KEY = 'my_secret_key'
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    APP_ORIGIN='http://127.0.0.1:8000/'

    
    class Config:
        env_file = '.env'

settings = Settings()