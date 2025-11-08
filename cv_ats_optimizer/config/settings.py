"""Environment driven settings for ATS CV Optimizer."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


def _get_bool(env_value: str | None, default: bool) -> bool:
    if env_value is None:
        return default
    return env_value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    """Typed settings object so the rest of the app can depend on it."""

    app_title: str = os.getenv("APP_TITLE", "ATS CV Optimizer")
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")
    max_file_size_mb: int = int(os.getenv("MAX_FILE_SIZE_MB", "5"))
    enforce_unique_words: bool = _get_bool(os.getenv("ENFORCE_UNIQUE_WORDS"), True)
    enforce_stopword_ban: bool = _get_bool(os.getenv("ENFORCE_STOPWORD_BAN"), False)
    enforce_banned_terms: bool = _get_bool(os.getenv("ENFORCE_BANNED_TERMS"), True)
    enforce_min_word_count: bool = _get_bool(os.getenv("ENFORCE_MIN_WORD_COUNT"), True)


settings = Settings()

__all__ = ["settings", "Settings"]
