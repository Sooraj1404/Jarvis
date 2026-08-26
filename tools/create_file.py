from tools.base import Tool
from tools.filesystem import FileSystemPolicy
from tools.result import ToolResult


class CreateFileTool(Tool):
    name = "create_file"
    description = "Create a new UTF-8 text file in an approved filesystem path."

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

        file_path = path.strip()

        parent_path = str(
            __import__("pathlib").Path(file_path).parent
        )

        valid, error, parent = self.policy.validate_path(parent_path)

        if not valid:
            return ToolResult.error(error)

        target = parent / __import__("pathlib").Path(file_path).name

        if target.exists():
            return ToolResult.error(
                f"File already exists: '{file_path}'."
            )

        if not parent.exists():
            return ToolResult.error(
                f"Parent directory does not exist: '{parent_path}'."
            )

        if not parent.is_dir():
            return ToolResult.error(
                f"Parent path is not a directory: '{parent_path}'."
            )

        try:
            target.write_text(
                content,
                encoding="utf-8",
            )

            return ToolResult.ok(
                f"Created file '{target}'.",
                {
                    "path": str(target.resolve()),
                    "size": len(content.encode("utf-8")),
                },
            )

        except OSError as exc:
            return ToolResult.error(
                f"Unable to create file '{file_path}': {exc}"
            )