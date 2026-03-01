import base64

from cognova.generator.context_builder import (
    IMAGE_MEDIA_TYPES,
    process_text,
    process_code,
    process_image,
    process_document,
    process_openapi,
    process_url,
    process_attachments,
)
from cognova.scenario.loader import Attachment


def test_process_text_content(tmp_path):
    (tmp_path / "sample.txt").write_text("sample sentence")
    att = Attachment(path="sample.txt", type="text")
    result = process_text(att, tmp_path)
    assert result["text"] == "sample sentence"


def test_process_code_language(tmp_path):
    (tmp_path / "sample.py").write_text("print('hello')")
    att = Attachment(path="sample.py")
    result = process_code(att, tmp_path)
    assert "python" in result["text"]
    assert "hello" in result["text"]


def test_process_image_valid(tmp_path):
    raw_bytes = b"\x89PNG\r\n\x1a\nfake"
    (tmp_path / "sample.png").write_bytes(raw_bytes)
    att = Attachment(path="sample.png")
    result = process_image(att, tmp_path)
    assert result["type"] == "image"
    assert result["source"]["media_type"] == "image/png"
    assert base64.b64decode(result["source"]["data"]) == raw_bytes


import pytest


@pytest.mark.parametrize(
    ("ext", "expected_mime"),
    [
        (".png", "image/png"),
        (".jpg", "image/jpeg"),
        (".jpeg", "image/jpeg"),
        (".gif", "image/gif"),
        (".webp", "image/webp"),
    ],
)
def test_process_image_media_types(tmp_path, ext, expected_mime):
    raw_bytes = b"\x00\x01\x02"
    (tmp_path / f"img{ext}").write_bytes(raw_bytes)
    att = Attachment(path=f"img{ext}")
    result = process_image(att, tmp_path)
    assert result["source"]["media_type"] == expected_mime


def test_process_document_valid(tmp_path):
    raw_bytes = b"%PDF-1.4 fake content"
    (tmp_path / "doc.pdf").write_bytes(raw_bytes)
    att = Attachment(path="doc.pdf")
    result = process_document(att, tmp_path)
    assert result["type"] == "document"
    assert result["source"]["media_type"] == "application/pdf"
    assert base64.b64decode(result["source"]["data"]) == raw_bytes


def test_process_openapi_parses_yaml(tmp_path):
    (tmp_path / "spec.yaml").write_text("openapi: 3.0.0\ninfo:\n  title: Test API\n")
    att = Attachment(path="spec.yaml", type="openapi")
    result = process_openapi(att, tmp_path)
    assert result["type"] == "text"
    assert "OpenAPI Spec:" in result["text"]
    assert "Test API" in result["text"]


def test_process_url_placeholder():
    att = Attachment(path="https://example.com/docs", type="url")
    from pathlib import Path

    result = process_url(att, Path("."))
    assert result["type"] == "text"
    assert "https://example.com/docs" in result["text"]


@pytest.mark.parametrize(
    ("filename", "att_type", "expected_return_type"),
    [
        ("sample.txt", "text", "text"),
        ("sample.py", "code", "text"),
        ("sample.png", "image", "image"),
        ("sample.pdf", "document", "document"),
        ("spec.yaml", "openapi", "text"),
    ],
)
def test_process_attachments_routing(tmp_path, filename, att_type, expected_return_type):
    if att_type in ("image", "document"):
        (tmp_path / filename).write_bytes(b"\x00\x01")
    else:
        (tmp_path / filename).write_text("content")
    att = Attachment(path=filename, type=att_type)
    result = process_attachments([att], tmp_path)
    assert len(result) == 1
    assert result[0]["type"] == expected_return_type


def test_process_attachments_url_routing():
    from pathlib import Path

    att = Attachment(path="https://example.com", type="url")
    result = process_attachments([att], Path("."))
    assert len(result) == 1
    assert result[0]["type"] == "text"


def test_process_attachments_empty():
    from pathlib import Path

    result = process_attachments([], Path("."))
    assert result == []


def test_process_attachments_mixed(tmp_path):
    (tmp_path / "readme.txt").write_text("hello")
    (tmp_path / "app.py").write_text("x = 1")
    (tmp_path / "logo.png").write_bytes(b"\x89PNG")
    atts = [
        Attachment(path="readme.txt", type="text"),
        Attachment(path="app.py", type="code"),
        Attachment(path="logo.png", type="image"),
        Attachment(path="https://example.com", type="url"),
    ]
    result = process_attachments(atts, tmp_path)
    assert len(result) == 4
    assert result[0]["type"] == "text"
    assert result[1]["type"] == "text"
    assert result[2]["type"] == "image"
    assert result[3]["type"] == "text"
