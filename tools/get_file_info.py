from tools.base import Tool
from tools.filesystem import FileSystemPolicy
from tools.result import ToolResult


class GetFileInfoTool(Tool):
    name = "get_file_info"
    description = "Get metadata about an approved file or directory."

    def __init__(self):
        self.policy = FileSystemPolicy()

    def execute(self, path: str = "", **kwargs) -> ToolResult:
        if not path.strip():
            return ToolResult.error(
                "No path was specified."
            )

        valid, error, target = self.policy.validate_path(path)

        if not valid:
            return ToolResult.error(error)

        if not target.exists():
            return ToolResult.error(
                f"Path does not exist: '{path}'."
            )

        try:
            stat = target.stat()

            if target.is_file():
                item_type = "file"
            elif target.is_dir():
                item_type = "directory"
            else:
                item_type = "other"

            suffix = target.suffix if target.is_file() else ""

            data = {
                "name": target.name,
                "path": str(target),
                "type": item_type,
                "size": stat.st_size,
                "extension": suffix,
                "created": stat.st_ctime,
                "modified": stat.st_mtime,
            }

            return ToolResult.ok(
                f"Retrieved information for '{target}'.",
                data,
            )

        except OSError as exc:
            return ToolResult.error(
                f"Unable to get information for '{path}': {exc}"
            )