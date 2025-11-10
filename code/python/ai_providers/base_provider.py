"""
Base AI Provider Abstract Class

Defines the interface that all AI provider implementations must follow.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class AIProvider(ABC):
    """
    Abstract base class for AI model providers.

    All provider implementations must inherit from this class and implement
    the required abstract methods.
    """

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize the AI provider.

        Args:
            api_key: API key for authentication (can be None for local models)
            base_url: Base URL for the API endpoint (optional)
        """
        self.api_key = api_key
        self.base_url = base_url
        self.client = None

    @abstractmethod
    def get_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.6,
        max_tokens: int = 2048,
        **kwargs
    ) -> str:
        """
        Get a text completion from the AI model.

        Args:
            prompt: The user prompt/query
            system_prompt: Optional system prompt to set context
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in response
            **kwargs: Additional provider-specific parameters

        Returns:
            The model's response as a string
        """
        pass

    @abstractmethod
    def get_chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.6,
        max_tokens: int = 2048,
        **kwargs
    ) -> str:
        """
        Get a chat completion from the AI model.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in response
            **kwargs: Additional provider-specific parameters

        Returns:
            The model's response as a string
        """
        pass

    @abstractmethod
    def get_tool_completion(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]],
        temperature: float = 0.6,
        tool_choice: str = "auto",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get a completion with tool/function calling capability.

        Args:
            messages: List of message dicts with 'role' and 'content'
            tools: List of tool definitions
            temperature: Sampling temperature (0.0 to 1.0)
            tool_choice: How to use tools ("auto", "required", or specific tool)
            **kwargs: Additional provider-specific parameters

        Returns:
            Dict containing response and any tool calls
        """
        pass

    @abstractmethod
    def validate_credentials(self) -> bool:
        """
        Validate that the API credentials are working.

        Returns:
            True if credentials are valid, False otherwise
        """
        pass

    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the model being used.

        Returns:
            Dict containing model metadata (name, context length, etc.)
        """
        pass
