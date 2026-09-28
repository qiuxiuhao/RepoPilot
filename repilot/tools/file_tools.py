from pathlib import Path
from typing import Any

from repilot.tools.base import Tool

class ListDirectoryTool(Tool):
    name = "list_directory"

    description = (
        "List the direct children of a directory inside "
        "the target repository. Use this tool when you need "
        "to inspect the repository structure."
    )

    parameters = {
        "type":"object",
        "properties":{
            "path":{
                "type":"string",
                "description":(
                    "Directory path relative to the repository root. "
                    "Use '.' for the repository root."
                ),
            }
        },
        "required":["path"],
        "additionalProperties":False,
    }

    def __init__(self,root:str | Path):
        self.root = Path(root).resolve()

    def execute(self, **kwargs:Any)->str:
        path = kwargs.get("path")

        if not isinstance(path,str):
            raise ValueError(
                "The 'path' argument must be a string."
            )

        if not path.strip():
            raise ValueError(
                "The 'path' argument cannot be empty."
            )

        target = (
            self.root / path
        ).resolve()

        try:
            target.relative_to(self.root)
        except ValueError as exc:
            raise ValueError(
                "Path escapes the repository root."
            ) from exc

        if not target.exists():
            raise FileNotFoundError(
                f"Directory does not exist: {path}"
            )

        if not target.is_dir():
            raise NotADirectoryError(
                f"Path is not a directory: {path}"
            )

        entries = sorted(
            target.iterdir(),
            key = lambda item:(
                not item.is_dir(),
                item.name.lower(),
            ),
        )

        if not entries:
            return "(empty directory)"

        lines: list[str] = []

        for entry in entries:
            relative_path = entry.relative_to(self.root)

            if entry.is_dir():
                lines.append(f"{relative_path}/")
            else:
                lines.append(str(relative_path))

        return "\n".join(lines)
