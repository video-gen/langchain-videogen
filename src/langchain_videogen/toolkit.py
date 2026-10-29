"""Factory and toolkit for the VideoGen LangChain integration."""

from __future__ import annotations

from typing import Iterable, List, Optional

from langchain_core.tools import BaseTool, BaseToolkit
from pydantic import ConfigDict, Field
from videogen import VideoGen

from .client import resolve_client
from .operations import Controls
from .tools import build_videogen_tools


def create_videogen_tools(
    client: Optional[VideoGen] = None,
    *,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    wait: bool = True,
    poll_interval_ms: Optional[int] = None,
    timeout_ms: Optional[int] = None,
    include: Optional[Iterable[str]] = None,
) -> List[BaseTool]:
    """Build VideoGen tools in LangChain format, ready to bind to any LangChain or LangGraph agent.

    Args:
        client: A pre-configured ``VideoGen`` client. When omitted, one is built
            from ``api_key`` / ``base_url`` or the ``VIDEOGEN_API_KEY`` environment variable.
        wait: When True (default), tools block until the workflow run or tool execution
            finishes and return the completed result. Set False to return immediately
            with the run/execution id for the caller to poll.
        poll_interval_ms: Poll interval while waiting. Defaults to the SDK's default.
        timeout_ms: Maximum time to wait before giving up. Defaults to the SDK's default.
        include: Restrict the returned tool set to these tool names. Defaults to all tools.
    """
    resolved_client = resolve_client(client, api_key=api_key, base_url=base_url)
    controls = Controls(wait=wait, poll_interval_ms=poll_interval_ms, timeout_ms=timeout_ms)

    tools = build_videogen_tools(resolved_client, controls)

    if include is None:
        return tools

    included = set(include)
    return [tool for tool in tools if tool.name in included]


class VideoGenToolkit(BaseToolkit):
    """A LangChain toolkit exposing the VideoGen tools.

    Example:
        >>> toolkit = VideoGenToolkit.from_client()
        >>> tools = toolkit.get_tools()
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    videogen_tools: List[BaseTool] = Field(default_factory=list)

    def get_tools(self) -> List[BaseTool]:
        return self.videogen_tools

    @classmethod
    def from_client(
        cls,
        client: Optional[VideoGen] = None,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        wait: bool = True,
        poll_interval_ms: Optional[int] = None,
        timeout_ms: Optional[int] = None,
        include: Optional[Iterable[str]] = None,
    ) -> "VideoGenToolkit":
        return cls(
            videogen_tools=create_videogen_tools(
                client,
                api_key=api_key,
                base_url=base_url,
                wait=wait,
                poll_interval_ms=poll_interval_ms,
                timeout_ms=timeout_ms,
                include=include,
            )
        )
