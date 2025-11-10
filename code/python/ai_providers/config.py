"""
Configuration management for AI providers.
"""

import os
from enum import Enum
from dataclasses import dataclass
from typing import Optional


class ModelProvider(Enum):
    """Supported AI model providers."""
    MOONSHOT = "moonshot"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"


@dataclass
class ProviderConfig:
    """
    Configuration for an AI provider.

    Attributes:
        provider: The model provider type
        api_key: API key for authentication (from environment or direct)
        model_name: Name of the specific model to use
        base_url: Base URL for API endpoint (optional)
        temperature: Default sampling temperature
        max_tokens: Default maximum tokens in response
    """
    provider: ModelProvider
    model_name: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.6
    max_tokens: int = 2048

    def __post_init__(self):
        """Load API key from environment if not provided."""
        if self.api_key is None:
            env_var_map = {
                ModelProvider.MOONSHOT: "MOONSHOT_API_KEY",
                ModelProvider.OPENAI: "OPENAI_API_KEY",
                ModelProvider.ANTHROPIC: "ANTHROPIC_API_KEY",
                ModelProvider.OLLAMA: None  # No key needed for local
            }
            env_var = env_var_map.get(self.provider)
            if env_var:
                self.api_key = os.getenv(env_var)

        # Set default base URLs if not provided
        if self.base_url is None:
            base_url_map = {
                ModelProvider.MOONSHOT: "https://api.moonshot.cn/v1",
                ModelProvider.OPENAI: "https://api.openai.com/v1",
                ModelProvider.ANTHROPIC: "https://api.anthropic.com",
                ModelProvider.OLLAMA: "http://localhost:11434",
            }
            self.base_url = base_url_map.get(self.provider)


# Predefined configurations for common use cases
KIMI_K2_INSTRUCT = ProviderConfig(
    provider=ModelProvider.MOONSHOT,
    model_name="moonshot-v1-128k",
    temperature=0.6,
    max_tokens=2048
)

KIMI_K2_THINKING = ProviderConfig(
    provider=ModelProvider.MOONSHOT,
    model_name="moonshot-v1-32k",
    temperature=0.6,
    max_tokens=4096
)
