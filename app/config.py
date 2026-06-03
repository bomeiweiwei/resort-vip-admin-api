import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Resort VIP Admin API")
    APP_ENV: str = os.getenv("APP_ENV", "local")

    DB_SERVER: str = os.getenv("DB_SERVER", "localhost")
    DB_NAME: str = os.getenv("DB_NAME", "ResortVipAdminDB")
    DB_USER: str = os.getenv("DB_USER", "resortmgr")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_DRIVER: str = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")

    FRONTEND_ORIGIN: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "change_this_secret_key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )


settings = Settings()