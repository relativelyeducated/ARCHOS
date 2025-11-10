"""
DFA Analysis Assistant using Kimi K2

This script demonstrates how to use Kimi K2 as an intelligent assistant
for DFA (Dialectical Fractal Archestructure) analysis tasks.

Features:
- Natural language queries about DFA theory
- Assistance with correlation dimension calculations
- Help interpreting experimental results
- Code generation for analysis tasks
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from moonshot_provider import MoonshotProvider


class DFAAssistant:
    """Intelligent assistant for DFA research using Kimi K2"""

    def __init__(self):
        self.provider = MoonshotProvider(model="moonshot-v1-128k")
        self.conversation_history = []

        # System prompt tailored for DFA research
        self.system_prompt = """You are an expert AI assistant specializing in the Dialectical Fractal Archestructure (DFA) theory.

Your expertise includes:
- Understanding of fractal mathematics and correlation dimensions
- Knowledge of the DFA framework and its applications
- Familiarity with Python, NumPy, SciPy, and scientific computing
- Experience with protein structure analysis and systems biology
- Understanding of computational linguistics and semantic analysis

You help researchers by:
1. Explaining DFA concepts and mathematical foundations
2. Assisting with data analysis and correlation dimension calculations
3. Interpreting experimental results in the DFA framework
4. Generating Python code for analysis tasks
5. Suggesting research directions and experimental designs

Always provide clear, scientifically rigorous explanations with references to the theory when relevant."""

        self.conversation_history.append({
            "role": "system",
            "content": self.system_prompt
        })

    def ask(self, question: str, temperature: float = 0.6) -> str:
        """
        Ask the assistant a question about DFA research.

        Args:
            question: The question to ask
            temperature: Sampling temperature (0.6 recommended for balanced responses)

        Returns:
            The assistant's response
        """
        # Add user question to history
        self.conversation_history.append({
            "role": "user",
            "content": question
        })

        # Get response
        response = self.provider.get_chat_completion(
            messages=self.conversation_history,
            temperature=temperature,
            max_tokens=4096
        )

        # Add response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })

        return response

    def clear_history(self):
        """Clear conversation history (keeping system prompt)"""
        self.conversation_history = [self.conversation_history[0]]

    def get_code_suggestion(self, task_description: str) -> str:
        """
        Get Python code suggestions for a specific analysis task.

        Args:
            task_description: Description of the coding task

        Returns:
            Python code suggestion
        """
        prompt = f"""Generate clean, well-documented Python code for the following task:

{task_description}

Requirements:
- Use NumPy, SciPy, and standard scientific libraries
- Include inline comments explaining the logic
- Follow best practices for scientific computing
- Make the code modular and reusable

Provide only the code without additional explanation."""

        return self.ask(prompt, temperature=0.3)  # Lower temp for code


def interactive_session():
    """Run an interactive Q&A session with the DFA assistant"""
    print("=" * 70)
    print("DFA Research Assistant (Powered by Kimi K2)")
    print("=" * 70)
    print("\nType your questions about DFA theory, analysis methods, or")
    print("experimental results. Type 'quit' to exit, 'clear' to reset,")
    print("or 'code: <task>' to get code suggestions.\n")

    assistant = DFAAssistant()

    print("Assistant ready! Ask me anything about DFA research.\n")

    while True:
        try:
            question = input("You: ").strip()

            if not question:
                continue

            if question.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break

            if question.lower() == 'clear':
                assistant.clear_history()
                print("\nConversation history cleared.\n")
                continue

            if question.lower().startswith('code:'):
                task = question[5:].strip()
                print("\nGenerating code...\n")
                response = assistant.get_code_suggestion(task)
            else:
                response = assistant.ask(question)

            print(f"\nKimi: {response}\n")

        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


def example_queries():
    """Run predefined example queries"""
    print("=" * 70)
    print("Example DFA Analysis Queries")
    print("=" * 70 + "\n")

    assistant = DFAAssistant()

    queries = [
        "What is the correlation dimension (D2) and why is it important in DFA theory?",
        "How do I interpret a D2 value of 2.3 for a protein structure dataset?",
        "What's the relationship between fractal dimension and information content in biological systems?",
        "Suggest an experimental design to validate DFA predictions in protein folding."
    ]

    for i, query in enumerate(queries, 1):
        print(f"Query {i}: {query}")
        print("-" * 70)
        response = assistant.ask(query)
        print(f"Response:\n{response}\n")
        print("=" * 70 + "\n")


def main():
    """Main entry point"""
    if not os.getenv("MOONSHOT_API_KEY"):
        print("ERROR: MOONSHOT_API_KEY environment variable not set.")
        print("\nPlease set your API key:")
        print("  export MOONSHOT_API_KEY='your-api-key-here'")
        return

    print("\nChoose mode:")
    print("  1. Interactive session")
    print("  2. Run example queries")
    print("  3. Both")

    choice = input("\nEnter choice (1-3): ").strip()

    if choice in ['2', '3']:
        example_queries()

    if choice in ['1', '3']:
        interactive_session()


if __name__ == "__main__":
    main()
