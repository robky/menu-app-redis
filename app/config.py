import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Settings:
    PROJECT_NAME: str = "Pavel Gaidukov"
    PROJECT_VERSION: str = "1.0.0"

    TEST: str = os.getenv("TEST")

    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "db")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
    if TEST:
        POSTGRES_DB: str = os.getenv("POSTGRES_DB") + "_test"
    else:
        POSTGRES_DB: str = os.getenv("POSTGRES_DB")

    DATABASE_URL = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    REDIS_SERVER = os.getenv("REDIS_SERVER")
    REDIS_PORT = os.getenv("REDIS_PORT", 6379)
    REDIS_DB = os.getenv("REDIS_DB", 0)


settings = Settings()
