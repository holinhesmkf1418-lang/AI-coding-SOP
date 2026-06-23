from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator, model_validator


REQUIRED_TOKEN_USAGE_KEYS = {"input_tokens", "output_tokens"}
API_KEY_VISIBLE_CHARS = 4
API_KEY_MASK = "***"
USAGE_WARNING_THRESHOLD = 80


def mask_api_key(api_key: str) -> str:
    if not api_key:
        return ""
    if len(api_key) <= API_KEY_VISIBLE_CHARS * 2:
        return API_KEY_MASK
    return f"{api_key[:API_KEY_VISIBLE_CHARS]}{API_KEY_MASK}{api_key[-API_KEY_VISIBLE_CHARS:]}"


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model_id: UUID
    messages: list[ChatMessage]
    stream: bool = True


class ChatResponse(BaseModel):
    content: str
    model: str
    usage: dict[str, int]

    @field_validator("usage")
    @classmethod
    def require_token_usage_keys(cls, usage: dict[str, int]) -> dict[str, int]:
        missing_keys = REQUIRED_TOKEN_USAGE_KEYS - set(usage)
        if missing_keys:
            raise ValueError("usage must include input_tokens and output_tokens")
        return usage


class ModelConfigCreate(BaseModel):
    provider: str
    model_name: str
    api_url: str
    api_key: str
    daily_limit: int = 0


class ModelConfigResponse(BaseModel):
    id: UUID
    provider: str
    model_name: str
    api_url: str
    api_key_masked: str
    is_active: bool
    daily_limit: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def build_masked_api_key(cls, data: Any) -> Any:
        response_fields = (
            "id",
            "provider",
            "model_name",
            "api_url",
            "is_active",
            "daily_limit",
            "created_at",
        )

        if isinstance(data, dict):
            values = dict(data)
            api_key = values.pop("api_key", None)
            encrypted_api_key = values.pop("api_key_encrypted", None)
        else:
            values = {
                field: getattr(data, field)
                for field in response_fields
                if hasattr(data, field)
            }
            api_key = getattr(data, "api_key", None)
            encrypted_api_key = getattr(data, "api_key_encrypted", None)
            if hasattr(data, "api_key_masked"):
                values["api_key_masked"] = getattr(data, "api_key_masked")

        if "api_key_masked" not in values:
            values["api_key_masked"] = mask_api_key(api_key or encrypted_api_key or "")
        return values


class ModelConfigStatus(BaseModel):
    has_configured: bool
    configured_providers: list[str]


class UsageModelStats(BaseModel):
    provider: str
    model_name: str
    today_calls: int
    today_tokens: int
    daily_limit: int
    usage_percent: float
    warning: bool = False

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def compute_warning(cls, data: Any) -> Any:
        fields = (
            "provider",
            "model_name",
            "today_calls",
            "today_tokens",
            "daily_limit",
            "usage_percent",
        )

        if isinstance(data, dict):
            values = dict(data)
        else:
            values = {
                field: getattr(data, field)
                for field in fields
                if hasattr(data, field)
            }

        usage_percent = values.get("usage_percent")
        if usage_percent is not None:
            values["warning"] = float(usage_percent) > USAGE_WARNING_THRESHOLD
        return values


class UsageStatsResponse(BaseModel):
    models: list[UsageModelStats]
