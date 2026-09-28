from repilot.config import load_config
from repilot.llm.client import LLMClient
from repilot.llm.schemas import LLMRequest
import json
from pathlib import Path
from repilot.tools.file_tools import(ListDirectoryTool)
from repilot.tools.registry import ToolRegistry

def build_tool_registry(repo_root:Path)->ToolRegistry:
    registry = ToolRegistry()

    registry.register(ListDirectoryTool(repo_root))

    return registry

def main()->None:
    print("="*40)
    print("RepoPilot - Day 2")
    print("=" * 40)
    print()

    config = load_config()

    llm = LLMClient(config.llm)

    repo_root = Path.cwd()

    registry = build_tool_registry(repo_root)

    user_input = input("You> ").strip()

    if not user_input:
        print("Input cannot be empty.")
        return

    request = LLMRequest(
        user_input=user_input,
        instructions=(
            "You are RepoPilot, a software "
            "engineering agent. "
            "Use the available tools when "
            "the user's request requires "
            "information from the repository. "
            "Do not invent repository contents."
        ),
        tools=registry.api_schemas(),
        tool_choice="auto"
    )

    response = llm.generate(request)

    print()
    if response.tool_calls:
        print("MODEL CHOSE TOOL")
        print("-" * 40)

        for tool_call in response.tool_calls:
            print(F"name:{tool_call.name}")
            print("arguments:")
            print(json.dumps(tool_call.arguments,indent=2,ensure_ascii=False))
            print()
            print("TOOL OBSERVATION")
            print("-" * 40)
            tool = registry.get(tool_call.name)
            try:
                observation = tool.execute(**tool_call.arguments)
            except Exception as exc:
                observation = (f"ERROR: " f"{type(exc).__name__}: " f"{exc}" )
            print(observation)
            print()

    else:
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