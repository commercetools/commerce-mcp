"""Tests for transform_tool_output."""
import json
import pytest
from commerce_mcp.shared.transform import transform_tool_output


def test_returns_json_string():
    data = {"id": "123", "name": "Widget"}
    result = transform_tool_output(data)
    assert '"id": "123"' in result
    assert '"name": "Widget"' in result


def test_nested_dict():
    data = {"product": {"id": "p1", "slug": "widget"}}
    result = transform_tool_output(data)
    parsed = json.loads(result)
    assert parsed["product"]["id"] == "p1"


def test_list_of_dicts():
    data = [{"id": "1"}, {"id": "2"}]
    result = transform_tool_output(data)
    parsed = json.loads(result)
    assert len(parsed) == 2


def test_none_value():
    result = transform_tool_output(None)
    assert result == "null"


def test_non_serializable_type_uses_str_fallback():
    from datetime import datetime
    data = {"ts": datetime(2024, 1, 1)}
    result = transform_tool_output(data)
    assert "2024-01-01" in result
