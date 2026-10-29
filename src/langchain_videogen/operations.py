# AUTO-GENERATED from api/integrations/python-agent-templates/operations.py. DO NOT EDIT.
"""Shared helpers for starting and polling VideoGen operations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional

from videogen import VideoGen
from videogen.poll_executed_tool import poll_executed_tool
from videogen.poll_project_export import poll_project_export
from videogen.poll_workflow_run import poll_workflow_run


@dataclass
class Controls:
    """How the tools handle asynchronous VideoGen operations."""

    wait: bool = True
    poll_interval_ms: Optional[int] = None
    timeout_ms: Optional[int] = None


def to_dict(obj: Any) -> Any:
    """Convert an SDK response model into a plain, JSON-serializable structure."""
    model_dump = getattr(obj, "model_dump", None)
    if callable(model_dump):
        return model_dump(mode="json")
    return obj


def drop_none(values: Dict[str, Any]) -> Dict[str, Any]:
    """Drop ``None``-valued keys so the SDK applies its own defaults."""
    return {key: value for key, value in values.items() if value is not None}


def _poll_kwargs(controls: Controls) -> Dict[str, int]:
    kwargs: Dict[str, int] = {}
    if controls.poll_interval_ms is not None:
        kwargs["poll_interval_ms"] = controls.poll_interval_ms
    if controls.timeout_ms is not None:
        kwargs["timeout_ms"] = controls.timeout_ms
    return kwargs


def run_workflow(
    client: VideoGen,
    controls: Controls,
    start: Callable[[], Any],
) -> Any:
    """Start a workflow and, unless ``wait`` is False, poll it to a terminal state."""
    started = start()
    if not controls.wait:
        return to_dict(started)

    run = poll_workflow_run(client, started["workflowRunId"], **_poll_kwargs(controls))
    return to_dict(run)


def run_tool(
    client: VideoGen,
    controls: Controls,
    start: Callable[[], Any],
) -> Any:
    """Start a media tool execution and, unless ``wait`` is False, poll it to a terminal state."""
    started = start()
    if not controls.wait:
        return to_dict(started)

    execution = poll_executed_tool(client, started["toolExecutionId"], **_poll_kwargs(controls))
    return to_dict(execution)


def run_export(
    client: VideoGen,
    controls: Controls,
    project_id: str,
    start: Callable[[], Any],
) -> Any:
    """Start a project export and, unless ``wait`` is False, poll until the download URL is ready."""
    started = start()
    if not controls.wait:
        return to_dict(started)

    project_export = poll_project_export(
        client, project_id, started["exportId"], **_poll_kwargs(controls)
    )
    return to_dict(project_export)
