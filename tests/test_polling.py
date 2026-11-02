"""Regression checks using actual SDK JSON response normalization, no network."""
import httpx
import pytest
from videogen import VideoGen
from langchain_videogen.operations import Controls, run_workflow, run_tool, run_export

@pytest.mark.parametrize("kind,id_key,start_path", [
    ("workflow", "workflowRunId", "/v1/workflows/storyboard-to-video"),
    ("tool", "toolExecutionId", "/v1/tools/generate-image"),
    ("export", "exportId", "/v1/projects/synthetic-project/exports"),
])
@pytest.mark.parametrize("wait", [True, False])
def test_sdk_normalized_start_response_polls(kind, id_key, start_path, wait):
    calls = []
    def handler(request):
        calls.append(request)
        if request.method == "POST":
            return httpx.Response(200, json={id_key: "synthetic-id"})
        return httpx.Response(200, json={"status": "succeeded", "downloadUrl": "https://example.invalid/result.mp4"})
    with httpx.Client(transport=httpx.MockTransport(handler)) as http:
        client = VideoGen(api_key="synthetic-only", base_url="https://example.invalid", http_client=http)
        controls = Controls(wait=wait)
        def start():
            return client.request(method="POST", path=start_path, body={})
        if kind == "workflow":
            result = run_workflow(client, controls, start)
        elif kind == "tool":
            result = run_tool(client, controls, start)
        else:
            result = run_export(client, controls, "synthetic-project", start)
    if wait:
        assert result["status"] == "succeeded"
        assert result["download_url"] == "https://example.invalid/result.mp4"
        assert len(calls) == 2
        assert "synthetic-id" in calls[1].url.path
    else:
        assert "synthetic-id" in result.values()
        assert len(calls) == 1
