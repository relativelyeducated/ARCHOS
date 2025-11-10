"""
AI Provider Abstraction Layer for KINGARCHOS

This module provides a unified interface for interacting with different
AI model providers including Moonshot AI (Kimi K2), OpenAI, Anthropic, etc.
"""

from .base_provider import AIProvider
from .moonshot_provider import MoonshotProvider
from .config import ProviderConfig, ModelProvider

__all__ = [
    'AIProvider',
    'MoonshotProvider',
    'ProviderConfig',
    'ModelProvider'
]

__version__ = '0.1.0'
