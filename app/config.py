from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = "AI SaaS Starter"
    DEBUG: bool = False
    
    # Security (Defaults provided for local dev, but must be set in .env for prod)
    SECRET_KEY: str = "dev-secret-key-change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 7 days
    
    # Database
    DATABASE_URL: str = "sqlite:///./app.db"

    # Automatically load from a .env file if it exists
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()