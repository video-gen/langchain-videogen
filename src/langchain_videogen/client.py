# AUTO-GENERATED from api/integrations/python-agent-templates/client.py. DO NOT EDIT.
"""Client resolution for the VideoGen LangChain integration."""

from __future__ import annotations

import os
from typing import Optional

from videogen import VideoGen

_DEFAULT_BASE_URL = "https://api.videogen.io"


def resolve_client(
    client: Optional[VideoGen] = None,
    *,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> VideoGen:
    """Resolve a VideoGen client from an explicit client, an explicit key, or the environment.

    Every tool call is authenticated as the team that owns the key.

    Args:
        client: A pre-configured ``VideoGen`` client. Used as-is when provided.
        api_key: API key. Falls back to the ``VIDEOGEN_API_KEY`` environment variable.
        base_url: API base URL. Falls back to ``VIDEOGEN_BASE_URL``, then production.
    """
    if client is not None:
        return client

    resolved_key = api_key or os.environ.get("VIDEOGEN_API_KEY")

    if resolved_key is None or resolved_key.strip() == "":
        raise ValueError(
            "No VideoGen API key found. Pass `client` or `api_key`, or set the "
            "VIDEOGEN_API_KEY environment variable. Create a key at "
            "https://app.videogen.io/api."
        )

    resolved_base_url = base_url or os.environ.get("VIDEOGEN_BASE_URL") or _DEFAULT_BASE_URL

    return VideoGen(
        api_key=resolved_key.strip(),
        base_url=resolved_base_url,
        client_id="langchain",
    )
