"""Text processing helpers used throughout the application."""

from __future__ import annotations

import re
from collections import Counter
from typing import Iterable, List

_WORD_RE = re.compile(r"[A-Za-z0-9']+")
_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_PHONE_RE = re.compile(
    r"(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{3}\)?[\s-]?)?\d{3}[\s-]?\d{4}"
)


def clean_text(text: str) -> str:
    """Normalize whitespace and strip control characters."""

    if not text:
        return ""
    normalized = re.sub(r"[\r\f\v]", " ", text)
    normalized = re.sub(r"\u00a0", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()


def tokenize_words(text: str) -> List[str]:
    """Tokenize text into lowercase alphanumeric words."""

    if not text:
        return []
    return [match.group(0).lower() for match in _WORD_RE.finditer(text)]


def extract_email(text: str) -> str | None:
    """Return the first email address found in the text."""

    if not text:
        return None
    match = _EMAIL_RE.search(text)
    return match.group(0) if match else None


def extract_phone(text: str) -> str | None:
    """Return the first phone number pattern found in the text."""

    if not text:
        return None
    match = _PHONE_RE.search(text)
    return match.group(0) if match else None


def count_words(text: str) -> int:
    """Count the number of word tokens in the text."""

    return len(tokenize_words(text))


def top_tokens(text: str, limit: int = 25) -> list[str]:
    """Return the most frequent tokens within the text up to limit."""

    tokens = tokenize_words(text)
    if not tokens:
        return []
    counter = Counter(tokens)
    most_common = counter.most_common(limit)
    return [token for token, _ in most_common]


__all__ = [
    "clean_text",
    "tokenize_words",
    "extract_email",
    "extract_phone",
    "count_words",
    "top_tokens",
]
