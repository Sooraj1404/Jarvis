from pathlib import Path

from tools.base import Tool
from tools.filesystem import FileSystemPolicy
from tools.result import ToolResult


class RenameFileTool(Tool):
    name = "rename_file"
    description = "Rename an approved file within the approved filesystem."

    def __init__(self):
        self.policy = FileSystemPolicy()

    def execute(
        self,
        path: str = "",
        new_name: str = "",
        **kwargs
    ) -> ToolResult:

        if not path.strip():
            return ToolResult.error(
                "No file path was specified."
            )

        if not new_name.strip():
            return ToolResult.error(
                "No new file name was specified."
            )

        source = Path(path.strip())

        valid, error, source_path = self.policy.validate_path(
            str(source)
        )

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

        destination_name = new_name.strip()
        destination_candidate = Path(destination_name)

        if (
            destination_candidate.name != destination_name
            or destination_candidate.is_absolute()
        ):
            return ToolResult.error(
                "New file name must be a file name, not a path."
            )

        destination = source_path.parent / destination_name

        valid, error, destination_path = self.policy.validate_path(
            str(destination)
        )

        if not valid:
            return ToolResult.error(error)

        if destination_path.exists():
            return ToolResult.error(
                f"Destination file already exists: "
                f"'{destination_name}'."
            )

        try:
            source_path.rename(destination_path)

            return ToolResult.ok(
                f"Renamed '{source_path.name}' to "
                f"'{destination_path.name}'.",
                {
                    "old_path": str(source_path),
                    "new_path": str(destination_path),
                },
            )

        except OSError as exc:
            return ToolResult.error(
                f"Unable to rename file '{path}': {exc}"
            )