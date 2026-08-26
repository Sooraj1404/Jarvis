from pathlib import Path

from tools.base import Tool
from tools.filesystem import FileSystemPolicy
from tools.result import ToolResult


class MoveFileTool(Tool):
    name = "move_file"
    description = "Move an approved file to another approved filesystem path."

    def __init__(self):
        self.policy = FileSystemPolicy()

    def execute(
        self,
        path: str = "",
        destination: str = "",
        **kwargs,
    ) -> ToolResult:

        if not path.strip():
            return ToolResult.error(
                "No file path was specified."
            )

        if not destination.strip():
            return ToolResult.error(
                "No destination path was specified."
            )

        # Validate source
        valid, error, source_path = self.policy.validate_path(path)

        if not valid:
            return ToolResult.error(error)

        if not source_path.exists():
            return ToolResult.error(
                f"File does not exist: '{path}'."
            )

        if not source_path.is_file():
            return ToolResult.error(
                f"Path is not a file: '{path}'."
            )

        # Validate destination
        valid, error, destination_path = self.policy.validate_path(
            destination
        )

        if not valid:
            return ToolResult.error(error)

        # Destination must not already exist
        if destination_path.exists():
            return ToolResult.error(
                f"Destination already exists: '{destination}'."
            )

        # Destination parent must exist
        if not destination_path.parent.exists():
            return ToolResult.error(
                f"Destination directory does not exist: "
                f"'{destination_path.parent}'."
            )

        if not destination_path.parent.is_dir():
            return ToolResult.error(
                f"Destination parent is not a directory: "
                f"'{destination_path.parent}'."
            )

        try:
            source_path.rename(destination_path)

            return ToolResult.ok(
                f"Moved '{source_path}' to '{destination_path}'.",
                {
                    "old_path": str(source_path),
                    "new_path": str(destination_path),
                },
            )

        except OSError as exc:
            return ToolResult.error(
                f"Unable to move file '{path}': {exc}"
            )