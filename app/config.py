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
    DB_DRIVER: str = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")

    FRONTEND_ORIGIN: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "change_this_secret_key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )

    AI_PROVIDER = os.getenv("AI_PROVIDER", "azure").lower()
    EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "azure").lower()

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL_NAME: str = os.getenv("GEMINI_MODEL_NAME", "gemini-3.5-flash")

    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_BASE_URL: str = os.getenv("AZURE_OPENAI_BASE_URL", "")
    AZURE_OPENAI_DEPLOYMENT_NAME: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")
    AZURE_OPENAI_EMBEDDING_MODEL: str = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL", "")

    LMSTUDIO_MODEL_NAME: str = os.getenv("LMSTUDIO_MODEL_NAME", "")
    LMSTUDIO_BASE_URL: str = os.getenv("LMSTUDIO_BASE_URL", "")
    LMSTUDIO_API_KEY: str = os.getenv("LMSTUDIO_API_KEY", "")

    OLLAMA_MODEL_NAME: str = os.getenv("OLLAMA_MODEL_NAME", "")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "")

    VIP_FRONTEND_URL: str = os.getenv("VIP_FRONTEND_URL", "http://localhost:5174")

    VECTOR_DB_DIR: str = os.getenv("VECTOR_DB_DIR", "")


settings = Settings()