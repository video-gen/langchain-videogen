# langchain-videogen

Official [LangChain](https://python.langchain.com) tools for the [VideoGen API](https://docs.videogen.io). Give any LangChain or LangGraph agent the ability to turn a script into a finished narrated video, plus generate standalone images, video clips, voiceovers, sound effects, music, and talking-head avatars.

Every tool wraps the official [`videogen`](https://pypi.org/project/videogen/) SDK and runs as the team that owns your API key.

## Install

```bash
pip install langchain-videogen
```

## Setup

Get an API key from [app.videogen.io/api](https://app.videogen.io/api) and set it as `VIDEOGEN_API_KEY`:

```bash
export VIDEOGEN_API_KEY="your_api_key"
```

## Usage

```python
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langchain_videogen import create_videogen_tools

tools = create_videogen_tools()

agent = create_react_agent(init_chat_model("openai:gpt-4o"), tools)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Make a short narrated video about why hydration matters."}]}
)
print(result["messages"][-1].content)
```

By default each tool blocks until the workflow or tool execution finishes and returns the completed result.

## Options

```python
from videogen import VideoGen
from langchain_videogen import create_videogen_tools, VideoGenToolkit

tools = create_videogen_tools(
    # Provide a pre-configured client, or pass api_key / base_url, or rely on env.
    client=VideoGen(api_key="your_api_key"),

    # Return the run/execution id immediately instead of waiting.
    wait=False,

    # Only expose a subset of tools to the model.
    include=["script_to_video", "generate_image", "text_to_speech"],
)

# Or use the toolkit:
toolkit = VideoGenToolkit.from_client()
tools = toolkit.get_tools()
```

| Option | Default | Description |
| --- | --- | --- |
| `client` | — | A pre-configured `VideoGen` client. |
| `api_key` | `VIDEOGEN_API_KEY` | API key used to build a client when `client` is omitted. |
| `base_url` | `VIDEOGEN_BASE_URL` or production | Override the API base URL. |
| `wait` | `True` | Block until the operation finishes and return the result. |
| `poll_interval_ms` | SDK default | Poll interval while waiting. |
| `timeout_ms` | SDK default | Maximum time to wait before giving up. |
| `include` | all tools | Restrict the returned tool set to these tool names. |

## Tools

<!-- BEGIN GENERATED PYTHON AGENT TOOLS -->
- Workflows: `cancel_workflow_run`, `get_workflow_run`, `list_workflow_runs`, `prompt_to_video_clip`, `script_to_video`, `slideshow_to_video`, `storyboard_to_video`, `video_to_video`, `voiceover_to_video`.
- Media generation: `cancel_tool_execution`, `generate_avatar`, `generate_image`, `generate_motion_graphic`, `generate_music`, `generate_sound_effect`, `generate_video_clip`, `get_tool_execution`, `image_3d_effect`, `list_tool_executions`, `remove_image_background`, `remove_video_background`, `text_to_speech`, `upscale_image`, `upscale_video`, `vectorize_image`.
- Projects: `export_project`, `get_project`, `list_project_remix_actions`, `list_projects`, `remix_project`.
- Files: `get_file`, `list_files`, `upload_file`.
- Resources and account: `get_me`, `list_languages`, `list_tts_voices`.

Avatar generation and supported video workflows use reusable actor entities. Pass `actor_entity_id` and set `avatar_quality` to `LOW`, `STANDARD`, `HIGH`, or `MAX`. Narrator changes are passed in `remix_actions` as `CHANGE_NARRATOR` action dictionaries.
<!-- END GENERATED PYTHON AGENT TOOLS -->

## Documentation

- [Use with AI agents](https://docs.videogen.io/use-with-ai-agents)
- [MCP server](https://docs.videogen.io/libraries/mcp)
- [API reference](https://docs.videogen.io)

## License

MIT

## Account and tool permissions

Generation uses your VideoGen account credits. Obtain user approval before invoking generation, editing or export tools. Start with a restricted `include` list when an agent only needs read access. File upload tools send the selected file to VideoGen; keep API keys in server-side environment variables and never place them in shared agent transcripts.

For a credential-free smoke check, build the tools with a synthetic key without invoking them. The package tests mock or avoid external calls; they do not prove paid generation.

[VideoGen](https://videogen.io/) · [MCP setup](https://videogen.io/videogen-mcp)

## 2.5.4

Fix polling after workflow, media-tool and export starts to use the Python SDK’s normalized response keys. No API capabilities or dependency requirements changed.
