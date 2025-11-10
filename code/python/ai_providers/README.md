# AI Providers for KINGARCHOS

This module provides a unified interface for interacting with AI language models from various providers, with initial support for **Moonshot AI's Kimi K2** models.

## Overview

The AI Providers module implements an abstraction layer that allows seamless integration with different AI model providers while maintaining a consistent API interface. This enables the KINGARCHOS project to leverage advanced language models for research assistance, code generation, and analysis tasks.

## Supported Providers

### Moonshot AI (Kimi K2)

- **Models**:
  - `moonshot-v1-8k` (8K context)
  - `moonshot-v1-32k` (32K context)
  - `moonshot-v1-128k` (128K context, recommended)
- **Features**:
  - OpenAI-compatible API
  - Up to 256K context support
  - Tool/function calling (200-300 sequential calls)
  - Streaming responses
  - Optimized for Chinese and English

## Installation

1. Install required dependencies:

```bash
pip install openai
```

2. Set up your API key:

```bash
export MOONSHOT_API_KEY="your-api-key-here"
```

Get your API key at: https://platform.moonshot.ai

## Quick Start

### Basic Usage

```python
from ai_providers import MoonshotProvider

# Initialize the provider
provider = MoonshotProvider(model="moonshot-v1-128k")

# Get a simple completion
response = provider.get_completion(
    prompt="Explain the concept of correlation dimension",
    temperature=0.6,
    max_tokens=512
)

print(response)
```

### Chat Conversation

```python
messages = [
    {"role": "system", "content": "You are a research assistant specializing in fractal analysis."},
    {"role": "user", "content": "What is the significance of D2 in complex systems?"}
]

response = provider.get_chat_completion(
    messages=messages,
    temperature=0.6,
    max_tokens=1024
)
```

### Tool Calling (Function Calling)

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate_d2",
            "description": "Calculate correlation dimension of a dataset",
            "parameters": {
                "type": "object",
                "required": ["data"],
                "properties": {
                    "data": {"type": "array", "description": "Data points"}
                }
            }
        }
    }
]

