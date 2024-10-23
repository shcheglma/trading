from pydantic_settings import BaseSettings
import motor.motor_asyncio


class Settings(BaseSettings):
    APP_NAME: str
    DATABASE_URL: str

    class Config:
        env_file = './.env'


settings = Settings()
MONGO_DETAILS = "mongodb://maria:mariapassword@127.0.0.1:27018/?authSource=admin&readPreference=primary&appname" \
                "=MongoDB%20Compass&ssl=false"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.binance
currency_collection = database.get_collection("currency")
