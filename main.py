from repilot.config import load_config
from repilot.llm.client import LLMClient
from repilot.llm.schemas import LLMRequest

def main()->None:
    print("="*40)
    print("RepoPilot - Day 1")
    print("=" * 40)
    print()

    config = load_config()

    llm = LLMClient(config.llm)

    user_input = input("You> ").strip()

    if not user_input:
        print("Input cannot be empty.")
        return

    request = LLMRequest(
        user_input=user_input,
        instructions=(
            "You are RepoPilot, a software engineering assistant. "
            "Answer clearly and concisely."
        ),
    )

    response = llm.generate(request)

    print()
    print("RepoPilot >")
    print(response.text)

    print()
    print("-" * 40)
    print(f"provider: {config.llm.provider}")
    print(f"model: {response.model}")

    if response.usage is not None:
        print(f"input tokens: {response.usage.input_tokens}")
        print(f"output tokens: {response.usage.output_tokens}")
        print(f"total tokens: {response.usage.total_tokens}")

if __name__ == "__main__":
    main()