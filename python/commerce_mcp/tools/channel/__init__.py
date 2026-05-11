from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_channel, read_channel, update_channel
from .prompts import CREATE_CHANNEL_PROMPT, READ_CHANNEL_PROMPT, UPDATE_CHANNEL_PROMPT
from .schemas import CreateChannelParams, ReadChannelParams, UpdateChannelParams

_CHANNEL_TOOLS = [
    ToolDefinition(
        method="read_channel",
        name="Read Channel",
        description=READ_CHANNEL_PROMPT,
        parameters=ReadChannelParams,
        handler=read_channel,
        actions={"channel": {"read": True}},
    ),
    ToolDefinition(
        method="create_channel",
        name="Create Channel",
        description=CREATE_CHANNEL_PROMPT,
        parameters=CreateChannelParams,
        handler=create_channel,
        actions={"channel": {"create": True}},
    ),
    ToolDefinition(
        method="update_channel",
        name="Update Channel",
        description=UPDATE_CHANNEL_PROMPT,
        parameters=UpdateChannelParams,
        handler=update_channel,
        actions={"channel": {"update": True}},
    ),
]

for _tool in _CHANNEL_TOOLS:
    register_tool(_tool)
