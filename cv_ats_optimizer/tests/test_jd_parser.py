from cv_ats_optimizer.parsers.jd_parser import extract_jd_sections


def test_extract_jd_sections_basic():
    jd_text = """
    Job Title: Senior Software Engineer
    Company: Tech Innovators Inc.
    Location: Remote
    Employment Type: Full-time
    We are looking for a talented engineer to join our mission.

    About Us
    Tech Innovators builds scalable platforms.

    Responsibilities
    - Build new services
    - Collaborate with cross-functional teams

    Requirements
    - Python
    - 5+ years experience building APIs

    Preferred Skills
    - AWS, Docker

    Education
    Bachelor's degree in Computer Science

    Contact: hiring@techinnovators.com
    """

    structured = extract_jd_sections(jd_text)

    assert structured.job_title == "Senior Software Engineer"
    assert structured.company_name == "Tech Innovators Inc."
    assert "Build new services" in structured.key_responsibilities
    assert "Python" in structured.required_skills
    assert structured.education
    assert "Email:" in structured.recruiter_info
    assert structured.keywords_for_ats
