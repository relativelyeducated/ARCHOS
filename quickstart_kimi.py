#!/usr/bin/env python3
"""
Quick Start Script for Kimi K2

The simplest way to test the Kimi K2 integration.
Just set your API key and run!
"""

import sys
import os

sys.path.append('/home/user/KINGARCHOS/code/python')

from ai_providers import MoonshotProvider


def main():
    print("\n" + "=" * 70)
    print("Kimi K2 Quick Start")
    print("=" * 70)

    # Check API key
    api_key = os.getenv("MOONSHOT_API_KEY")
    if not api_key:
        print("\n❌ MOONSHOT_API_KEY not set!")
        print("\nPlease run:")
        print('  export MOONSHOT_API_KEY="your-api-key-here"')
        print("\nGet your key at: https://platform.moonshot.ai")
        return

    # Initialize Kimi K2
    print("\n🚀 Initializing Kimi K2...")
    kimi = MoonshotProvider(model="moonshot-v1-128k")

    # Test credentials
    print("🔑 Validating API key...")
    if not kimi.validate_credentials():
        print("❌ Invalid API key. Please check your MOONSHOT_API_KEY.")
        return

    print("✅ API key valid!")

    # Show model info
    info = kimi.get_model_info()
    print(f"\n📊 Model Information:")
    print(f"   Provider: {info['provider']}")
    print(f"   Model: {info['model']}")
    print(f"   Context Length: {info['context_length']} tokens")
    print(f"   Tool Calling: {info['supports_tool_calling']}")

    # Simple test query
    print("\n💬 Testing with a simple query...")
    print("-" * 70)

    response = kimi.get_completion(
        prompt="In 2-3 sentences, explain what makes the Kimi K2 model unique.",
        temperature=0.6,
        max_tokens=256
    )

    print(f"\nKimi K2: {response}")
    print("-" * 70)

    print("\n✅ Success! Kimi K2 is working correctly.")
    print("\nNext steps:")
    print("  1. Try the interactive assistant:")
    print("     python code/python/ai_providers/examples/dfa_analysis_assistant.py")
    print("\n  2. Use in your scripts:")
    print("     python code/python/analyze_with_kimi.py")
    print("\n  3. Read the docs:")
    print("     code/python/ai_providers/README.md")
    print()


if __name__ == "__main__":
    main()
