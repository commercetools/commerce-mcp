"""Tests for FieldFilteringHandler — mirrors processors/test/field-filtering/ in TypeScript."""
import pytest
from commerce_mcp.config import FieldFilteringConfig
from commerce_mcp.shared.field_filtering import FieldFilteringHandler


def test_filter_path_removes_field():
    cfg = FieldFilteringConfig(filter_paths=["secret"])
    handler = FieldFilteringHandler(cfg)
    result = handler.process({"id": "1", "secret": "hidden"})
    assert "secret" not in result
    assert result["id"] == "1"


def test_redact_path_replaces_value():
    cfg = FieldFilteringConfig(redact_paths=["password"])
    handler = FieldFilteringHandler(cfg)
    result = handler.process({"password": "super-secret", "id": "1"})
    assert result["password"] == "[REDACTED]"
    assert result["id"] == "1"


def test_filter_nested_path():
    cfg = FieldFilteringConfig(filter_paths=["credentials.token"])
    handler = FieldFilteringHandler(cfg)
    result = handler.process({"credentials": {"token": "abc", "type": "Bearer"}})
    assert "token" not in result["credentials"]
    assert result["credentials"]["type"] == "Bearer"


def test_whitelist_overrides_filter():
    cfg = FieldFilteringConfig(
        filter_paths=["data"],
        whitelist_paths=["publicData"],
    )
    handler = FieldFilteringHandler(cfg)
    result = handler.process({"data": "filtered", "publicData": "kept"})
    assert "data" not in result
    assert result.get("publicData") == "kept"


def test_filter_property_removes_key_everywhere():
    cfg = FieldFilteringConfig(filter_properties=["internalId"])
    handler = FieldFilteringHandler(cfg)
    data = {"id": "1", "internalId": "secret", "nested": {"internalId": "also-secret"}}
    result = handler.process(data)
    assert "internalId" not in result
    assert "internalId" not in result["nested"]


def test_case_insensitive_matching():
    cfg = FieldFilteringConfig(filter_paths=["SECRET"], case_sensitive=False)
    handler = FieldFilteringHandler(cfg)
    result = handler.process({"secret": "hidden", "id": "1"})
    assert "secret" not in result
