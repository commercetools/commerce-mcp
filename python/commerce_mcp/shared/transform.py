from __future__ import annotations

import json
from typing import Any


def transform_tool_output(data: Any) -> str:
    return json.dumps(data, default=str, indent=2)
