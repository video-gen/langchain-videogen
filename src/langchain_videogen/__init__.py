"""Official LangChain tools for the VideoGen API."""

from importlib.metadata import PackageNotFoundError, version

from .client import resolve_client
from .operations import Controls
from .toolkit import VideoGenToolkit, create_videogen_tools

__all__ = [
    "Controls",
    "VideoGenToolkit",
    "create_videogen_tools",
    "resolve_client",
]

try:
    __version__ = version("langchain-videogen")
except PackageNotFoundError:
    __version__ = "0.0.0"
