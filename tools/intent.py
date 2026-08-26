from tools.command import ToolCommand


class ToolIntentDetector:
    """Detect basic tool-related intents from natural language."""

    POLITE_PREFIXES = (
        "could you please ",
        "could you ",
        "can you please ",
        "can you ",
        "would you please ",
        "would you ",
        "please ",
        "i want you to ",
        "i need you to ",
    )

    POLITE_SUFFIXES = (
    " for me",
    " please",
    )

    ACTION_ALIASES = {
        "launch ": "open ",
        "start ": "open ",
        "show me ": "show ",
        "remove ": "delete file ",
        "get rid of ": "delete file ",
    }

    def detect(self, text: str) -> ToolCommand | None:
        text = text.strip()

        if not text:
            return None

        text = self._normalize_request(text)
        lowered = text.lower()

        # -------------------------------------------------
        # APPLICATION CONTROL
        # -------------------------------------------------

        if lowered.startswith("open "):
            app = text[5:].strip()

            if app:
                return ToolCommand(
                    tool="open_app",
                    arguments={
                        "app": self._clean_value(app),
                    },
                )

        if lowered.startswith("close "):
            app = text[6:].strip()

            if app:
                return ToolCommand(
                    tool="close_app",
                    arguments={
                        "app": self._clean_value(app),
                    },
                )

        # -------------------------------------------------
        # FILESYSTEM - LIST
        # -------------------------------------------------

        if lowered in {
            "list files",
            "show files",
            "list directory",
            "show directory",
            "list the files here",
            "show the files here",
            "show what's in this folder",
            "show whats in this folder",
            "what files are in this directory",
            "what files are in this folder",
        }:
            return ToolCommand(
                tool="list_files",
                arguments={
                    "path": ".",
                },
            )

        # -------------------------------------------------
        # FILESYSTEM - READ
        # -------------------------------------------------

        if lowered.startswith("read "):
            path = text[5:].strip()

            if path:
                return ToolCommand(
                    tool="read_file",
                    arguments={
                        "path": self._clean_value(path),
                    },
                )

        # -------------------------------------------------
        # FILESYSTEM - CREATE FILE
        # -------------------------------------------------

        if lowered.startswith("create file "):
            path = text[12:].strip()

            if path:
                return ToolCommand(
                    tool="create_file",
                    arguments={
                        "path": self._clean_value(path),
                        "content": "",
                    },
                )

        # -------------------------------------------------
        # FILESYSTEM - WRITE FILE
        # -------------------------------------------------

        if lowered.startswith("write to "):
            remainder = text[9:].strip()

            if " with " in remainder.lower():
                path, content = self._split_once(
                    remainder,
                    " with ",
                )

                if path and content:
                    return ToolCommand(
                        tool="write_file",
                        arguments={
                            "path": self._clean_value(path),
                            "content": content.strip(),
                        },
                    )

        # -------------------------------------------------
        # FILESYSTEM - DELETE FILE
        # -------------------------------------------------

        if lowered.startswith("delete file "):
            path = text[12:].strip()

            if path:
                return ToolCommand(
                    tool="delete_file",
                    arguments={
                        "path": self._clean_value(path),
                    },
                )

        # -------------------------------------------------
        # FILESYSTEM - RENAME
        # -------------------------------------------------

        if lowered.startswith("rename "):
            remainder = text[7:].strip()

            if " to " in remainder.lower():
                old_path, new_name = self._split_once(
                    remainder,
                    " to ",
                )

                if old_path and new_name:
                    return ToolCommand(
                        tool="rename_file",
                        arguments={
                            "path": self._clean_value(old_path),
                            "new_name": self._clean_value(new_name),
                        },
                    )

        # -------------------------------------------------
        # FILESYSTEM - MOVE
        # -------------------------------------------------

        if lowered.startswith("move "):
            remainder = text[5:].strip()

            if " to " in remainder.lower():
                source, destination = self._split_once(
                    remainder,
                    " to ",
                )

                if source and destination:
                    return ToolCommand(
                        tool="move_file",
                        arguments={
                            "path": self._clean_value(source),
                            "destination": self._clean_value(destination),
                        },
                    )

        # -------------------------------------------------
        # FILESYSTEM - SEARCH
        # -------------------------------------------------

        if lowered.startswith("find "):
            query = text[5:].strip()

            if query:
                return ToolCommand(
                    tool="search_files",
                    arguments={
                        "query": self._clean_value(query),
                        "path": ".",
                    },
                )

        if lowered.startswith("search for "):
            query = text[11:].strip()

            if query:
                return ToolCommand(
                    tool="search_files",
                    arguments={
                        "query": self._clean_value(query),
                        "path": ".",
                    },
                )

        # -------------------------------------------------
        # DIRECTORY - CREATE
        # -------------------------------------------------

        if lowered.startswith("create directory "):
            path = text[17:].strip()

            if path:
                return ToolCommand(
                    tool="create_directory",
                    arguments={
                        "path": self._clean_value(path),
                    },
                )

        if lowered.startswith("create folder "):
            path = text[14:].strip()

            if path:
                return ToolCommand(
                    tool="create_directory",
                    arguments={
                        "path": self._clean_value(path),
                    },
                )

        # -------------------------------------------------
        # DIRECTORY - DELETE
        # -------------------------------------------------

        if lowered.startswith("delete directory "):
            path = text[17:].strip()

            if path:
                return ToolCommand(
                    tool="delete_directory",
                    arguments={
                        "path": self._clean_value(path),
                    },
                )

        if lowered.startswith("delete folder "):
            path = text[14:].strip()

            if path:
                return ToolCommand(
                    tool="delete_directory",
                    arguments={
                        "path": self._clean_value(path),
                    },
                )

        # -------------------------------------------------
        # FILE INFO
        # -------------------------------------------------

        prefixes = (
            "get information about ",
            "get info about ",
            "show information about ",
            "show info about ",
        )

        for prefix in prefixes:
            if lowered.startswith(prefix):
                path = text[len(prefix):].strip()

                if path:
                    return ToolCommand(
                        tool="get_file_info",
                        arguments={
                            "path": self._clean_value(path),
                        },
                    )

        return None

    @classmethod
    def _normalize_request(cls, text: str) -> str:
        """Normalize common conversational phrasing."""

        normalized = text.strip()

        lowered = normalized.lower()

        for prefix in cls.POLITE_PREFIXES:
            if lowered.startswith(prefix):
                normalized = normalized[len(prefix):].strip()
                break

        lowered = normalized.lower()

        for source, target in cls.ACTION_ALIASES.items():
            if lowered.startswith(source):
                normalized = (
                    target
                    + normalized[len(source):]
                )
                break

        lowered = normalized.lower()

        for suffix in cls.POLITE_SUFFIXES:
            if lowered.endswith(suffix):
                normalized = normalized[:-len(suffix)].strip()
                break

        return normalized
    @staticmethod
    def _clean_value(value: str) -> str:
        """Clean extracted command values."""

        value = value.strip().rstrip(".,!?")

        lowered = value.lower()

        for suffix in (
            " for me",
            " please",
        ):
            if lowered.endswith(suffix):
                value = value[:-len(suffix)].strip()
                break

        return value

    @staticmethod
    def _split_once(
        text: str,
        separator: str,
    ) -> tuple[str, str]:
        """Split text once using a case-insensitive separator."""

        lowered = text.lower()
        index = lowered.find(separator.lower())

        if index == -1:
            return "", ""

        left = text[:index].strip()
        right = text[index + len(separator):].strip()

        return left, right