#!/usr/bin/env python3
"""
Analyze DFA Results with Kimi K2 Assistance

This script demonstrates how to use Kimi K2 to interpret correlation dimension
results from your DFA analysis.
"""

import sys
import numpy as np
sys.path.append('/home/user/KINGARCHOS/code/python')

from ai_providers import MoonshotProvider


def analyze_d2_results_with_ai(d2_values, dataset_description):
    """
    Use Kimi K2 to interpret correlation dimension results.

    Args:
        d2_values: Dict or list of D2 values
        dataset_description: Description of the dataset analyzed

    Returns:
        AI interpretation of the results
    """
    # Initialize Kimi K2
    kimi = MoonshotProvider(model="moonshot-v1-128k")

    # Validate credentials
    if not kimi.validate_credentials():
        print("ERROR: Invalid API key. Please set MOONSHOT_API_KEY environment variable.")
        return None

    # Construct the analysis prompt
    prompt = f"""I've calculated correlation dimensions (D2) for the following dataset:

Dataset: {dataset_description}
D2 Results: {d2_values}

Please provide:
1. Interpretation of these D2 values
2. What they indicate about system complexity
3. Comparison to expected values for similar systems
4. Potential implications for the DFA framework
5. Suggested follow-up analyses

Be specific and reference relevant literature where applicable."""

    system_prompt = """You are an expert in fractal analysis, correlation dimensions,
and the Dialectical Fractal Archestructure (DFA) theory. Provide scientifically
rigorous interpretations based on established research."""

    # Get AI interpretation
    print("Analyzing results with Kimi K2...")
    interpretation = kimi.get_completion(
        prompt=prompt,
        system_prompt=system_prompt,
        temperature=0.6,
        max_tokens=2048
    )

    return interpretation


def generate_analysis_code(task_description):
    """
    Use Kimi K2 to generate Python code for analysis tasks.

    Args:
        task_description: Description of the analysis task

    Returns:
        Generated Python code
    """
    kimi = MoonshotProvider()

    prompt = f"""Generate Python code for the following analysis task:

{task_description}

Requirements:
- Use NumPy and SciPy
- Include error handling
- Add inline comments
- Make it compatible with the KINGARCHOS project structure
- Follow scientific computing best practices

Provide only the code, no explanations."""

    code = kimi.get_completion(
        prompt=prompt,
        temperature=0.3,  # Lower temperature for more deterministic code
        max_tokens=2048
    )

    return code


def ask_research_question(question):
    """
    Ask Kimi K2 a research question about DFA theory.

    Args:
        question: Your research question

    Returns:
        AI response
    """
    kimi = MoonshotProvider()

    response = kimi.get_completion(
        prompt=question,
        system_prompt="You are an expert in DFA theory, fractal mathematics, and complex systems analysis.",
        temperature=0.6,
        max_tokens=1024
    )

    return response


# Example usage scenarios
if __name__ == "__main__":
    import os

    # Check API key
    if not os.getenv("MOONSHOT_API_KEY"):
        print("=" * 70)
        print("ERROR: MOONSHOT_API_KEY not set")
        print("=" * 70)
        print("\nPlease set your API key:")
        print("  export MOONSHOT_API_KEY='your-key-here'")
        print("\nGet your key at: https://platform.moonshot.ai")
        sys.exit(1)

    print("=" * 70)
    print("DFA Analysis with Kimi K2 - Usage Examples")
    print("=" * 70)

    # Example 1: Interpret D2 results
    print("\n[Example 1] Interpreting D2 Results")
    print("-" * 70)

    d2_results = {
        "protein_1ABC": 2.31,
        "protein_2DEF": 2.89,
        "protein_3GHI": 1.97
    }

    interpretation = analyze_d2_results_with_ai(
        d2_values=d2_results,
        dataset_description="Protein backbone atom coordinates from PDB structures"
    )

    if interpretation:
        print(f"\nAI Interpretation:\n{interpretation}\n")

    # Example 2: Ask a research question
    print("\n[Example 2] Research Question")
    print("-" * 70)

    question = "How does the correlation dimension relate to information content in biological macromolecules?"
    print(f"Question: {question}")

    answer = ask_research_question(question)
    print(f"\nAnswer:\n{answer}\n")

    # Example 3: Generate analysis code
    print("\n[Example 3] Generate Analysis Code")
    print("-" * 70)

    task = """Create a function that calculates the Lyapunov exponent for a time series
dataset and plots the results. Include error bars and statistical significance testing."""

    print(f"Task: {task}")
    print("\nGenerating code...\n")

    code = generate_analysis_code(task)
    print("Generated Code:")
    print("=" * 70)
    print(code)
    print("=" * 70)
