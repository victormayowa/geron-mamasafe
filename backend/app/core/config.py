from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # App
    APP_NAME: str = "Geron Mamasafe Health AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/geron_mamasafe"
    )
    DATABASE_URL_SYNC: str = (
        "postgresql://postgres:postgres@localhost:5432/geron_mamasafe"
    )

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Twilio
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_WHATSAPP_NUMBER: str = "whatsapp:+14155238886"
    TWILIO_PHONE_NUMBER: str

    # AI - Free LLM Options
    # Option 1: OpenAI (paid)
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4"

    # Option 2: Groq (free tier - recommended)
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # Option 3: Ollama (local, completely free)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1:8b"

    # Option 4: HuggingFace (free tier)
    HUGGINGFACE_API_KEY: Optional[str] = None
    HUGGINGFACE_MODEL: str = "microsoft/Phi-3-mini-4k-instruct"

    # Active AI Provider (groq, ollama, openai, huggingface)
    AI_PROVIDER: str = "groq"

    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # Scheduler
    DAILY_MESSAGE_HOUR: int = 8
    DAILY_MESSAGE_TIMEZONE: str = "Africa/Lagos"

    # Health Center
    DEFAULT_HEALTH_CENTER_ID: int = 1

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
