from tools.base import Tool
from tools.filesystem import FileSystemPolicy
from tools.result import ToolResult


class ReadFileTool(Tool):
    name = "read_file"
    description = "Read the contents of an approved text file."

    MAX_FILE_SIZE = 1 * 1024 * 1024  # 1 MB

    def __init__(self):
        self.policy = FileSystemPolicy()

    def execute(self, path: str = "", **kwargs) -> ToolResult:
        if not path.strip():
            return ToolResult.error(
                "No file path was specified."
            )

        valid, error, file_path = self.policy.validate_path(path)

        if not valid:
            return ToolResult.error(error)

        if not file_path.exists():
            return ToolResult.error(
                f"File does not exist: '{path}'."
            )

        if not file_path.is_file():
            return ToolResult.error(
                f"Path is not a file: '{path}'."
            )

        try:
            file_size = file_path.stat().st_size

            if file_size > self.MAX_FILE_SIZE:
                return ToolResult.error(
                    "File is too large to read. "
                    f"Maximum size is "
                    f"{self.MAX_FILE_SIZE // (1024 * 1024)} MB."
                )

            content = file_path.read_text(
                encoding="utf-8"
            )

            return ToolResult.ok(
                f"Read file '{file_path}'.",
                {
                    "path": str(file_path),
                    "content": content,
                    "size": file_size,
                },
            )

        except UnicodeDecodeError:
            return ToolResult.error(
                f"File is not a supported UTF-8 text file: '{path}'."
            )

        except OSError as exc:
            return ToolResult.error(
                f"Unable to read file '{path}': {exc}"
            )