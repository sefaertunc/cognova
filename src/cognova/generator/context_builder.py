import base64
from pathlib import Path
from typing import Any

import yaml

from cognova.scenario.loader import Attachment, detect_language

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
