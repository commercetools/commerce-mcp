from __future__ import annotations


class ContextError(Exception):
    """Raised when a tool is called without the required CTContext scope.

    Mirrors the TypeScript behaviour where contextToXFunctionMapping returns {}
    when no valid context is set — the tool is simply not callable.
    """
    def __init__(self, tool: str, required: str) -> None:
        super().__init__(
            f"'{tool}' is not available in the current context. "
            f"Required: {required}."
        )


class SDKError(Exception):
    """Wraps Commercetools API errors with operation context."""

    def __init__(self, operation: str, error: Exception | None = None) -> None:
        detail = ""
        if error is not None:
            # Try to extract body from httpx or requests-style responses
            if hasattr(error, "response") and error.response is not None:  # type: ignore[union-attr]
                try:
                    body = error.response.json()  # type: ignore[union-attr]
                    errors = body.get("errors", [])
                    detail = "; ".join(
                        e.get("detailedErrorMessage") or e.get("message", "") for e in errors
                    )
                except Exception:
                    detail = str(error)
            else:
                detail = str(error)

        message = f"Failed to {operation}"
        if detail:
            message = f"{message}: {detail}"
        super().__init__(message)
