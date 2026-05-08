from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Awaitable, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from ..config import Configuration

Handler = Callable[..., Awaitable[Any]]


@dataclass
class ToolDefinition:
    """Framework-agnostic tool descriptor.

    All toolkit adapters (fastMCP, LangChain, Anthropic SDK, Vercel AI SDK)
    consume this single definition and wrap it in their own format.
    """
    method: str
    name: str
    description: str
    parameters: type[BaseModel]
    handler: Handler
    actions: dict[str, dict[str, bool]] = field(default_factory=dict)


class Registry:
    """Holds all registered tool definitions for a given server instance.

    Use the module-level register_tool() / get_tools() helpers for the default
    global instance.  Pass an isolated Registry() into build_server() in tests
    to prevent cross-test bleed or to run two servers with different tool sets
    in the same process.
    """

    def __init__(self) -> None:
        self._tools: list[ToolDefinition] = []
        self._handlers: dict[str, Handler] = {}

    def register(self, tool: ToolDefinition) -> None:
        self._tools.append(tool)
        self._handlers[tool.method] = tool.handler

    def get_handlers(self) -> dict[str, Handler]:
        return self._handlers

    def get_tools(self, config: "Configuration") -> list[ToolDefinition]:
        _ensure_all_namespaces_imported()
        allowed: list[ToolDefinition] = []
        for tool in self._tools:
            if _is_allowed(tool, config):
                allowed.append(tool)
        for custom in config.custom_tools:
            allowed.append(
                ToolDefinition(
                    method=custom.method,
                    name=custom.name,
                    description=custom.description,
                    parameters=custom.parameters,
                    handler=custom.handler,
                    actions=custom.actions,
                )
            )
        return allowed


# ── Default global instance ───────────────────────────────────────────────────
# Namespace modules self-register here when their module is imported.

_default_registry = Registry()


def register_tool(tool: ToolDefinition) -> None:
    """Called by each namespace module to add its tool definitions."""
    _default_registry.register(tool)


def get_function_registry() -> dict[str, Handler]:
    return _default_registry.get_handlers()


def get_tools(config: "Configuration") -> list[ToolDefinition]:
    """Returns tools permitted by config.actions, plus any custom tools."""
    return _default_registry.get_tools(config)


def _is_allowed(tool: ToolDefinition, config: "Configuration") -> bool:
    if config.actions is None:
        return True  # no restriction → all tools available

    for namespace, perms in tool.actions.items():
        ns_actions = getattr(config.actions, namespace.replace("-", "_"), None)
        if ns_actions is None:
            ns_actions = getattr(config.actions, namespace, None)

        if ns_actions is None:
            return False

        for action, required in perms.items():
            if required and not getattr(ns_actions, action, False):
                return False
    return True


def _ensure_all_namespaces_imported() -> None:
    """Import every namespace package so their register_tool() calls run."""
    from . import (  # noqa: F401
        products,
        orders,
        carts,
        zones,
        channel,
        types,
        discount_code,
        extensions,
        inventory,
        reviews,
        subscriptions,
        transactions,
        standalone_price,
        payments,
        payment_methods,
        payment_intents,
        product_discount,
        product_selection,
        custom_objects,
        customer_group,
        bulk,
        product_search,
        customer,
        product_tailoring,
        project,
        tax_category,
        product_type,
        shipping_methods,
        recurring_orders,
        category,
        store,
        staged_quote,
        cart_discount,
        business_unit,
        shopping_lists,
        quote_request,
        quote,
    )
