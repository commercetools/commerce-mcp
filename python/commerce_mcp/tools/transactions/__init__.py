from __future__ import annotations

from ..registry import ToolDefinition, register_tool
from .functions import create_transaction, read_transaction
from .schemas import CreateTransactionParams, ReadTransactionParams
from .prompts import CREATE_TRANSACTION_PROMPT, READ_TRANSACTION_PROMPT

_TRANSACTIONS_TOOLS = [
    ToolDefinition(
        method="read_transaction",
        name="Read Transaction",
        description=READ_TRANSACTION_PROMPT,
        parameters=ReadTransactionParams,
        handler=read_transaction,
        actions={"transactions": {"read": True}},
    ),
    ToolDefinition(
        method="create_transaction",
        name="Create Transaction",
        description=CREATE_TRANSACTION_PROMPT,
        parameters=CreateTransactionParams,
        handler=create_transaction,
        actions={"transactions": {"create": True}},
    ),
]

for _tool in _TRANSACTIONS_TOOLS:
    register_tool(_tool)
