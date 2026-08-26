from pathlib import Path

from tools.base import Tool
from tools.filesystem import FileSystemPolicy
from tools.result import ToolResult


class ListFilesTool(Tool):
    name = "list_files"
    description = "List files and directories in an approved filesystem path."

    def __init__(self):
        self.policy = FileSystemPolicy()

    def execute(self, path: str = "", **kwargs) -> ToolResult:
        if not path.strip():
            return ToolResult.error(
                "No directory path was specified."
            )

        valid, error, directory = self.policy.validate_path(path)

        if not valid:
            return ToolResult.error(error)

        if not directory.exists():
            return ToolResult.error(
                f"Directory does not exist: '{path}'."
            )

        if not directory.is_dir():
            return ToolResult.error(
                f"Path is not a directory: '{path}'."
            )

        try:
            entries = []

            for entry in sorted(
                directory.iterdir(),
                key=lambda item: item.name.lower(),
            ):
                entries.append(
                    {
                        "name": entry.name,
                        "type": "directory" if entry.is_dir() else "file",
                    }
                )

            return ToolResult.ok(
                f"Found {len(entries)} entries in '{directory}'.",
                {
                    "path": str(directory),
                    "entries": entries,
                },
            )

        except OSError as exc:
            return ToolResult.error(
                f"Unable to list directory '{path}': {exc}"
            )