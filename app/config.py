try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings 


class Settings(BaseSettings):

    PROJECT_NAME: str = "Personal Finance Tracker"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./finance.db"
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
    API_BASE_URL: str = "http://127.0.0.1:8000"

    class Config:

        env_file = ".env"
        case_sensitive = False


settings = Settings()
