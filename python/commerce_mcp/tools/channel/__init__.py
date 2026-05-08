from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_channel, read_channel, update_channel
from .schemas import CreateChannelParams, ReadChannelParams, UpdateChannelParams

_CHANNEL_TOOLS = [
    ToolDefinition(
        method="read_channel",
        name="Read Channel",
        description="Read or list channels. Provide an id or key to fetch a specific channel, or omit both to list channels with optional filtering.",
        parameters=ReadChannelParams,
        handler=read_channel,
        actions={"channel": {"read": True}},
    ),
    ToolDefinition(
        method="create_channel",
        name="Create Channel",
        description="Create a new channel with a key, roles, optional localized name, description, address, and geo location.",
        parameters=CreateChannelParams,
        handler=create_channel,
        actions={"channel": {"create": True}},
    ),
    ToolDefinition(
        method="update_channel",
        name="Update Channel",
        description="Apply update actions to an existing channel identified by id or key.",
        parameters=UpdateChannelParams,
        handler=update_channel,
        actions={"channel": {"update": True}},
    ),
]

for _tool in _CHANNEL_TOOLS:
    register_tool(_tool)
