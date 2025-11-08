"""Rule-based job description parser for Phase-1."""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Iterable

from cv_ats_optimizer.utils.text_processor import (
    clean_text,
    extract_email,
    extract_phone,
    top_tokens,
)


@dataclass
class JDStructured:
    job_title: str = ""
    company_name: str = ""
    location: str = ""
    work_type: str = ""
    experience_required: str = ""
    company_overview: str = ""
    role_summary: str = ""
    key_responsibilities: list[str] = field(default_factory=list)
    required_skills: list[str] = field(default_factory=list)
    preferred_skills: list[str] = field(default_factory=list)
    education: str = ""
    soft_skills: list[str] = field(default_factory=list)
    diversity_statement: str = "Not present in the JD."
    recruiter_info: str = ""
    keywords_for_ats: list[str] = field(default_factory=list)


def _collect_after_heading(lines: list[str], start_idx: int) -> list[str]:
    collected: list[str] = []
    for line in lines[start_idx + 1 :]:
        if not line.strip():
            break
        if re.match(r"^[\-•*\d]", line.strip()):
            collected.append(re.sub(r"^[\-•*\d\.\s]+", "", line.strip()))
        else:
            collected.append(line.strip())
    return collected


def _find_heading_indices(lines: list[str], patterns: Iterable[str]) -> list[int]:
    compiled = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    indices = []
    for idx, line in enumerate(lines):
        if any(pattern.search(line) for pattern in compiled):
            indices.append(idx)
    return indices


def extract_jd_sections(jd_text: str) -> JDStructured:
    cleaned_text = clean_text(jd_text)
    lines = [line.strip() for line in re.split(r"\n+", jd_text) if line.strip()]
    paragraphs = [para.strip() for para in re.split(r"\n\s*\n", jd_text) if para.strip()]

    structured = JDStructured()

    # Job Title
    title_patterns = [re.compile(r"job\s*title\s*:\s*(.+)", re.IGNORECASE)]
    for pattern in title_patterns:
        match = pattern.search(jd_text)
        if match:
            structured.job_title = clean_text(match.group(1))
            break
    if not structured.job_title and lines:
        structured.job_title = lines[0]

    # Company Name
    company_match = re.search(r"company\s*:\s*(.+)", jd_text, re.IGNORECASE)
    if company_match:
        structured.company_name = clean_text(company_match.group(1))

    # Location
    location_match = re.search(r"location\s*:\s*(.+)", jd_text, re.IGNORECASE)
    if location_match:
        structured.location = clean_text(location_match.group(1))

    # Work Type
    work_type_match = re.search(r"(work|employment)\s*type\s*:\s*(.+)", jd_text, re.IGNORECASE)
    if work_type_match:
        structured.work_type = clean_text(work_type_match.group(2))

    # Experience Required
    experience_match = re.search(r"(\d+\+?\s*(?:years|yrs).+experience)", jd_text, re.IGNORECASE)
    if experience_match:
        structured.experience_required = clean_text(experience_match.group(1))

    # Company Overview
    overview_indices = _find_heading_indices(lines, [r"about\s+us", r"about\s+the\s+company"])
    if overview_indices:
        idx = overview_indices[0]
        overview_lines = _collect_after_heading(lines, idx)[:3]
        structured.company_overview = " ".join(overview_lines)

    # Role Summary
    if len(paragraphs) > 1:
        structured.role_summary = paragraphs[1]

    # Key Responsibilities
    responsibility_indices = _find_heading_indices(
        lines, [r"responsibilit", r"what\s+you\s+will\s+do", r"duties"]
    )
    if responsibility_indices:
        items = _collect_after_heading(lines, responsibility_indices[0])
        structured.key_responsibilities = items

    # Required Skills
    required_indices = _find_heading_indices(
        lines, [r"required\s+skills", r"requirements", r"must\s+have"]
    )
    if required_indices:
        items = _collect_after_heading(lines, required_indices[0])
        structured.required_skills = _split_skill_items(items)

    # Preferred Skills
    preferred_indices = _find_heading_indices(
        lines, [r"preferred\s+skills", r"nice\s+to\s+have", r"bonus"]
    )
    if preferred_indices:
        items = _collect_after_heading(lines, preferred_indices[0])
        structured.preferred_skills = _split_skill_items(items)

    # Education
    education_match = re.search(
        r"(bachelor|master|phd|degree|b\.tech|bsc|msc)[^\n]+", jd_text, re.IGNORECASE
    )
    if education_match:
        structured.education = clean_text(education_match.group(0))

    # Soft Skills
    soft_skill_terms = [
        "communication",
        "team",
        "leadership",
        "ownership",
        "collaborat",
        "initiative",
        "adaptability",
        "problem-solving",
        "critical thinking",
    ]
    structured.soft_skills = [
        line for line in lines if any(term in line.lower() for term in soft_skill_terms)
    ]

    # Diversity Statement
    diversity_match = re.search(
        r"(equal opportunity|diversity|inclusive|inclusion)[^\n]+", jd_text, re.IGNORECASE
    )
    if diversity_match:
        structured.diversity_statement = clean_text(diversity_match.group(0))

    # Recruiter Info
    email = extract_email(jd_text)
    phone = extract_phone(jd_text)
    contact_parts = []
    if email:
        contact_parts.append(f"Email: {email}")
    if phone:
        contact_parts.append(f"Phone: {phone}")
    structured.recruiter_info = " | ".join(contact_parts) if contact_parts else "Not provided."

    structured.keywords_for_ats = top_tokens(cleaned_text, 25)

    return structured


def _split_skill_items(items: list[str]) -> list[str]:
    skills: list[str] = []
    for item in items:
        parts = re.split(r"[,;]\s*", item)
        for part in parts:
            if part:
                skills.append(part.strip())
    return skills


__all__ = ["JDStructured", "extract_jd_sections"]
