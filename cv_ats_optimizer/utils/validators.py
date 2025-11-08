"""Validation helpers for uploaded or pasted text."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from cv_ats_optimizer.config.constants import ALLOWED_EXTENSIONS
from cv_ats_optimizer.config.settings import settings
from cv_ats_optimizer.utils.text_processor import clean_text


@dataclass
class ValidationResult:
    is_valid: bool
    message: str


class InputValidator:
    """Collection of validation routines for files and text content."""

    MIN_CV_CHAR_LENGTH = 300
    MIN_JD_CHAR_LENGTH = 200

    CV_KEYWORDS = {"experience", "education", "project", "work", "intern", "skills"}
    JD_KEYWORDS = {"responsibilities", "requirements", "skills", "job", "role"}

    @staticmethod
    def validate_file_extension(filename: str) -> ValidationResult:
        extension = Path(filename).suffix.lower()
        if extension in ALLOWED_EXTENSIONS:
            return ValidationResult(True, "Valid file extension.")
        return ValidationResult(False, f"Unsupported file type: {extension}.")

    @staticmethod
    def validate_file_size(size_bytes: int) -> ValidationResult:
        max_bytes = settings.max_file_size_mb * 1024 * 1024
        if size_bytes <= max_bytes:
            return ValidationResult(True, "File size within limits.")
        return ValidationResult(False, f"File exceeds maximum allowed size of {settings.max_file_size_mb} MB.")

    @staticmethod
    def validate_text_input(text: str, min_len: int) -> ValidationResult:
        cleaned = clean_text(text)
        if not cleaned:
            return ValidationResult(False, "Text content is empty after cleaning.")
        if len(cleaned) < min_len:
            return ValidationResult(False, f"Text content must be at least {min_len} characters.")
        return ValidationResult(True, "Text content length is sufficient.")

    @classmethod
    def validate_cv(cls, text: str) -> ValidationResult:
        result = cls.validate_text_input(text, cls.MIN_CV_CHAR_LENGTH)
        if not result.is_valid:
            return result
        lowered = clean_text(text).lower()
        if not any(keyword in lowered for keyword in cls.CV_KEYWORDS):
            return ValidationResult(False, "CV must mention experience, education, or skills.")
        return ValidationResult(True, "CV looks valid.")

    @classmethod
    def validate_job_description(cls, text: str) -> ValidationResult:
        result = cls.validate_text_input(text, cls.MIN_JD_CHAR_LENGTH)
        if not result.is_valid:
            return result
        lowered = clean_text(text).lower()
        if not any(keyword in lowered for keyword in cls.JD_KEYWORDS):
            return ValidationResult(False, "Job description must mention responsibilities or requirements.")
        return ValidationResult(True, "Job description looks valid.")

    validate_jd = validate_job_description


__all__ = ["InputValidator", "ValidationResult"]
