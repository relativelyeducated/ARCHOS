"""
Basic Usage Examples for Moonshot Kimi K2 Provider

This script demonstrates how to use the Kimi K2 API through the MoonshotProvider class.

Before running:
1. Set your API key: export MOONSHOT_API_KEY="your-api-key-here"
2. Install dependencies: pip install openai
3. Run: python basic_usage.py
"""

import sys
import os

# Add parent directory to path to import ai_providers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from moonshot_provider import MoonshotProvider
from config import KIMI_K2_INSTRUCT


def example_simple_completion():
    """Example 1: Simple text completion"""
    print("=" * 60)
    print("Example 1: Simple Text Completion")
    print("=" * 60)

    # Initialize provider (will read MOONSHOT_API_KEY from environment)
    provider = MoonshotProvider(model="moonshot-v1-128k")

    # Validate credentials
    if not provider.validate_credentials():
        print("ERROR: Invalid API credentials. Please check your MOONSHOT_API_KEY.")
        return

    # Get a simple completion
    response = provider.get_completion(
        prompt="What is the significance of the DFA (Dialectical Fractal Archestructure) theory in understanding complex systems?",
        system_prompt="You are Kimi, an AI assistant specializing in systems theory and complexity science.",
        temperature=0.6,
        max_tokens=512
    )

    print(f"\nResponse:\n{response}\n")


def example_chat_conversation():
    """Example 2: Multi-turn chat conversation"""
    print("=" * 60)
    print("Example 2: Multi-turn Chat Conversation")
    print("=" * 60)

    provider = MoonshotProvider()

    messages = [
        {
            "role": "system",
            "content": "You are Kimi, an AI assistant created by Moonshot AI."
        },
        {
            "role": "user",
            "content": "Can you explain what makes you different from other language models?"
        }
    ]

    response = provider.get_chat_completion(
        messages=messages,
        temperature=0.6,
        max_tokens=512
    )

    print(f"\nKimi: {response}\n")


def example_tool_calling():
    """Example 3: Tool/function calling"""
    print("=" * 60)
    print("Example 3: Tool Calling (Function Calling)")
    print("=" * 60)

    provider = MoonshotProvider()

    # Define available tools
    tools = [
        {
            "type": "function",
            "function": {
                "name": "calculate_correlation_dimension",
                "description": "Calculate the correlation dimension (D2) of a dataset using the Grassberger-Procaccia algorithm.",
                "parameters": {
                    "type": "object",
                    "required": ["data_points", "embedding_dimension"],
                    "properties": {
                        "data_points": {
                            "type": "array",
                            "description": "Array of numerical data points for analysis"
                        },
                        "embedding_dimension": {
                            "type": "integer",
                            "description": "Embedding dimension for phase space reconstruction"
                        },
                        "min_scale": {
                            "type": "number",
                            "description": "Minimum scale for D2 calculation"
                        },
                        "max_scale": {
                            "type": "number",
                            "description": "Maximum scale for D2 calculation"
                        }
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "fetch_protein_structure",
                "description": "Fetch protein structure from PDB database",
                "parameters": {
                    "type": "object",
                    "required": ["pdb_id"],
                    "properties": {
                        "pdb_id": {
                            "type": "string",
                            "description": "PDB identifier (e.g., '1ABC')"
                        }
                    }
                }
            }
        }
    ]

    messages = [
        {
            "role": "user",
            "content": "I need to analyze the correlation dimension of a time series dataset with 1000 points and then fetch the protein structure 6XYZ from PDB. Can you help?"
        }
    ]

    response = provider.get_tool_completion(
        messages=messages,
        tools=tools,
        temperature=0.6,
        tool_choice="auto"
    )

    print(f"\nResponse content: {response['content']}")
    if response['tool_calls']:
        print(f"\nTool calls requested:")
        for tool_call in response['tool_calls']:
            print(f"  - {tool_call['function']['name']}")
            print(f"    Arguments: {tool_call['function']['arguments']}")
    print()


def example_streaming_response():
    """Example 4: Streaming responses"""
    print("=" * 60)
    print("Example 4: Streaming Response")
    print("=" * 60)

    provider = MoonshotProvider()

    messages = [
        {
            "role": "user",
            "content": "Write a short poem about fractals and self-similarity in nature."
        }
    ]

    print("\nStreaming response:\n")
    for chunk in provider.stream_completion(messages=messages, max_tokens=256):
        print(chunk, end='', flush=True)
    print("\n")


def example_model_info():
    """Example 5: Get model information"""
    print("=" * 60)
    print("Example 5: Model Information")
    print("=" * 60)

    provider = MoonshotProvider(model="moonshot-v1-128k")
    info = provider.get_model_info()

    print(f"\nModel Information:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    print()


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("Moonshot Kimi K2 Provider - Usage Examples")
    print("=" * 60 + "\n")

    try:
        # Check if API key is set
        if not os.getenv("MOONSHOT_API_KEY"):
            print("ERROR: MOONSHOT_API_KEY environment variable not set.")
            print("\nPlease set your API key:")
            print("  export MOONSHOT_API_KEY='your-api-key-here'")
            print("\nGet your API key at: https://platform.moonshot.ai")
            return

        # Run examples
        example_model_info()
        example_simple_completion()
        example_chat_conversation()
        example_tool_calling()
        example_streaming_response()

        print("=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nPlease check:")
        print("  1. MOONSHOT_API_KEY is set correctly")
        print("  2. You have internet connectivity")
        print("  3. Your API key has sufficient quota")


if __name__ == "__main__":
    main()
