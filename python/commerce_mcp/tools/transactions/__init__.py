from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_transaction, read_transaction
from .schemas import CreateTransactionParams, ReadTransactionParams

_TRANSACTIONS_TOOLS = [
    ToolDefinition(
        method="read_transaction",
        name="Read Transaction",
        description="Read or list checkout transactions. Provide an id or key to fetch a specific transaction, or omit both to list transactions.",
        parameters=ReadTransactionParams,
        handler=read_transaction,
        actions={"transactions": {"read": True}},
    ),
    ToolDefinition(
        method="create_transaction",
        name="Create Transaction",
        description="Create a new checkout transaction for a cart with a payment integration.",
        parameters=CreateTransactionParams,
        handler=create_transaction,
        actions={"transactions": {"create": True}},
    ),
]

for _tool in _TRANSACTIONS_TOOLS:
    register_tool(_tool)
