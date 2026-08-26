from tools.base import Tool
from tools.filesystem import FileSystemPolicy
from tools.result import ToolResult


class SearchFilesTool(Tool):
    name = "search_files"
    description = "Search for files and directories by name in an approved path."

    def __init__(self):
        self.policy = FileSystemPolicy()

    def execute(
        self,
        query: str = "",
        path: str = "",
        **kwargs,
    ) -> ToolResult:

        if not query.strip():
            return ToolResult.error(
                "No search query was specified."
            )

        if not path.strip():
            path = "."

        valid, error, root = self.policy.validate_path(path)

        if not valid:
            return ToolResult.error(error)

        if not root.exists():
            return ToolResult.error(
                f"Directory does not exist: '{path}'."
            )

        if not root.is_dir():
            return ToolResult.error(
                f"Search path is not a directory: '{path}'."
            )

        query = query.strip().lower()

        try:
            matches = []

            for entry in root.rglob("*"):
                # Validate every discovered path before returning it.
                valid, _, resolved = self.policy.validate_path(
                    str(entry)
                )

                if not valid:
                    continue

                if query in entry.name.lower():
                    matches.append(
                        {
                            "name": entry.name,
                            "path": str(resolved),
                            "type": (
                                "directory"
                                if entry.is_dir()
                                else "file"
                            ),
                        }
                    )

            matches.sort(
                key=lambda item: item["path"].lower()
            )

            return ToolResult.ok(
                f"Found {len(matches)} matching entries.",
                {
                    "query": query,
                    "root": str(root),
                    "matches": matches,
                },
            )

        except OSError as exc:
            return ToolResult.error(
                f"Unable to search '{path}': {exc}"
            )