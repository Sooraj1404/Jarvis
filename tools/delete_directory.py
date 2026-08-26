from tools.base import Tool
from tools.filesystem import FileSystemPolicy
from tools.result import ToolResult


class DeleteDirectoryTool(Tool):
    name = "delete_directory"
    description = "Delete an empty directory inside the approved filesystem."

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
            directory.rmdir()

            return ToolResult.ok(
                f"Deleted directory '{directory}'.",
                {
                    "path": str(directory),
                },
            )

        except OSError as exc:
            return ToolResult.error(
                f"Unable to delete directory '{path}': {exc}"
            )