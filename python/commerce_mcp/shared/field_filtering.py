from __future__ import annotations

from typing import Any
from ..config import FieldFilteringConfig

_REDACTED = "[REDACTED]"


class FieldFilteringHandler:
    """Post-processes tool output by filtering or redacting fields.

    Mirrors the TypeScript FieldFilteringHandler behaviour.
    """

    def __init__(self, config: FieldFilteringConfig) -> None:
        self._config = config

    def process(self, data: Any) -> Any:
        return self._walk(data, path=[])

    def _walk(self, node: Any, path: list[str]) -> Any:
        if isinstance(node, dict):
            result: dict[str, Any] = {}
            for key, value in node.items():
                current_path = path + [key]
                dotted = ".".join(current_path)

                if self._should_filter_path(dotted) or self._should_filter_property(key):
                    continue

                if self._should_redact_path(dotted):
                    result[key] = _REDACTED
                else:
                    result[key] = self._walk(value, current_path)
            return result

        if isinstance(node, list):
            return [self._walk(item, path) for item in node]

        return node

    def _should_filter_path(self, path: str) -> bool:
        cfg = self._config
        for pattern in cfg.filter_paths + cfg.filter_includes:
            if self._match(path, pattern, cfg.case_sensitive):
                if not any(self._match(path, w, cfg.case_sensitive) for w in cfg.whitelist_paths):
                    return True
        return False

    def _should_redact_path(self, path: str) -> bool:
        return any(
            self._match(path, p, self._config.case_sensitive)
            for p in self._config.redact_paths
        )

    def _should_filter_property(self, key: str) -> bool:
        cfg = self._config
        return any(
            self._match(key, p, cfg.case_sensitive) for p in cfg.filter_properties
        )

    @staticmethod
    def _match(value: str, pattern: str, case_sensitive: bool) -> bool:
        if not case_sensitive:
            value, pattern = value.lower(), pattern.lower()
        return pattern in value
