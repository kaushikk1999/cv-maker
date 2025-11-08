"""Application constants for ATS CV Optimizer Phase-1."""

from __future__ import annotations

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_FILE_SIZE_MB = 5

APPROVED_ACTION_VERBS = [
    "achieved",
    "analyzed",
    "architected",
    "automated",
    "built",
    "collaborated",
    "conducted",
    "created",
    "delivered",
    "designed",
    "developed",
    "drove",
    "enhanced",
    "engineered",
    "executed",
    "expanded",
    "implemented",
    "improved",
    "launched",
    "led",
    "managed",
    "optimized",
    "orchestrated",
    "organized",
    "owned",
    "piloted",
    "planned",
    "reduced",
    "resolved",
    "shipped",
    "streamlined",
    "spearheaded",
    "supported",
    "transformed",
]

BANNED_TERMS = [
    "guru",
    "rockstar",
    "ninja",
    "wizard",
    "synergy",
    "best-in-class",
    "world-class",
    "wheelhouse",
    "leverage (as noun)",
    "game changer",
    "out-of-the-box thinker",
]

STOPWORDS = [
    "a",
    "an",
    "the",
    "and",
    "or",
    "but",
    "if",
    "in",
    "on",
    "for",
    "with",
    "to",
    "of",
    "at",
    "by",
    "from",
    "as",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
]

CONFIGURATION_RULES = {
    "enforce_unique_words": True,
    "enforce_stopword_ban": False,
    "enforce_banned_terms": True,
    "enforce_min_word_count": True,
}
