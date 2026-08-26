from pathlib import Path


class FileSystemPolicy:
    """Controls which filesystem paths JARVIS tools may access."""

    PROTECTED_NAMES = {
        ".git",
        ".venv",
        "__pycache__",
    }

    def __init__(self, allowed_root: Path | None = None):
        if allowed_root is None:
            allowed_root = Path.cwd()

        self.allowed_root = allowed_root.resolve()

    def validate_path(
        self,
        path: str,
    ) -> tuple[bool, str, Path | None]:

        path = path.strip()

        if not path:
            return False, "No path was specified.", None

        target = Path(path).expanduser()

        try:
            resolved = target.resolve()
        except OSError as exc:
            return (
                False,
                f"Unable to resolve path: {exc}",
                None,
            )

        try:
            resolved.relative_to(self.allowed_root)
        except ValueError:
            return (
                False,
                f"Access outside the approved directory is not allowed: "
                f"'{path}'.",
                None,
            )

        protected_names = {
            name.lower()
            for name in self.PROTECTED_NAMES
        }

        for part in resolved.parts:
            if part.lower() in protected_names:
                return (
                    False,
                    f"Access to protected path is not allowed: '{path}'.",
                    None,
                )

        return True, "", resolved