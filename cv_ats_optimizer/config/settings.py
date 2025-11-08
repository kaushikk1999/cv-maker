"""Environment-driven settings loader for the ATS CV Optimizer project."""

# Consumer modules should import like:
# from config.settings import settings

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Container for environment configuration values."""

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    APP_TITLE = os.getenv("APP_TITLE", "ATS CV Optimizer")
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 5))


settings = Settings()

__all__ = ["Settings", "settings"]
