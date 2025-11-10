"""
Moonshot AI (Kimi K2) Provider Implementation

Provides integration with Moonshot AI's Kimi K2 models via OpenAI-compatible API.
"""

from typing import List, Dict, Any, Optional
from openai import OpenAI
import logging

from .base_provider import AIProvider


logger = logging.getLogger(__name__)


class MoonshotProvider(AIProvider):
    """
    Provider for Moonshot AI's Kimi K2 models.

    Uses OpenAI-compatible API at api.moonshot.cn
    Supports models: moonshot-v1-8k, moonshot-v1-32k, moonshot-v1-128k

    Temperature Note: Moonshot recommends temperature=0.6 for Kimi-K2-Instruct.
    For Anthropic-compatible usage: real_temperature = request_temperature * 0.6
    """

    DEFAULT_MODEL = "moonshot-v1-128k"
    DEFAULT_BASE_URL = "https://api.moonshot.cn/v1"

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: str = DEFAULT_MODEL
    ):
        """
        Initialize Moonshot provider.

        Args:
            api_key: Moonshot API key (or set MOONSHOT_API_KEY env var)
            base_url: API base URL (defaults to https://api.moonshot.cn/v1)
            model: Model name (moonshot-v1-8k, moonshot-v1-32k, moonshot-v1-128k)
        """
        super().__init__(api_key, base_url or self.DEFAULT_BASE_URL)
        self.model = model

        if not self.api_key:
            import os
            self.api_key = os.getenv("MOONSHOT_API_KEY")
            if not self.api_key:
                logger.warning(
                    "No API key provided. Set MOONSHOT_API_KEY environment variable "
                    "or pass api_key parameter."
                )

        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            logger.info(f"Initialized MoonshotProvider with model: {self.model}")
        else:
            logger.warning("MoonshotProvider initialized without API key")

    def get_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.6,
        max_tokens: int = 2048,
        **kwargs
    ) -> str:
        """
        Get a text completion from Kimi K2.

        Args:
            prompt: The user prompt/query
            system_prompt: Optional system prompt
            temperature: Sampling temperature (default 0.6 recommended)
            max_tokens: Maximum tokens in response
            **kwargs: Additional parameters

        Returns:
            The model's response as a string
        """
        if not self.client:
            raise ValueError("Client not initialized. Please provide API key.")

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        return self.get_chat_completion(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )

    def get_chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.6,
        max_tokens: int = 2048,
        **kwargs
    ) -> str:
        """
        Get a chat completion from Kimi K2.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (default 0.6 recommended)
            max_tokens: Maximum tokens in response
            **kwargs: Additional parameters

        Returns:
            The model's response as a string
        """
        if not self.client:
            raise ValueError("Client not initialized. Please provide API key.")

        logger.debug(f"Requesting chat completion with {len(messages)} messages")

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )

        return response.choices[0].message.content

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

        Kimi K2 supports up to 200-300 sequential tool calls.

        Args:
            messages: List of message dicts
            tools: List of tool definitions
            temperature: Sampling temperature (default 0.6)
            tool_choice: "auto", "required", or specific tool name
            **kwargs: Additional parameters

        Returns:
            Dict containing 'content' and 'tool_calls' (if any)
        """
        if not self.client:
            raise ValueError("Client not initialized. Please provide API key.")

        logger.debug(
            f"Requesting tool completion with {len(messages)} messages "
            f"and {len(tools)} tools"
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            tools=tools,
            tool_choice=tool_choice,
            **kwargs
        )

        message = response.choices[0].message
        result = {
            "content": message.content,
            "tool_calls": []
        }

        if hasattr(message, 'tool_calls') and message.tool_calls:
            result["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in message.tool_calls
            ]

        return result

    def validate_credentials(self) -> bool:
        """
        Validate that the API credentials are working.

        Returns:
            True if credentials are valid, False otherwise
        """
        if not self.client:
            return False

        try:
            # Make a minimal API call to test credentials
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            logger.error(f"Credential validation failed: {e}")
            return False

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current Kimi K2 model.

        Returns:
            Dict containing model metadata
        """
        context_lengths = {
            "moonshot-v1-8k": 8192,
            "moonshot-v1-32k": 32768,
            "moonshot-v1-128k": 131072,
        }

        return {
            "provider": "Moonshot AI",
            "model": self.model,
            "context_length": context_lengths.get(self.model, "Unknown"),
            "max_output_tokens": 8192,  # Standard, 16K for coding
            "supports_tool_calling": True,
            "supports_streaming": True,
            "recommended_temperature": 0.6,
            "description": "Kimi K2 - Trillion-parameter LLM with 256K context support"
        }

    def stream_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.6,
        max_tokens: int = 2048,
        **kwargs
    ):
        """
        Stream a chat completion from Kimi K2.

        Args:
            messages: List of message dicts
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            **kwargs: Additional parameters

        Yields:
            Chunks of the response as they arrive
        """
        if not self.client:
            raise ValueError("Client not initialized. Please provide API key.")

        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
            **kwargs
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
