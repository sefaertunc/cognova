import base64
import struct

import pytest

from cognova.generator.context_builder import (
    IMAGE_MEDIA_TYPES,
    _count_pdf_pages,
    _estimate_image_tokens,
    _estimate_text_tokens,
    _get_image_dimensions,
    estimate_attachment_cost,
    estimate_attachment_tokens,
    process_attachments,
    process_code,
    process_document,
    process_image,
    process_openapi,
    process_text,
    process_url,
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


# --- Cost Estimation Tests ---


def _make_png(width: int, height: int) -> bytes:
    """Build a minimal PNG header with given dimensions."""
    header = b"\x89PNG\r\n\x1a\n"
    ihdr_data = struct.pack(">II", width, height)
    # Pad to 24 bytes so struct.unpack at [16:24] works
    return header + b"\x00" * 4 + b"IHDR" + ihdr_data


def _make_gif(width: int, height: int) -> bytes:
    """Build a minimal GIF header with given dimensions."""
    return b"GIF89a" + struct.pack("<HH", width, height)


def _make_jpeg(width: int, height: int) -> bytes:
    """Build a minimal JPEG with SOF0 marker containing dimensions."""
    soi = b"\xff\xd8"
    # SOF0 marker: FF C0, length (2), precision (1), height (2), width (2)
    sof_length = struct.pack(">H", 8)  # length includes itself
    sof_data = b"\x01" + struct.pack(">HH", height, width)
    sof = b"\xff\xc0" + sof_length + sof_data
    eoi = b"\xff\xd9"
    return soi + sof + eoi


def test_get_image_dimensions_png(tmp_path):
    (tmp_path / "img.png").write_bytes(_make_png(800, 600))
    w, h = _get_image_dimensions(tmp_path / "img.png")
    assert (w, h) == (800, 600)


def test_get_image_dimensions_gif(tmp_path):
    (tmp_path / "img.gif").write_bytes(_make_gif(320, 240))
    w, h = _get_image_dimensions(tmp_path / "img.gif")
    assert (w, h) == (320, 240)


def test_get_image_dimensions_jpeg(tmp_path):
    (tmp_path / "img.jpg").write_bytes(_make_jpeg(1024, 768))
    w, h = _get_image_dimensions(tmp_path / "img.jpg")
    assert (w, h) == (1024, 768)


def test_get_image_dimensions_unknown_fallback(tmp_path):
    (tmp_path / "img.bmp").write_bytes(b"\x00" * 32)
    w, h = _get_image_dimensions(tmp_path / "img.bmp")
    assert (w, h) == (512, 512)


def test_estimate_image_tokens_no_resize():
    # 1000x1000: (1000*1000)/750 = 1333
    assert _estimate_image_tokens(1000, 1000) == 1333


def test_estimate_image_tokens_from_anthropic_docs():
    # Anthropic docs: 200x200 -> ~54 tokens
    assert _estimate_image_tokens(200, 200) == 53  # 40000 // 750


def test_estimate_image_tokens_with_resize():
    # 3000x2000: scale = 1568/3000, new dims = int(3000*s) x int(2000*s)
    scale = 1568 / 3000
    expected = (int(3000 * scale) * int(2000 * scale)) // 750
    assert _estimate_image_tokens(3000, 2000) == expected


def test_estimate_image_tokens_minimum():
    # Tiny image: 1x1 -> max(1, 0) = 1
    assert _estimate_image_tokens(1, 1) == 1


def test_estimate_text_tokens(tmp_path):
    # 400 bytes / 4 = 100 tokens
    (tmp_path / "file.txt").write_text("a" * 400)
    assert _estimate_text_tokens(tmp_path / "file.txt") == 100


def test_estimate_text_tokens_small(tmp_path):
    # 3 bytes / 4 = 0, but min is 1
    (tmp_path / "tiny.txt").write_text("abc")
    assert _estimate_text_tokens(tmp_path / "tiny.txt") == 1


def test_count_pdf_pages_single(tmp_path):
    pdf = b"%PDF-1.4\n/Type /Page\n/Type /Pages\nendobj"
    # 1 x "/Type /Page" minus 1 x "/Type /Pages" = 0, min 1
    (tmp_path / "doc.pdf").write_bytes(pdf)
    assert _count_pdf_pages(tmp_path / "doc.pdf") == 1


def test_count_pdf_pages_multiple(tmp_path):
    pdf = b"%PDF-1.4\n/Type /Pages\n/Type /Page\n/Type /Page\n/Type /Page\nendobj"
    # 4 x "/Type /Page" (includes the one in /Pages) minus 1 x "/Type /Pages"
    # Actually: "/Type /Page" appears in all 4 lines, "/Type /Pages" in 1
    # count("/Type /Page") = 4, count("/Type /Pages") = 1 -> 3
    (tmp_path / "doc.pdf").write_bytes(pdf)
    assert _count_pdf_pages(tmp_path / "doc.pdf") == 3


def test_estimate_attachment_tokens_url():
    att = Attachment(path="https://example.com", type="url")
    from pathlib import Path

    assert estimate_attachment_tokens(att, Path(".")) == 0


def test_estimate_attachment_tokens_text(tmp_path):
    (tmp_path / "file.txt").write_text("a" * 800)
    att = Attachment(path="file.txt", type="text")
    assert estimate_attachment_tokens(att, tmp_path) == 200


def test_estimate_attachment_tokens_image(tmp_path):
    (tmp_path / "img.png").write_bytes(_make_png(1000, 1000))
    att = Attachment(path="img.png", type="image")
    assert estimate_attachment_tokens(att, tmp_path) == 1333


def test_estimate_attachment_tokens_document(tmp_path):
    pdf = b"%PDF-1.4\n/Type /Pages\n/Type /Page\n/Type /Page\nendobj"
    (tmp_path / "doc.pdf").write_bytes(pdf)
    att = Attachment(path="doc.pdf", type="document")
    # 3 "/Type /Page" - 1 "/Type /Pages" = 2 pages * 1500 = 3000
    assert estimate_attachment_tokens(att, tmp_path) == 3000


def test_estimate_attachment_cost_structure(tmp_path):
    (tmp_path / "file.py").write_text("x = 1\n" * 100)
    atts = [Attachment(path="file.py", type="code")]
    result = estimate_attachment_cost(atts, tmp_path)
    assert "attachments" in result
    assert "total_estimated_tokens" in result
    assert "estimated_cost_usd" in result
    assert "model" in result
    assert "price_per_mtok" in result
    assert len(result["attachments"]) == 1
    assert result["attachments"][0]["path"] == "file.py"
    assert result["attachments"][0]["type"] == "code"
    assert result["total_estimated_tokens"] > 0
    assert result["estimated_cost_usd"] > 0


def test_estimate_attachment_cost_sonnet_pricing(tmp_path):
    # 400 bytes / 4 = 100 tokens, Sonnet input = $3.00/MTok
    (tmp_path / "file.txt").write_text("a" * 400)
    atts = [Attachment(path="file.txt", type="text")]
    result = estimate_attachment_cost(atts, tmp_path)
    assert result["total_estimated_tokens"] == 100
    assert result["price_per_mtok"] == 3.0
    assert result["estimated_cost_usd"] == round(100 * 3.0 / 1_000_000, 6)


def test_estimate_attachment_cost_opus_pricing(tmp_path):
    # 400 bytes / 4 = 100 tokens, Opus input = $5.00/MTok
    (tmp_path / "file.txt").write_text("a" * 400)
    atts = [Attachment(path="file.txt", type="text")]
    result = estimate_attachment_cost(atts, tmp_path, model="claude-opus-4-6")
    assert result["price_per_mtok"] == 5.0
    assert result["estimated_cost_usd"] == round(100 * 5.0 / 1_000_000, 6)


def test_estimate_attachment_cost_mixed(tmp_path):
    (tmp_path / "readme.txt").write_text("a" * 400)
    (tmp_path / "img.png").write_bytes(_make_png(200, 200))
    atts = [
        Attachment(path="readme.txt", type="text"),
        Attachment(path="img.png", type="image"),
        Attachment(path="https://example.com", type="url"),
    ]
    result = estimate_attachment_cost(atts, tmp_path)
    assert len(result["attachments"]) == 3
    assert result["attachments"][0]["estimated_tokens"] == 100  # 400/4
    assert result["attachments"][1]["estimated_tokens"] == 53  # (200*200)/750
    assert result["attachments"][2]["estimated_tokens"] == 0  # url
    assert result["total_estimated_tokens"] == 153


def test_estimate_attachment_cost_empty(tmp_path):
    result = estimate_attachment_cost([], tmp_path)
    assert result["total_estimated_tokens"] == 0
    assert result["estimated_cost_usd"] == 0
