import re
from typing import Any

from repilot.tools.base import Tool

class ToolRegistry:
    _NAME_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")

    def __init__(self)->None:
        self._tools:dict[str,Tool] = {}

    def register(self,tool:Tool):
        if not tool.name:
            raise ValueError("Tool name cannot be empty.")
        
        if len(tool.name) > 128:
            raise ValueError(
                f"Tool name is too long: {tool.name}"
            )

        if self._NAME_PATTERN.fullmatch(tool.name) is None:
            raise ValueError(
                f"Invalid tool name: {tool.name}"
            )

        if tool.name in self._tools:
            raise ValueError(
                f"Tool already registered: {tool.name}"
            )

        self._tools[tool.name] = tool

    def get(self,name:str)->Tool:
        try:
            return self._tools[name]
        except KeyError as exc:
            raise KeyError(
                f"Unknown tool: {name}"
            ) from exc

    def api_schemas(self)->list[dict[str,Any]]:
        return [
            tool.to_api_schema()
            for tool in self._tools.values()
        ]

        