from tools.base import Tool
from tools.filesystem import FileSystemPolicy
from tools.result import ToolResult


class CreateDirectoryTool(Tool):
    name = "create_directory"
    description = "Create a directory inside the approved filesystem."

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

        if directory.exists():
            if directory.is_dir():
                return ToolResult.error(
                    f"Directory already exists: '{path}'."
                )

            return ToolResult.error(
                f"A file already exists at: '{path}'."
            )

        parent = directory.parent

        if not parent.exists():
            return ToolResult.error(
                f"Parent directory does not exist: '{parent}'."
            )

        if not parent.is_dir():
            return ToolResult.error(
                f"Parent path is not a directory: '{parent}'."
            )

        try:
            directory.mkdir()

            return ToolResult.ok(
                f"Created directory '{directory}'.",
                {
                    "path": str(directory),
                },
            )

        except OSError as exc:
            return ToolResult.error(
                f"Unable to create directory '{path}': {exc}"
            )