from cv_ats_optimizer.utils.file_parser import parse_txt


def test_parse_txt_utf8():
    content = "Hello World".encode("utf-8")
    parsed = parse_txt(content)
    assert parsed == "Hello World"