response = provider.get_tool_completion(
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

if response['tool_calls']:
    for call in response['tool_calls']:
        print(f"Function: {call['function']['name']}")
        print(f"Arguments: {call['function']['arguments']}")
```

### Streaming Responses

```python
messages = [{"role": "user", "content": "Explain DFA theory"}]

for chunk in provider.stream_completion(messages=messages):
    print(chunk, end='', flush=True)
```

## Architecture

### Base Provider (`base_provider.py`)

The `AIProvider` abstract base class defines the interface that all provider implementations must follow:

- `get_completion()` - Simple text completion
- `get_chat_completion()` - Multi-turn conversations
- `get_tool_completion()` - Function calling capability
- `validate_credentials()` - Check API key validity
- `get_model_info()` - Model metadata

### Moonshot Provider (`moonshot_provider.py`)

Implementation for Moonshot AI's Kimi K2 models using the OpenAI-compatible API.

**Key Features:**
- Automatic API key loading from environment
- Configurable base URL and model selection
- Full support for Kimi K2's capabilities
- Comprehensive error handling and logging

### Configuration (`config.py`)

Centralized configuration management with:
- `ModelProvider` enum for supported providers
- `ProviderConfig` dataclass for provider settings
- Predefined configurations for common use cases
- Automatic environment variable loading

## Examples

### 1. Basic Usage (`examples/basic_usage.py`)

Demonstrates core functionality:
- Simple completions
- Chat conversations
- Tool calling
- Streaming responses
- Model information

Run with:
```bash
python examples/basic_usage.py
```

### 2. DFA Analysis Assistant (`examples/dfa_analysis_assistant.py`)

Interactive AI assistant tailored for DFA research:
- Natural language queries about DFA theory
- Code generation for analysis tasks
- Research guidance and experiment design
- Context-aware multi-turn conversations

Run with:
```bash
python examples/dfa_analysis_assistant.py
```

## API Reference

### MoonshotProvider

```python
MoonshotProvider(
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    model: str = "moonshot-v1-128k"
)
```

**Parameters:**
- `api_key`: Moonshot API key (or set `MOONSHOT_API_KEY` env var)
- `base_url`: API base URL (default: `https://api.moonshot.cn/v1`)
- `model`: Model name (default: `moonshot-v1-128k`)

**Methods:**

#### `get_completion(prompt, system_prompt=None, temperature=0.6, max_tokens=2048, **kwargs)`

Get a text completion from the model.

**Returns:** String response

#### `get_chat_completion(messages, temperature=0.6, max_tokens=2048, **kwargs)`

Get a chat completion with conversation history.

**Parameters:**
- `messages`: List of `{"role": str, "content": str}` dicts

**Returns:** String response

#### `get_tool_completion(messages, tools, temperature=0.6, tool_choice="auto", **kwargs)`

Get a completion with function calling capability.

**Parameters:**
- `tools`: List of tool definitions
- `tool_choice`: `"auto"`, `"required"`, or specific tool name

**Returns:** Dict with `"content"` and `"tool_calls"` keys

#### `stream_completion(messages, temperature=0.6, max_tokens=2048, **kwargs)`

Stream response chunks as they arrive.

**Yields:** String chunks

#### `validate_credentials()`

Test if API credentials are valid.

**Returns:** Boolean

#### `get_model_info()`

Get model metadata.

**Returns:** Dict with model information

## Configuration

### Environment Variables

- `MOONSHOT_API_KEY`: Your Moonshot AI API key (required)

### Model Selection

Choose a model based on your context requirements:

| Model | Context | Best For |
|-------|---------|----------|
| `moonshot-v1-8k` | 8K tokens | Short conversations |
| `moonshot-v1-32k` | 32K tokens | Medium documents |
| `moonshot-v1-128k` | 128K tokens | Long documents, complex analysis |

### Temperature Settings

- **0.1-0.3**: Focused, deterministic (code generation)
- **0.6**: Balanced (recommended default)
- **0.8-1.0**: Creative, diverse outputs

## Integration with KINGARCHOS

### Use Cases

1. **Research Assistance**
   - Explain DFA concepts and mathematical foundations
   - Literature review and paper summarization
   - Hypothesis generation

2. **Code Generation**
   - Generate analysis scripts
   - Create visualization code
   - Implement mathematical algorithms

3. **Data Analysis**
   - Interpret correlation dimension results
   - Suggest statistical tests
   - Identify patterns in experimental data

4. **Documentation**
   - Generate code documentation
   - Write experiment protocols
   - Create educational materials

### Example Integration

```python
# In your analysis script
from ai_providers import MoonshotProvider

def analyze_with_ai_assistance():
    provider = MoonshotProvider()

    # Get AI interpretation of results
    results_summary = f"D2 values: {d2_results}, Variance: {variance}"

    interpretation = provider.get_completion(
        prompt=f"Interpret these correlation dimension results: {results_summary}",
        system_prompt="You are an expert in fractal analysis and DFA theory.",
        temperature=0.6
    )

    print(f"AI Interpretation:\n{interpretation}")
```

## Best Practices

1. **API Key Security**
   - Never hardcode API keys in source code
   - Use environment variables or secure key management
   - Don't commit `.env` files to version control

2. **Rate Limiting**
   - Implement exponential backoff for retries
   - Cache responses when appropriate
   - Use streaming for long outputs

3. **Error Handling**
   - Always validate credentials before making requests
   - Implement try-except blocks for API calls
   - Log errors for debugging

4. **Cost Optimization**
   - Choose appropriate model size for the task
   - Set reasonable `max_tokens` limits
   - Use lower temperatures for deterministic tasks

## Troubleshooting

### "Invalid API credentials"

- Check that `MOONSHOT_API_KEY` is set correctly
- Verify your API key at https://platform.moonshot.ai
- Ensure you have sufficient quota

### Connection errors

- Check internet connectivity
- Verify base URL is correct
- Try with a different network

### Import errors

- Ensure `openai` package is installed: `pip install openai`
- Check Python path includes the `ai_providers` directory

## Future Extensions

Planned additions:
- OpenAI provider (GPT-4, o1)
- Anthropic provider (Claude)
- Ollama provider (local models)
- Embedding generation
- Fine-tuning support
- Batch processing

## Contributing

When adding new providers:

1. Inherit from `AIProvider` base class
2. Implement all abstract methods
3. Add configuration to `config.py`
4. Create usage examples
5. Update this README

## License

This module is part of the KINGARCHOS project.

Copyright (c) 2025 The KINGARCHOS Project Contributors

## References

- Moonshot AI Platform: https://platform.moonshot.ai
- Kimi K2 Documentation: https://moonshotai.github.io/Kimi-K2/
- KINGARCHOS Project: https://github.com/relativelyeducated/KINGARCHOS

---

*Last updated: November 10, 2025*
