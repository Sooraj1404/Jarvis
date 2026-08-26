from pathlib import Path

from tools.base import Tool
from tools.filesystem import FileSystemPolicy
from tools.result import ToolResult


class WriteFileTool(Tool):
    name = "write_file"
    description = "Overwrite an existing approved UTF-8 text file."

    MAX_FILE_SIZE = 1 * 1024 * 1024  # 1 MB

    def __init__(self):
        self.policy = FileSystemPolicy()

    def execute(
        self,
        path: str = "",
        content: str = "",
        **kwargs
    ) -> ToolResult:

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

        content_size = len(content.encode("utf-8"))

        if content_size > self.MAX_FILE_SIZE:
            return ToolResult.error(
                "Content is too large to write. "
                f"Maximum size is "
                f"{self.MAX_FILE_SIZE // (1024 * 1024)} MB."
            )

        try:
            target.write_text(
                content,
                encoding="utf-8",
            )

            return ToolResult.ok(
                f"Updated file '{target}'.",
                {
                    "path": str(target.resolve()),
                    "size": content_size,
                },
            )

        except OSError as exc:
            return ToolResult.error(
                f"Unable to write file '{path}': {exc}"
            )