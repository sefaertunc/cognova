import base64
import struct
from pathlib import Path
from typing import Any

import yaml

from cognova.scenario.loader import Attachment, detect_language
from cognova.utils.cost_tracker import PRICING_REGISTRY

IMAGE_MEDIA_TYPES: dict[str, str] = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


def process_text(attachment: Attachment, base_path: Path) -> dict[str, Any]:
    with open(base_path / attachment.path) as file:
        content = file.read()
    return {"type": "text", "text": content}


def process_code(attachment: Attachment, base_path: Path) -> dict[str, Any]:
    with open(base_path / attachment.path) as file:
        content = file.read()
    language = detect_language(attachment.path)
    return {"type": "text", "text": f"```{language}\n{content}\n```"}


def process_image(attachment: Attachment, base_path: Path) -> dict[str, Any]:
    with open(base_path / attachment.path, "rb") as file:
        file_bytes = file.read()
    ext = Path(attachment.path).suffix.lower()
    media_type = IMAGE_MEDIA_TYPES.get(ext, "image/png")
    data = base64.b64encode(file_bytes).decode()
    return {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": data}}


def process_document(attachment: Attachment, base_path: Path) -> dict[str, Any]:
    with open(base_path / attachment.path, "rb") as file:
        file_bytes = file.read()
    data = base64.b64encode(file_bytes).decode()
    return {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": data}}


def process_openapi(attachment: Attachment, base_path: Path) -> dict[str, Any]:
    with open(base_path / attachment.path) as file:
        formatted_content = yaml.safe_load(file)
    return {"type": "text", "text": f"OpenAPI Spec:\n{formatted_content}"}


def process_url(attachment: Attachment, base_path: Path) -> dict[str, Any]:  # noqa: ARG001
    return {"type": "text", "text": f"URL reference: {attachment.path}"}


def process_attachments(attachments: list[Attachment], base_path: Path) -> list[dict[str, Any]]:
    processes = []
    for attachment in attachments:
        if attachment.type == "image":
            processes.append(process_image(attachment=attachment, base_path=base_path))
        elif attachment.type == "document":
            processes.append(process_document(attachment=attachment, base_path=base_path))
        elif attachment.type == "code":
            processes.append(process_code(attachment=attachment, base_path=base_path))
        elif attachment.type == "text":
            processes.append(process_text(attachment=attachment, base_path=base_path))
        elif attachment.type == "openapi":
            processes.append(process_openapi(attachment=attachment, base_path=base_path))
        elif attachment.type == "url":
            processes.append(process_url(attachment=attachment, base_path=base_path))
    return processes


# --- Cost Estimation ---
# Real-world token formulas from Anthropic docs:
# - Text: ~4 characters per token (Anthropic documented heuristic)
# - Images: (width * height) / 750, scaled to fit 1568px max dimension
# - PDF: ~1,500 tokens per page (each page rendered as image)
# - URL: 0 (cannot estimate without fetching)

CHARS_PER_TOKEN = 4
IMAGE_MAX_DIMENSION = 1568
IMAGE_TOKEN_DIVISOR = 750
PDF_TOKENS_PER_PAGE = 1500
DEFAULT_MODEL = "claude-sonnet-4-5-20250514"


def _get_image_dimensions(file_path: Path) -> tuple[int, int]:
    """Parse image dimensions from file header. No external dependencies."""
    with open(file_path, "rb") as f:
        header = f.read(32)

    ext = file_path.suffix.lower()

    if ext == ".png" and header[:8] == b"\x89PNG\r\n\x1a\n":
        width, height = struct.unpack(">II", header[16:24])
        return width, height

    if ext == ".gif" and header[:6] in (b"GIF87a", b"GIF89a"):
        width, height = struct.unpack("<HH", header[6:10])
        return width, height

    if ext in (".jpg", ".jpeg"):
        return _get_jpeg_dimensions(file_path)

    if (
        ext == ".webp"
        and header[:4] == b"RIFF"
        and header[8:12] == b"WEBP"
        and header[12:16] == b"VP8 "
    ):
        width = struct.unpack("<H", header[26:28])[0] & 0x3FFF
        height = struct.unpack("<H", header[28:30])[0] & 0x3FFF
        return width, height

    return 512, 512


def _get_jpeg_dimensions(file_path: Path) -> tuple[int, int]:
    """Parse JPEG dimensions from SOF markers."""
    with open(file_path, "rb") as f:
        f.read(2)  # skip SOI
        while True:
            b = f.read(1)
            if not b:
                break
            if b != b"\xff":
                continue
            marker = f.read(1)
            if not marker:
                break
            while marker == b"\xff":
                marker = f.read(1)
            if marker[0] in (0xC0, 0xC1, 0xC2):
                f.read(3)  # length + precision
                height, width = struct.unpack(">HH", f.read(4))
                return width, height
            if marker[0] == 0xD9:
                break
            if marker[0] in range(0xD0, 0xD8) or marker[0] == 0x01:
                continue
            length_bytes = f.read(2)
            if len(length_bytes) < 2:
                break
            length = struct.unpack(">H", length_bytes)[0]
            f.read(length - 2)
    return 512, 512


def _estimate_image_tokens(width: int, height: int) -> int:
    """Claude's formula: scale to fit 1568px max, then (w * h) / 750."""
    if width > IMAGE_MAX_DIMENSION or height > IMAGE_MAX_DIMENSION:
        scale = IMAGE_MAX_DIMENSION / max(width, height)
        width = int(width * scale)
        height = int(height * scale)
    return max(1, (width * height) // IMAGE_TOKEN_DIVISOR)


def _count_pdf_pages(file_path: Path) -> int:
    """Count PDF pages from /Type /Page entries in raw bytes."""
    raw = file_path.read_bytes()
    count = raw.count(b"/Type /Page") - raw.count(b"/Type /Pages")
    return max(1, count)


def _estimate_text_tokens(file_path: Path) -> int:
    """~4 characters per token (Anthropic heuristic)."""
    size = file_path.stat().st_size
    return max(1, size // CHARS_PER_TOKEN)


def estimate_attachment_tokens(attachment: Attachment, base_path: Path) -> int:
    """Estimate token count for a single attachment."""
    if attachment.type == "url":
        return 0

    file_path = base_path / attachment.path

    if attachment.type == "image":
        width, height = _get_image_dimensions(file_path)
        return _estimate_image_tokens(width, height)

    if attachment.type == "document":
        pages = _count_pdf_pages(file_path)
        return pages * PDF_TOKENS_PER_PAGE

    # text, code, openapi — all text-based
    return _estimate_text_tokens(file_path)


def estimate_attachment_cost(
    attachments: list[Attachment],
    base_path: Path,
    model: str = DEFAULT_MODEL,
) -> dict[str, Any]:
    """Estimate token cost for all attachments before generation.

    Uses real Anthropic pricing from PRICING_REGISTRY.
    """
    input_price = PRICING_REGISTRY.get(model, PRICING_REGISTRY[DEFAULT_MODEL])["input"]
    details = []
    total_tokens = 0

    for att in attachments:
        tokens = estimate_attachment_tokens(att, base_path)
        total_tokens += tokens
        details.append({
            "path": att.path,
            "type": att.type,
            "estimated_tokens": tokens,
        })

    cost_usd = total_tokens * input_price / 1_000_000

    return {
        "attachments": details,
        "total_estimated_tokens": total_tokens,
        "estimated_cost_usd": round(cost_usd, 6),
        "model": model,
        "price_per_mtok": input_price,
    }
