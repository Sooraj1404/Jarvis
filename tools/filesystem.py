from pathlib import Path


class FileSystemPolicy:
    """Controls which filesystem paths JARVIS tools may access."""

    PROTECTED_NAMES = {
        ".git",
        ".venv",
        "__pycache__",
    }

    def validate_path(self, path: str) -> tuple[bool, str, Path | None]:
        path = path.strip()

        if not path:
            return False, "No directory path was specified.", None

        target = Path(path).expanduser()

        try:
            resolved = target.resolve()
        except OSError as exc:
            return False, f"Unable to resolve path: {exc}", None

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