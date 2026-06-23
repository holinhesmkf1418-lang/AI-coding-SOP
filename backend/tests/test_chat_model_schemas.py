from datetime import datetime
from types import SimpleNamespace
from uuid import uuid4

import pytest
from pydantic import ValidationError

from backend.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ModelConfigCreate,
    ModelConfigResponse,
    ModelConfigStatus,
    UsageStatsResponse,
)


def test_chat_request_uses_stream_by_default() -> None:
    model_id = uuid4()
    request = ChatRequest(
        model_id=model_id,
        messages=[{"role": "user", "content": "你好"}],
    )

    assert request.model_id == model_id
    assert request.messages[0].role == "user"
    assert request.stream is True


def test_chat_response_requires_token_usage_keys() -> None:
    response = ChatResponse(
        content="ok",
        model="configured-model",
        usage={"input_tokens": 10, "output_tokens": 20},
    )

    assert response.usage["input_tokens"] == 10

    with pytest.raises(ValidationError):
        ChatResponse(
            content="ok",
            model="configured-model",
            usage={"input_tokens": 10},
        )


def test_model_config_create_defaults_daily_limit_to_zero() -> None:
    config = ModelConfigCreate(
        provider="provider-a",
        model_name="model-a",
        api_url="https://example.test/chat",
        api_key="1234567890abcdef",
    )

    assert config.daily_limit == 0


def test_model_config_response_masks_api_key_and_omits_plaintext() -> None:
    response = ModelConfigResponse.model_validate(
        SimpleNamespace(
            id=uuid4(),
            provider="provider-a",
            model_name="model-a",
            api_url="https://example.test/chat",
            api_key="1234567890abcdef",
            is_active=True,
            daily_limit=100,
            created_at=datetime.utcnow(),
        )
    )

    dumped = response.model_dump()

    assert response.api_key_masked == "1234***cdef"
    assert "api_key" not in dumped


def test_model_config_status_records_configured_providers() -> None:
    status = ModelConfigStatus(
        has_configured=True,
        configured_providers=["provider-a", "provider-b"],
    )

    assert status.configured_providers == ["provider-a", "provider-b"]


def test_usage_stats_response_computes_warning_from_usage_percent() -> None:
    response = UsageStatsResponse(
        models=[
            {
                "provider": "provider-a",
                "model_name": "model-a",
                "today_calls": 3,
                "today_tokens": 100,
                "daily_limit": 1000,
                "usage_percent": 80,
            },
            {
                "provider": "provider-b",
                "model_name": "model-b",
                "today_calls": 4,
                "today_tokens": 900,
                "daily_limit": 1000,
                "usage_percent": 90,
            },
        ]
    )

    assert response.models[0].warning is False
    assert response.models[1].warning is True
