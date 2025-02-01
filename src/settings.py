from os import environ
from dotenv import load_dotenv


load_dotenv()


class Settings:
    BOT_TOKEN = environ.get("BOT_TOKEN")
    API_BASE_URL = environ.get("API_BASE_URL")
    JWT_SECRET = environ.get("JWT_SECRET")
    IMEI_API_TOKEN = environ.get("IMEI_API_TOKEN")
    DB_URI = environ.get("DB_URI")
