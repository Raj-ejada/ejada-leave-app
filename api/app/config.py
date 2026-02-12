import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Ejada Leave Portal API"
    ENV: str = os.getenv("ENV", "local")

    # Security
    JWT_SECRET: str = os.getenv("JWT_SECRET", "CHANGE_ME_DEV_ONLY")
    JWT_ALGO: str = "HS256"
    JWT_EXPIRE_MIN: int = 60 * 8

    # Database
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASS: str = os.getenv("DB_PASS", "postgres")
    DB_NAME: str = os.getenv("DB_NAME", "ejada_leave")

    # AWS
    AWS_REGION: str = os.getenv("AWS_REGION", "ap-south-1")
    S3_BUCKET: str = os.getenv("S3_BUCKET", "")
    SES_SENDER: str = os.getenv("SES_SENDER", "no-reply@ejada.com")

    # Auth Mode
    AUTH_MODE: str = os.getenv("AUTH_MODE", "local")  # local|cognito
    COGNITO_USER_POOL_ID: str = os.getenv("COGNITO_USER_POOL_ID", "")
    COGNITO_CLIENT_ID: str = os.getenv("COGNITO_CLIENT_ID", "")
    COGNITO_ISSUER: str = os.getenv("COGNITO_ISSUER", "")

    class Config:
        case_sensitive = True

settings = Settings()