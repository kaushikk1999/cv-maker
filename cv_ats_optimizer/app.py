"""Streamlit UI for ATS CV Optimizer Phase-1."""

from __future__ import annotations

from typing import Optional

import streamlit as st

from cv_ats_optimizer.config.settings import settings
from cv_ats_optimizer.parsers.jd_parser import JDStructured, extract_jd_sections
from cv_ats_optimizer.utils.file_parser import FileParsingError, parse_file
from cv_ats_optimizer.utils.text_processor import clean_text, count_words
from cv_ats_optimizer.utils.validators import InputValidator

st.set_page_config(page_title=settings.app_title, page_icon="📄", layout="wide")

if "cv_text" not in st.session_state:
    st.session_state.cv_text = ""
if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""
if "jd_structured" not in st.session_state:
    st.session_state.jd_structured = None

validator = InputValidator()


def _handle_file_upload(file, label: str) -> Optional[str]:
    if not file:
        return None
    extension_result = validator.validate_file_extension(file.name)
    if not extension_result.is_valid:
        st.error(extension_result.message)
        return None
    size_result = validator.validate_file_size(file.size)
    if not size_result.is_valid:
        st.error(size_result.message)
        return None
    try:
        content = parse_file(file.name, file.read())
    except FileParsingError as exc:
        st.error(f"Failed to parse {label}: {exc}")
        return None
    return content


def _display_text_preview(text: str, label: str) -> None:
    if not text:
        return
    with st.expander(f"Preview {label}"):
        st.write(text[:1000] + ("..." if len(text) > 1000 else ""))


st.title("ATS CV Optimizer – Phase 1")
st.caption("Ingest, validate, and parse job descriptions. No scoring yet.")

st.subheader("Candidate CV Input")
col_upload, col_paste = st.columns(2)

with col_upload:
    st.markdown("**Upload CV File**")
    uploaded_cv = st.file_uploader("Upload CV", type=["pdf", "docx", "txt"], key="upload_cv")
    if uploaded_cv is not None:
        content = _handle_file_upload(uploaded_cv, "CV file")
        if content:
            result = validator.validate_cv(content)
            if result.is_valid:
                st.session_state.cv_text = content
                st.success("CV uploaded and validated.")
            else:
                st.error(result.message)
    _display_text_preview(st.session_state.cv_text, "CV")

with col_paste:
    st.markdown("**Paste CV Text**")
    pasted_cv = st.text_area("Paste CV", value="", height=300, key="pasted_cv")
    if st.button("Use pasted CV"):
        if not pasted_cv:
            st.error("Please paste your CV text before submitting.")
        else:
            cleaned = clean_text(pasted_cv)
            result = validator.validate_cv(cleaned)
            if result.is_valid:
                st.session_state.cv_text = cleaned
                st.success("Pasted CV saved.")
            else:
                st.error(result.message)

if st.session_state.cv_text:
    st.info(f"CV ready with {count_words(st.session_state.cv_text)} words.")

st.divider()

st.subheader("Job Description Input")
input_mode = st.radio("Choose JD input method", options=["Paste Text", "Upload File"], horizontal=True)

if input_mode == "Paste Text":
    pasted_jd = st.text_area("Paste Job Description", value="", height=300, key="pasted_jd")
    if st.button("Use pasted JD"):
        if not pasted_jd:
            st.error("Please paste the job description before submitting.")
        else:
            cleaned = clean_text(pasted_jd)
            result = validator.validate_job_description(cleaned)
            if result.is_valid:
                st.session_state.jd_text = cleaned
                st.success("Job description saved.")
            else:
                st.error(result.message)
else:
    uploaded_jd = st.file_uploader("Upload Job Description", type=["pdf", "docx", "txt"], key="upload_jd")
    if uploaded_jd is not None:
        content = _handle_file_upload(uploaded_jd, "job description")
        if content:
            result = validator.validate_job_description(content)
            if result.is_valid:
                st.session_state.jd_text = content
                st.success("Job description uploaded and validated.")
            else:
                st.error(result.message)

_display_text_preview(st.session_state.jd_text, "Job Description")

if st.session_state.jd_text:
    st.info(f"Job description ready with {count_words(st.session_state.jd_text)} words.")

st.divider()

st.subheader("Analysis")
if st.button("Analyze JD & CV (Phase-1)"):
    if not st.session_state.cv_text:
        st.error("Please provide a CV before analysis.")
    elif not st.session_state.jd_text:
        st.error("Please provide a job description before analysis.")
    else:
        with st.spinner("Parsing job description..."):
            structured = extract_jd_sections(st.session_state.jd_text)
            st.session_state.jd_structured = structured
        st.success("Job description parsed successfully.")

structured: Optional[JDStructured] = st.session_state.jd_structured
if structured:
    st.header("Parsed Job Description")
    top_cols = st.columns(5)
    top_cols[0].metric("Job Title", structured.job_title or "N/A")
    top_cols[1].metric("Company", structured.company_name or "N/A")
    top_cols[2].metric("Location", structured.location or "N/A")
    top_cols[3].metric("Work Type", structured.work_type or "N/A")
    top_cols[4].metric("Experience", structured.experience_required or "N/A")

    with st.expander("Company Overview", expanded=False):
        st.write(structured.company_overview or "Not provided.")
    with st.expander("Role Summary", expanded=False):
        st.write(structured.role_summary or "Not provided.")
    with st.expander("Key Responsibilities", expanded=True):
        if structured.key_responsibilities:
            st.markdown("\n".join(f"- {item}" for item in structured.key_responsibilities))
        else:
            st.write("Not provided.")
    with st.expander("Required Skills", expanded=True):
        if structured.required_skills:
            st.markdown("\n".join(f"- {item}" for item in structured.required_skills))
        else:
            st.write("Not provided.")
    with st.expander("Preferred / Bonus Skills", expanded=False):
        if structured.preferred_skills:
            st.markdown("\n".join(f"- {item}" for item in structured.preferred_skills))
        else:
            st.write("Not provided.")
    with st.expander("Education", expanded=False):
        st.write(structured.education or "Not provided.")
    with st.expander("Soft Skills / Values", expanded=False):
        if structured.soft_skills:
            st.markdown("\n".join(f"- {item}" for item in structured.soft_skills))
        else:
            st.write("Not provided.")
    with st.expander("Diversity / Inclusion Statement", expanded=False):
        st.write(structured.diversity_statement or "Not provided.")
    with st.expander("Recruiter / Contact Information", expanded=False):
        st.write(structured.recruiter_info or "Not provided.")
    with st.expander("Keywords for ATS Optimization", expanded=False):
        if structured.keywords_for_ats:
            st.markdown(", ".join(structured.keywords_for_ats))
        else:
            st.write("Not available.")
