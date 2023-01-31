import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Settings:
    PROJECT_NAME: str = "Pavel Gaidukov"
    PROJECT_VERSION: str = "1.0.0"

    TEST: str | None = os.getenv("TEST")

    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "db")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str
    if TEST:
        POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres") + "_test"
    else:
        POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")

    DATABASE_URL = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    REDIS_SERVER = os.getenv("REDIS_SERVER", "redis")
    REDIS_PORT = os.getenv("REDIS_PORT", 6379)
    REDIS_DB = os.getenv("REDIS_DB", 1)


settings = Settings()
