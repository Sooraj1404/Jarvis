from pathlib import Path

from tools.base import Tool
from tools.filesystem import FileSystemPolicy
from tools.result import ToolResult


class DeleteFileTool(Tool):
    name = "delete_file"
    description = "Delete an approved file."

    def __init__(self):
        self.policy = FileSystemPolicy()

    def execute(self, path: str = "", **kwargs) -> ToolResult:
        if not path.strip():
            return ToolResult.error(
                "No file path was specified."
            )

        file_path = Path(path.strip())

        valid, error, target = self.policy.validate_path(
            str(file_path)
        )

        if not valid:
            return ToolResult.error(error)

        if not target.exists():
            return ToolResult.error(
                f"File does not exist: '{path}'."
            )

        if not target.is_file():
            return ToolResult.error(
                f"Path is not a file: '{path}'."
            )

        try:
            target.unlink()

            return ToolResult.ok(
                f"Deleted file '{target}'.",
                {
                    "path": str(target.resolve()),
                },
            )

        except OSError as exc:
            return ToolResult.error(
                f"Unable to delete file '{path}': {exc}"
            )